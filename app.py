from flask import Flask, jsonify, render_template, request, session
import config
from blueprints import user_bp
from blueprints import api_bp, library_bp
from blueprints.exts import db, mail
from Model import book_list

app = Flask(__name__)
app.config.from_object(config)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI
db.init_app(app)
mail.init_app(app)
app.register_blueprint(user_bp)
app.register_blueprint(api_bp)
app.register_blueprint(library_bp)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('/homepage.html')


@app.route('/homepage')
def homepage():
    return render_template('/homepage.html')


@app.route('/library')
def library():
    return render_template('/library.html')


@app.route('/test')
def test():  # put application's code here

    engine = db.get_engine()
    with engine.connect() as conn:
        result = conn.execute("select * from book_user")
        print(type(result.fetchone()))
        return jsonify(result.fetchone()[0])


@app.route('/search',methods=['POST','GET'])
def search():
    if request.method == 'GET':
        if (request.args.to_dict() == {}):
            data = {
                "page": 1,
                "search_text": "",
                "choose": "bname",
                "result_number": 0
            }
            return render_template('search.html', data=data)
        else:
            search_text = request.args['search_text']
            page = request.args['page']
            choose = request.args['choose']
            if search_text == "":
                if choose != "":
                    data = {
                        "page": 1,
                        "search_text": "",
                        "choose": choose,
                        "result_number": 0,
                        "bid": [],
                        "bname": []
                    }
                    return render_template('search.html', data=data)
                else:
                    data = {
                        "page": 1,
                        "search_text": "",
                        "choose": "bname",
                        "result_number": 0,
                        "bid": [],
                        "bname": []
                    }
                    return render_template('search.html', data=data)
            else:
                search_result = db.session.query(book_list).filter(book_list.bname.like("%" + search_text + "%")).all()
                result_number = db.session.query(book_list).filter(
                    book_list.bname.like("%" + search_text + "%")).count()
                bid = []
                bname = []
                for r in search_result:
                    bid.append(r.bid)
                    bname.append(r.bname)
                data = {
                    "page": 1,
                    "search_text": search_text,
                    "choose": choose,
                    "result_number": result_number,
                    "bid": bid,
                    "bname": bname
                }
                return render_template('search.html', data=data)
    else:
        search_text = request.form['search_text']
        choose = request.form['choose']
        page = int(request.form['page'])
        page = page-1
        page_size=10
        if choose == "bname":
            search_result = db.session.query(book_list).filter(book_list.bname.like("%" + search_text + "%")).limit(10).offset(page * page_size).all()
            result_number = db.session.query(book_list).filter(book_list.bname.like("%" + search_text + "%")).count()
        elif choose == "author":
            search_result = db.session.query(book_list).filter(book_list.author.like("%" + search_text + "%")).limit(10).offset(page * page_size).all()
            result_number = db.session.query(book_list).filter(book_list.author.like("%" + search_text + "%")).count()
        elif choose == "press":
            search_result = db.session.query(book_list).filter(book_list.press.like("%" + search_text + "%")).limit(10).offset(page * page_size).all()
            result_number = db.session.query(book_list).filter(book_list.press.like("%" + search_text + "%")).count()
        bid = []
        bname = []
        for r in search_result:
            bid.append(r.bid)
            bname.append(r.bname)
        return {"status":[200],"bid":bid,"bname":bname,"result_number":result_number}



if __name__ == '__main__':
    app.run()
