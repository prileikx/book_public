from api import check_user_limits
from flask import Blueprint, request, render_template,session
from Model import book_list, UserModel
from blueprints.exts import db

bp = Blueprint("library", __name__, url_prefix="/library")


@bp.route("/books/<int:bid>")
def books_bid(bid):
    book_object = db.session.query(book_list).filter(book_list.bid == bid)
    if (book_object.first() == None):
        psrc = "/static/upload/" + "0.png"
        data = {"psrc": [psrc],
                "status": ["404"],
                "bid": [bid],
                "bname": ["无法找到该图书"],
                "author": ["None"],
                "press": ["None"],
                "isbn_code": ["None"],
                "book_class": ["None"],
                "price": ["None"],
                "number": ["None"],
                "Issue_date": ["None"],
                "introduce": ["None"]
                }
        return render_template('books.html', data=data)
    else:
        book = book_object.first()
        psrc = "/static/upload/" + str(bid) + ".png"
        data = {"psrc": [psrc],
                "status": ["200"],
                "bid": [bid],
                "bname": [book.bname],
                "author": [book.author],
                "press": [book.press],
                "isbn_code": [book.isbn_code],
                "book_class": [book.book_class],
                "price": [book.price],
                "number": [book.number],
                "Issue_date": [book.Issue_date],
                "introduce": [book.introduce]
                }
        return render_template('books.html', data=data)


@bp.route("/", methods=['GET', 'POST'])
def all_books():
    if request.method == 'GET':
        return render_template('/library.html')
    else:
        form = request.form
        uid = request.cookies.get("uid")
        page = int(form.to_dict()['page'])
        if (page > 0):
            page = page - 1
        user = db.session.query(UserModel).filter(UserModel.uid == uid)
        print("函数已被调用")
        page_size = 10
        if (user != None):
            if (user.first().limits >= 10):
                books = db.session.query(book_list).limit(page).offset((page) * page_size)
                print(page)
                start = page * page_size
                print(start)
                #数据库中图书的总条目数
                count = db.session.query(book_list).count()
                if(count%10 == 0):
                    pageall = count//10
                else:
                    pageall = count//10+1
                response = {
                    "status":[200],
                    "pageall":[pageall],
                    "page":[page],
                    "bid":[start,start+1,start+2,start+3,start+4,start+5,start+6,start+7,start+8,start+9],
                    "bname":[books[0].bname,
                             books[1].bname,
                             books[2].bname,
                             books[3].bname,
                             books[4].bname,
                             books[5].bname,
                             books[6].bname,
                             books[7].bname,
                             books[8].bname,
                             books[9].bname,
                             ]
                }
                print(db.session.query(book_list).count())
        return response

@bp.route("add_book",methods=['POST'])
def add_book():
    check = check_user_limits(request.cookies.get('uid'),session['verify'],100)
    if(check == 200):
        form = request.form
        if(book_list(form).validate):
            bname = form['bname']
            author = form['author']
            press = form['press']
            isbn_code = form['isbn_code']
            book_class = form['book_class']
            price = form['price']
            number = form['number']
            Issue_date = form['Issue_date']
            introduce = form['introduce']
            db.session.query(book_list).filter(book_list)
            new_book = book_list(bname=bname,author=author,press=press,isbn_code=isbn_code,book_class=book_class,
                                 price=price,number=number,Issue_date=Issue_date,introduce=introduce)
            db.add(new_book)
            db.commit()
            return {"status":[200]}


