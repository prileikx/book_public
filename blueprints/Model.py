from blueprints.exts import db
import wtforms
from wtforms.validators import length,email,EqualTo,ValidationError,Regexp
#Regexp是正则表达式验证ragex='正则模式'
class UserModel(db.Model):
    __tablename__ = "book_user"
    uid = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(20),nullable=False)
    psw = db.Column(db.String(200),nullable=True)
    email = db.Column(db.String(40),nullable=False)
    limits = db.Column(db.Integer,nullable=False)
    notes = db.Column(db.String(255))
    session = db.Column(db.String(10))
    session_time = db.Column(db.DateTime)
    verify = db.Column(db.String(10))

def unameJuage(form,filed):
    if filed.data.isalnum()==True:
        return
    raise ValidationError("用户名不能包含特殊字符")

class registerForm(wtforms.Form):
    name = wtforms.StringField(validators=[length(min=1,max=20,message="用户名长度不符"),unameJuage])
    email = wtforms.StringField(validators=[email(message="邮箱格式不正确")])
    captcha = wtforms.StringField(validators=[length(min=4,max=4,message="验证码不正确")])
    pwd = wtforms.StringField(validators=[length(min=6,max=16,message="密码长度不符"),EqualTo('confirm',message="两次密码输入不一致")])
    confirm = wtforms.StringField()

class captchaModel(db.Model):
    __tablename__ = "captcha"
    uid = db.Column(db.Integer,nullable=False,primary_key=True)
    email = db.Column(db.String(40),nullable=False)
    captcha = db.Column(db.String(4),nullable=False)
    captcha_time = db.Column(db.DateTime)

class usernameCheck(wtforms.Form):
    uname_login = wtforms.StringField(validators=[email(message="邮箱格式不正确")])

class unameCheck(wtforms.Form):
    name = wtforms.StringField(validators=[email(message="邮箱格式不正确")])

class emailCheck(wtforms.Form):
    email = wtforms.StringField(validators=[email(message="邮箱格式不正确")])

class book_list(db.Model):
    __tablename__ = "book_list"
    bid = db.Column(db.Integer,primary_key=True,autoincrement=True)
    bname = db.Column(db.String(100),nullable=False)
    author = db.Column(db.String(50),nullable=True)
    press = db.Column(db.String(30),nullable=False)
    isbn_code = db.Column(db.String(20),nullable=False)
    book_class = db.Column(db.String(10),nullable=False)
    price = db.Column(db.DECIMAL,nullable=False)
    number = db.Column(db.Integer,nullable=False)
    Issue_date = db.Column(db.String(10),nullable=False)
    introduce = db.Column(db.String(255),nullable=True)