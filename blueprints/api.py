import string
import random
from flask import Blueprint, Response, request, session
from blueprints.exts import mail
from flask_mail import Message
from Model import captchaModel, UserModel, unameCheck, book_list,captcha_for_change_email, emailCheck, book_borrow, book_favourite, user_msg
from blueprints.exts import db
import datetime
from PIL import Image, ImageDraw, ImageFont
from config import font_path, img_path
from sqlalchemy import and_, desc,or_

bp = Blueprint("api", __name__, url_prefix="/api")

@bp.route('/new_sys_msg',methods=['POST'])
def new_sys_msg():
    check = check_user_limits(request.cookies.get('uid'), session['verify'], 100)
    if (check == 200):
        msg="系统公告:"+request.form['sys_msg']
        print(msg)
        new_msg = user_msg(uid=37,msg=msg)
        db.session.add(new_msg)
        db.session.commit()
        db.session.close()
        return {"status":[200],"message":["成功"]}
    else:
        return {"status": [502], "message": ["权限不足"]}

@bp.route('/send_email_for_change_email', methods=['POST'])
def send_email_for_change_email():
    uid = request.cookies.get('uid')
    verify = session.get('verify')
    check = check_user_is_true(uid, verify)
    if check == 200:
        email = request.form['new_email_send']
        captcha = get_cpatcha(4)
        if db.session.query(UserModel).filter(UserModel.email == email).first() == None:
            user_captcha = db.session.query(captcha_for_change_email).filter(captcha_for_change_email.uid == uid).first()
            if user_captcha == None:
                ucpa = captcha_for_change_email(uid=uid,email=email,captcha=captcha)
                db.session.add(ucpa)
                db.session.commit()
                db.session.close()
                message = Message(
                    subject="[book manage]修改邮箱验证码",
                    recipients=[email],
                    body=f"[测试邮件]您的修改邮箱验证码是:{captcha}"
                )
                mail.send(message)
                return {"status": [200]}
            else:
                user_captcha.captcha=captcha
                db.session.commit()
                db.session.close()
                message = Message(
                    subject="[book manage]注册验证码",
                    recipients=[email],
                    body=f"[测试邮件]您的注册验证码是:{captcha}"
                )
                mail.send(message)
                return {"status": [200]}
        else:
            return {"status": [502],"message":["该邮箱已被注册,无法修改为此邮箱"]}
    else:
        return {"status": [502],"message":[check]}

# 检查登录状态
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


# 设置uid的cookie
@bp.route('/set_uid_cookie', methods=['POST'])
def set_uid_cookie():
    uid = request.form['uid']
    username = request.form['username']
    # uid=request.args.get("uid")
    response = Response('设置登录信息')
    response.set_cookie("uid", str(uid), max_age=60 * 60 * 24 * 30)
    response.set_cookie("username", username, max_age=60 * 60 * 24 * 30)
    return response


# 设置登录session
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


# 删除session
@bp.route('del_session', methods=['POST'])
def del_session():
    if (session['verify']):
        del session['verify']
        return {'message': ['已退出登录']}


# 设置cookie示例
@bp.route('/set_cookie')
def set_cookie():
    response = Response("cookie 设置")
    response.set_cookie("user_uid", "0001")
    return response


# 获取cookie示例
@bp.route('/get_cookie')
def get_cookie():
    user_uid = request.cookies.get("user_uid")
    print("user_uid:", user_uid)
    return "获取cookie"


# 设置session示例
@bp.route('/set_session')
def set_session():
    session['username'] = 'admin'
    session.permanent = True
    return 'session设置成功'


# 获取session示例
@bp.route('/get_session')
def get_session():
    username = session.get('username')
    return '获得username=' + username


# 生成验证码,传入一个数字生成指定位数的验证码
@bp.route('/get_captcha')
def get_cpatcha(number):
    letters = string.ascii_letters + string.digits
    captcha = "".join(random.sample(letters, number))
    return captcha


# 发送邮件
@bp.route("/send_email", methods=['POST'])
def send_mail():
    captcha = get_cpatcha(4)
    email = request.form['email']
    if (emailCheck(request.form).validate()):
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


# 发送修改密码的邮件
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
    if (user_object.first() != None):
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


# 设置图书数量(已废弃)
@bp.route("/set_book_number", methods=['GET', 'POST'])
def set_book_number():
    # for i in range(1, 228):
    #     book = db.session.query(book_list).filter(book_list.bid == i).first()
    # book.number = random.randint(1, 50)
    # db.session.commit()
    return "ok"


# 生成图片,用于生成默认图书的封面
# @bp.route("/generate_photo", methods=['GET', 'POST'])
def generate_photo(word, bid):
    # 背景颜色
    bg_colors = ['#747D9E', '#BFB5B4', '#A1C8CD']
    # 字体颜色
    word_colors = ['#9063A4', '#2F1C32', '#0F1418']
    # 设置待生成字符
    # word = request.args.get('word')
    # bid = request.args.get('bid')
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


# 检查是否为管理员,返回200为管理员
@bp.route("/check_admin", methods=['POST'])
def check_admin():
    if check_user_limits(request.cookies.get('uid'), session['verify'], 100) == 200:
        return {"status": [200]}
    else:
        return {"status": [502]}


# 检查用户权限,传入uid,verify(session)和需要的权限三项来验证是否符合条件
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


# 检查用户session及uid是否对应
def check_user_is_true(uid, verify):
    user = db.session.query(UserModel).filter(UserModel.uid == uid).first()
    if (user != None):
        if user.verify == verify:
            return 200  # 用户可以成功访问
        else:
            return "用户已退出登录(用户验证错误),请重新登陆以解决此问题"
    else:
        return "用户不存在,请重新登陆以解决此问题"  # check_user_limits(request.cookies.get('uid'),session['verify'],100)


# 检查用户的借阅数量
@bp.route('/check_borrow_number', methods=['POST'])
def check_borrow_number():
    uid = request.cookies.get('uid')
    verify = session.get('verify')
    check = check_user_is_true(uid, verify)
    if check == 200:
        user_borrow_number = db.session.query(book_borrow).filter(
            and_(book_borrow.uid == uid, book_borrow.book_status == 2)).count()
        return {"status": [200], "number": [user_borrow_number]}
    else:
        return {"status": [502], "message": [check]}


# 检查用户的借阅列表
@bp.route('/check_borrow_list', methods=['POST'])
def check_borrow_list():
    uid = request.cookies.get('uid')
    verify = session.get('verify')
    check = check_user_is_true(uid, verify)
    if check == 200:
        books = db.session.query(book_borrow).filter(book_borrow.uid == uid).all()
        book_appointtime = []
        book_user = []
        book_borrowtime = []
        book_back_time = []
        book_status = []
        book_name = []
        book_bid = []
        list_number = 0
        for book in books:
            book_bid.append(book.bid)
            book_name.append(db.session.query(book_list.bid == book.bid).first())
            if book.appointment_time != None:
                book_appointtime.append(book.appointment_time.strftime("%Y/%m/%d, %H:%M:%S"))
            else:
                book_appointtime.append("-")
            book_user.append(db.session.query(UserModel).filter(UserModel.uid == book.uid).first().name)
            if book.borrow_time != None:
                book_borrowtime.append(book.borrow_time.strftime("%Y/%m/%d, %H:%M:%S"))
            else:
                book_borrowtime.append("-")
            if book.back_time != None:
                book_back_time.append(book.back_time.strftime("%Y/%m/%d, %H:%M:%S"))
            else:
                book_back_time.append("-")
            book_status.append(book.book_status)
            list_number = list_number + 1
        return {"status": [200], "book_bid": book_bid, "book_user": book_user, "book_status": book_status,
                "book_appointtime": book_appointtime, "book_borrowtime": book_borrowtime,
                'book_back_time': book_back_time, "list_number": list_number, "book_name": book_name}
    else:
        return {"status": [502], "message": [check]}


# @bp.route('/upload_photo',methods=['POST'])
# def upload_photo(img):
#     img = request.files.get('photo')
#     img.save("D:/project_developer/book_manage/static/upload/books/img/test.jpg")
#     return "ok"

# 返回用户的喜爱图书列表
@bp.route('/my_fav', methods=['POST'])
def my_fav():
    uid = request.cookies.get('uid')
    verify = session.get('verify')
    check = check_user_is_true(uid, verify)
    if check == 200:
        count = 0
        books_fav = db.session.query(book_favourite).filter(book_favourite.uid == uid).order_by(desc('fav_time')).all()
        if books_fav == None:
            return {"status": [204], "message": ["没有收藏图书"]}
        else:
            book_bid = []
            book_name = []
            book_fav_time = []
            for book in books_fav:
                count = count + 1
                book_bid.append(book.bid)
                book_name.append(db.session.query(book_list).filter(book_list.bid == book.bid).first().bname)
                book_fav_time.append(book.fav_time.strftime("%Y/%m/%d, %H:%M:%S"))
            return {"status": [200], "book_bid": book_bid, "book_name": book_name, "book_fav_time": book_fav_time,
                    "countb": [count]}
    else:
        return {"status": [502], "message": [check]}


# 返回图书预约信息
@bp.route('/pre_borrow_book_msg', methods=['POST'])
def pre_borrow_book_msg():
    uid = request.cookies.get('uid')
    verify = session.get('verify')
    check = check_user_is_true(uid, verify)
    if check == 200:
        books = db.session.query(book_borrow).filter(
            and_(book_borrow.uid == uid, book_borrow.book_status == 1)).order_by(desc('appointment_time')).all()
        if books == None:
            return {"status": [204], "message": ["没有收藏图书"]}
        else:
            book_appointtime = []
            book_name = []
            book_bid = []
            list_number = 0
            for book in books:
                # 检查图书预约信息是否过期,如果过期就往信息里添加消息,并且把书籍状态设为0
                if (datetime.datetime.now() - book.appointment_time).total_seconds() > 60 * 60 * 24 * 3:
                    book_number = db.session.query(book_list).filter(book_list.bid == book.bid).first().number
                    book_number = book_number + 1
                    book.appointment_time = None
                    book.book_status = 0
                    msg = user_msg(uid=uid, msg="您的预约《" + db.session.query(book_list).filter(
                        book_list.bid == book.bid).first().bname + "》已过期,请重新预约")
                    db.session.add(msg)
                    db.session.commit()
                    db.session.close()
                else:
                    if book.appointment_time != None:
                        book_appointtime.append(book.appointment_time.strftime("%Y/%m/%d, %H:%M:%S"))
                    else:
                        book_appointtime.append("-")
                    book_bid.append(book.bid)
                    book_name.append(db.session.query(book_list).filter(book_list.bid == book.bid).first().bname)
                    list_number = list_number + 1
            countb = []
            countb.append(list_number)
            return {"status": [200], "book_name": book_name, "book_appointtime": book_appointtime, "countb": countb,
                    "book_bid": book_bid}
    else:
        return {"status": [502]}


# 返回用户消息
@bp.route('/my_msg_find', methods=['POST'])
def my_msg_find():
    uid = request.cookies.get('uid')
    verify = session.get('verify')
    check = check_user_is_true(uid, verify)
    if check == 200:
        msg_all = db.session.query(user_msg).filter(or_(user_msg.uid == uid,user_msg.uid == 37)).order_by(desc('mid')).all()
        user_msg_list = []
        list_number = 0
        for msg_p in msg_all:
            user_msg_list.append(msg_p.msg)
            list_number = list_number + 1
        countb = []
        countb.append(list_number)
        return {"status": [200], "msg": user_msg_list, "countb": countb}
    else:
        return {"status": [502]}


# 返回图书借阅信息
@bp.route('/borrow_book_msg', methods=['POST'])
def borrow_book_msg():
    uid = request.cookies.get('uid')
    verify = session.get('verify')
    check = check_user_is_true(uid, verify)
    if check == 200:
        books = db.session.query(book_borrow).filter(
            and_(book_borrow.uid == uid, book_borrow.book_status == 2)).order_by(desc('borrow_time')).all()
        if books == None:
            return {"status": [204], "message": ["没有借阅图书"]}
        else:
            book_borrowtime = []
            book_name = []
            book_bid = []
            list_number = 0
            book_back_time = []
            for book in books:
                if book.back_time != None:
                    book_back_time.append(book.back_time.strftime("%Y/%m/%d, %H:%M:%S"))
                else:
                    book_back_time.append("-")
                book_bid.append(book.bid)
                book_name.append(db.session.query(book_list).filter(book_list.bid == book.bid).first().bname)
                list_number = list_number + 1
                book_borrowtime.append(book.borrow_time.strftime("%Y/%m/%d, %H:%M:%S"))
            countb = []
            countb.append(list_number)
            return {"status": [200], "book_name": book_name,"book_back_time":book_back_time, "book_borrowtime": book_borrowtime, "countb": countb,
                    "book_bid": book_bid}
    else:
        return {"status": [502]}
