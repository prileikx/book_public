from flask import Flask, jsonify, render_template

import config
from blueprints import user_bp
from blueprints import api_bp,library_bp
from blueprints.exts import db, mail


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

if __name__ == '__main__':
    app.run()
