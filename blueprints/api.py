import string
import random
from flask import Blueprint, Response, request, session,render_template
from blueprints.exts import mail
from flask_mail import Message
from Model import captchaModel, UserModel
from blueprints.exts import db
import datetime

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route('/check_login_status',methods=['POST'])
def check_login_status():
    uid = request.cookies.get('uid')
    toregis = request.form['toregis']
    user = db.session.query(UserModel).filter(UserModel.uid == uid).first()
    name = session.get('username')
    if user!=None and name == user.name:
        return {"status": [200]}
    elif toregis == "yes" and request.form['webtitle']!='用户注册':
        return {"status": [301]}
    elif request.form['webtitle']!='用户登录' and request.form['webtitle']!='用户注册':
        return {"status": [302]}
    else:
        return {"status": [201]}

@bp.route('/set_uid_cookie', methods=['POST'])
def set_uid_cookie():
    uid = request.form['uid']
    # uid=request.args.get("uid")
    response = Response('设置登录信息')
    response.set_cookie("uid", str(uid), max_age=60 * 60 * 24 * 30)
    return response


@bp.route('/set_login_session',methods=['POST'])
def set_login_session():
    username = request.form['username']
    session['username'] = username
    if request.form['ifsave'] == "true":
        session.permanent = True
    else:
        session.permanent = False
    return 'session设置成功'


@bp.route('/set_cookie')
def set_cookie():
    response = Response("cookie 设置")
    response.set_cookie("user_uid", "0001")
    return response


@bp.route('/get_cookie')
def get_cookie():
    user_uid = request.cookies.get("user_uid")
    print("user_uid:", user_uid)
    return "获取cookie"


@bp.route('/set_session')
def set_session():
    session['username'] = 'admin'
    session.permanent = True
    return 'session设置成功'


@bp.route('/get_session')
def get_session():
    username = session.get('username')
    return '获得username=' + username


@bp.route('/get_captcha')
def get_cpatcha(number):
    letters = string.ascii_letters + string.digits
    captcha = "".join(random.sample(letters, number))
    return captcha


@bp.route("/send_email", methods=['POST'])
def send_mail():
    captcha = get_cpatcha(4)
    email = request.form['email']
    # get方法使用
    # form = registerForm(request.form)
    # email=form.email.data
    # email=request.args.get("email")
    if (db.session.query(UserModel).filter(UserModel.email == email).first() != None and db.session.query(
            UserModel).filter(UserModel.email == email).first().limits != -1):
        return {"email": ["该邮箱已被注册激活,如忘记密码请使用找回密码功能"]}
    if db.session.query(UserModel).filter(UserModel.email == email).first() == None:  # 如果没有该数据就往数据库中添加该数据
        user = UserModel(name=get_cpatcha(20), psw='', email=email, limits=-1)
        db.session.add(user)
        db.session.commit()
    result = db.session.query(UserModel).filter(UserModel.email == email).first()
    # 获取邮箱对应的captcha表数据(若该数据不为空,则修改captcha,否则添加改邮箱和对应的captcha)↑
    if db.session.query(captchaModel).filter(captchaModel.email == email).first() == None:
        capt = captchaModel(uid=result.uid, email=email, captcha=captcha, captcha_time=datetime.datetime.now())
        db.session.add(capt)  # 添加captcha条目
        db.session.commit()
    else:
        if (datetime.datetime.now() - db.session.query(captchaModel).filter(
                captchaModel.email == email).first().captcha_time).total_seconds() > 60:  # 秒数相差60秒以上才能继续发送邮件
            abc = db.session.query(captchaModel).filter(captchaModel.uid == result.uid).first()
            abc.captcha = captcha  # 更新captcha
            abc.captcha_time = datetime.datetime.now()  # 更新captcha_time
            db.session.commit()
        else:
            return
    message = Message(
        subject="email test",
        recipients=[email],
        body=f"[测试邮件]您的注册验证码是:{captcha}"
    )
    mail.send(message)
    return {"email": ["邮件发送成功"]}
