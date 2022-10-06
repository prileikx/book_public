import string
import random
from flask import Blueprint, Response, request, session
from blueprints.exts import mail
from flask_mail import Message
from Model import captchaModel, UserModel, unameCheck, book_list,emailCheck
from blueprints.exts import db
import datetime
from PIL import Image, ImageDraw, ImageFont
from config import font_path, img_path

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route('/check_login_status', methods=['POST'])
def check_login_status():
    uid = request.cookies.get('uid')
    toregis = request.form['toregis']
    user = db.session.query(UserModel).filter(UserModel.uid == uid).first()
    verify = session.get('verify')
    if user != None and verify == user.verify and user.verify != None:
        return {"status": [200]}
    elif toregis == "yes" and request.form['webtitle'] != '用户注册' and request.form['webtitle'] != '找回密码':
        return {"status": [301]}
    elif request.form['webtitle'] != '用户登录' and request.form['webtitle'] != '用户注册' and request.form[
        'webtitle'] != '找回密码':
        return {"status": [302]}
    elif request.form['webtitle'] == '找回密码':
        return {"sratus": [303]}
    else:
        return {"status": [201]}


@bp.route('/set_uid_cookie', methods=['POST'])
def set_uid_cookie():
    uid = request.form['uid']
    username = request.form['username']
    # uid=request.args.get("uid")
    response = Response('设置登录信息')
    response.set_cookie("uid", str(uid), max_age=60 * 60 * 24 * 30)
    response.set_cookie("username", username, max_age=60 * 60 * 24 * 30)
    return response


@bp.route('/set_login_session', methods=['POST'])
def set_login_session():
    uid = request.form['uid']
    user = db.session.query(UserModel).filter(UserModel.uid == uid).first()
    verify = get_cpatcha(10)
    user.verify = verify
    db.session.commit()
    session['verify'] = verify
    if request.form['ifsave'] == "true":
        session.permanent = True
    else:
        session.permanent = False
    return 'session设置成功'


@bp.route('del_session', methods=['POST'])
def del_session():
    if (session['verify']):
        del session['verify']
        return {'message': ['已退出登录']}


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
    if(emailCheck(request.form).validate()):
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
                return {"email": ["60秒内只得发送一次邮件"]}
        message = Message(
            subject="[book manage]注册验证码",
            recipients=[email],
            body=f"[测试邮件]您的注册验证码是:{captcha}"
        )
        mail.send(message)
        return {"email": ["邮件发送成功"]}
    else:
        return {"email": ["邮件格式不正确"]}

@bp.route("/send_change_password_email", methods=['POST'])
def send_change_password_email():
    form = request.form
    ucheck = unameCheck(request.form)
    name = form.to_dict()['name']
    print(name)
    if ucheck.validate():
        user_object = db.session.query(UserModel).filter(UserModel.email == name)
    elif name.isdigit():
        user_object = db.session.query(UserModel).filter(UserModel.uid == name)
    elif name.isalnum():
        user_object = db.session.query(UserModel).filter(UserModel.name == name)
    else:
        print(ucheck.errors)
        return {"message": ["未能识别到用户"], "status": ["402"]}
    if (user_object != None):
        user = user_object.first()
        uid = user.uid
        email = user.email
        captcha_object = db.session.query(captchaModel).filter(captchaModel.email == email).first()
        captcha = get_cpatcha(4)
        if (datetime.datetime.now() - db.session.query(captchaModel).filter(
                captchaModel.uid == uid).first().captcha_time).total_seconds() > 60:
            captcha_object.captcha = captcha
            captcha_object.captcha_time = datetime.datetime.now()
            db.session.commit()
            message = Message(
                subject="[book manage]修改密码",
                recipients=[email],
                body=f"[测试邮件]您的修改密码的验证码是:{captcha}"
            )
            mail.send(message)
            return {"message": ["邮件发送成功"], "status": ["200"]}
        else:
            return {"message": ["60秒内只得发送一次邮件"], "status": ["502"]}
    else:
        return {"message": ["未找到该用户"], "status": ["401"]}


@bp.route("/set_book_number", methods=['GET', 'POST'])
def set_book_number():
    for i in range(1, 228):
        book = db.session.query(book_list).filter(book_list.bid == i).first()
        # book.number = random.randint(1, 50)
        # db.session.commit()
    return "ok"


@bp.route("/generate_photo", methods=['GET', 'POST'])
def generate_photo():
    # 背景颜色
    bg_colors = ['#747D9E', '#BFB5B4', '#A1C8CD']
    # 字体颜色
    word_colors = ['#9063A4', '#2F1C32', '#0F1418']
    # 设置待生成字符
    word = request.args.get('word')
    bid = request.args.get('bid')
    # word = request.form.to_dict['word']
    # bid = request.form.to_dict['bid']
    # word = db.session.query(book_list).filter(book_list.bid == i).first().bname
    # bid = str(db.session.query(book_list).filter(book_list.bid == i).first().bid)
    img_save_path = img_path + bid + ".png"
    # (200,400)为图片尺寸
    image = Image.new("RGB", (200, 300), color=random.choice(bg_colors))
    draw_table = ImageDraw.Draw(im=image)
    # xy为文字在图片中的位置,font为字体及大小
    draw_table.text(xy=(5, 5), text=word, fill=random.choice(word_colors), font=ImageFont.truetype(font_path, 25))
    image.save(img_save_path)
    return "成功"


def check_user_limits(uid, verify, need_limits):  # 传入uid和需要的权限来判断用户是否拥有足够的权限
    user = db.session.query(UserModel).filter(UserModel.uid == uid).first()
    if (user != None):
        if user.verify == verify:
            if user.limits >= need_limits:
                return 200  # 用户可以成功访问
            else:
                return "用户权限不足"
        else:
            return "用户已退出登录(用户验证错误)"
    else:
        return "用户不存在"  # check_user_limits(request.cookies.get('uid'),session['verify'],100)
