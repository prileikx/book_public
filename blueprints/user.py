from flask import Blueprint, request, render_template, session
import datetime
from blueprints.exts import db
from werkzeug.security import generate_password_hash, check_password_hash
from Model import UserModel, registerForm, captchaModel, unameCheck, usernameCheck, book_list, user_msg, book_borrow, \
    book_favourite,captcha_for_change_email
from api import check_user_is_true
from sqlalchemy import and_, desc,or_

bp = Blueprint("user", __name__, url_prefix="/user")

@bp.route("/change_email",methods=['POST'])
def change_email():
    uid = request.cookies.get('uid')
    verify = session.get('verify')
    check = check_user_is_true(uid, verify)
    if check == 200:
        captcha = request.form['captcha_for_change_email']
        captcha_for_chge_email_model=db.session.query(captcha_for_change_email).filter(captcha_for_change_email.uid == uid).first()
        if captcha.lower() == captcha_for_chge_email_model.captcha.lower():
            user = db.session.query(UserModel).filter(UserModel.uid == uid).first()
            user.email = captcha_for_chge_email_model.email
            db.session.commit()
            db.session.close()
            return {"status": [200], "message": ["邮箱修改成功"]}
        else:
            return {"status": [502], "message": ["验证码错误"]}
    else:
        return {"status": [502], "message": [check]}



@bp.route("/change_uname",methods=['POST'])
def change_uname():
    uid = request.cookies.get('uid')
    verify = session.get('verify')
    check = check_user_is_true(uid, verify)
    if check == 200:
        pwd = request.form['pwd']
        user_object = db.session.query(UserModel).filter(UserModel.uid == uid)
        if check_password_hash(user_object.first().psw, pwd):
            user_object.first().name = request.form['uname_text']
            db.session.commit()
            db.session.close()
            return {"status":[200],"message":["用户名修改成功"]}
        else:
            return {"status": [502], "message": ["密码错误"]}
    else:
        return {"status": [502], "message": [check]}

@bp.route("change_pwd_know_pwd",methods=['POST'])
def change_pwd_know_pwd():
    uid = request.cookies.get('uid')
    verify = session.get('verify')
    check = check_user_is_true(uid, verify)
    if check == 200:
        ori_pwd=request.form['origin_pwd']
        user = db.session.query(UserModel).filter(UserModel.uid == uid).first()
        if check_password_hash(user.psw, ori_pwd):
            user.psw = generate_password_hash(request.form['change_pwd'])
            print(request.form['change_pwd'])
            user.verify = None
            db.session.commit()
            db.session.close()
            return {"status": [200], "message": ["密码修改成功,请重新登录"]}
        else:
            return {"status": [502], "message": ["原密码错误"]}
    else:
        return {"status": [502], "message": [check]}

@bp.route("/account")
def user():
    uid = request.cookies.get('uid')
    verify = session.get('verify')
    check = check_user_is_true(uid, verify)
    if check == 200:
        user = db.session.query(UserModel).filter(UserModel.uid == uid).first()
        user_limits = user.limits
        if user_limits == 10:
            u_group = "普通用户"
        elif user_limits == 100:
            u_group = "管理员"
        if request.args.to_dict() == {}:
            data = {
                "status": 200,
                "choose": "user_msg",
                "uname": user.name,
                "u_group": u_group,
                "email": user.email,
                "uid": uid,
                "borrow_book_number": db.session.query(book_borrow).filter(
                    and_(book_borrow.uid == uid, book_borrow.book_status == 2)).count(),
                "fav_book_number": db.session.query(book_favourite).filter(book_favourite.uid == uid).count()
            }
            return render_template('/user.html', data=data)
        else:
            if request.args['choose'] == 'user_msg':
                data = {
                    "status": 200,
                    "choose": "user_msg",
                    "uname": user.name,
                    "u_group": u_group,
                    "email": user.email,
                    "uid": uid,
                    "borrow_book_number": db.session.query(book_borrow).filter(
                        and_(book_borrow.uid == uid, book_borrow.book_status == 2)).count(),
                    "fav_book_number": db.session.query(book_favourite).filter(book_favourite.uid == uid).count()
                }
                return render_template('/user.html', data=data)
            elif request.args['choose'] == 'account_manage':
                data = {
                    "status": 202,
                    "choose": "user_msg",
                    "uname": user.name,
                    "email": user.email
                }
                return render_template('/user.html', data=data)
            elif request.args['choose'] == 'my_fav':
                count = 0
                books_fav = db.session.query(book_favourite).filter(book_favourite.uid == uid).order_by(
                    desc('fav_time')).all()
                if books_fav == None:
                    data = {
                        "status": [203],
                        "choose": "my_fav",
                        "book_bid": [0],
                        "book_name": ["没有收藏任何图书"],
                        "book_fav_time": ["-"],
                        "countb": 1
                    }
                    return render_template('/user.html', data=data)
                else:
                    book_bid = []
                    book_name = []
                    book_fav_time = []
                    for book in books_fav:
                        count = count + 1
                        book_bid.append(book.bid)
                        book_name.append(db.session.query(book_list).filter(book_list.bid == book.bid).first().bname)
                        book_fav_time.append(book.fav_time.strftime("%Y/%m/%d, %H:%M:%S"))
                data = {
                    "status": 203,
                    "choose": "my_fav",
                    "book_bid": book_bid,
                    "book_name": book_name,
                    "book_fav_time": book_fav_time,
                    "countb": count
                }
                return render_template('/user.html', data=data)
            elif request.args['choose'] == "my_pre_borrow":
                books = db.session.query(book_borrow).filter(
                    and_(book_borrow.uid == uid, book_borrow.book_status == 1)).order_by(desc('appointment_time')).all()
                if books == None:
                    data = {
                        "status": 204,
                        "choose": "my_pre_borrow",
                        "book_name": ["没有预约任何图书"],
                        "book_appointtime": ["-"],
                        "countb": 1,
                        "book_bid": [0]
                    }
                    return render_template('/user.html', data=data)
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
                            book_name.append(
                                db.session.query(book_list).filter(book_list.bid == book.bid).first().bname)
                            list_number = list_number + 1
                    countb = []
                    countb.append(list_number)
                    data = {
                        "status": 204,
                        "book_name": book_name,
                        "choose": "my_pre_borrow",
                        "book_appointtime": book_appointtime,
                        "countb": countb,
                        "book_bid": book_bid
                    }
                    return render_template('/user.html', data=data)
            elif request.args['choose'] == "my_borrow":
                books = db.session.query(book_borrow).filter(
                    and_(book_borrow.uid == uid, book_borrow.book_status == 2)).order_by(desc('borrow_time')).all()
                if books == None:
                    data = {
                        "status": 205,
                        "choose": "my_borrow",
                        "book_name": ['没有借阅任何图书'],
                        "book_back_time": ['-'],
                        "book_borrowtime": ['-'],
                        "countb": 1,
                        "book_bid": [0]
                    }
                    return render_template('/user.html', data=data)
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
                    data = {
                        "status": 205,
                        "book_name": book_name,
                        "choose": "my_borrow",
                        "book_back_time": book_back_time,
                        "book_borrowtime": book_borrowtime,
                        "countb": countb,
                        "book_bid": book_bid
                    }
                    return render_template('/user.html', data=data)
            elif request.args['choose'] == "my_msg":
                msg_all = db.session.query(user_msg).filter(or_(user_msg.uid == uid,user_msg.uid == 37)).order_by(desc('mid')).all()
                user_msg_list = []
                list_number = 0
                for msg_p in msg_all:
                    user_msg_list.append(msg_p.msg)
                    list_number = list_number + 1
                countb = []
                countb.append(list_number)
                data={
                    "status": 206,
                    "choose": "my_msg",
                    "user_msg_list": user_msg_list,
                    "countb": countb
                }
                return render_template('/user.html', data=data)
    else:
        data = {
            "status": 200,
            "choose": check,
            "uname": check,
            "u_group": check,
            "email": check
        }
        return render_template('/user.html', data=data)


@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('/login.html')
    else:
        status = 502
        form = request.form
        ucheck = usernameCheck(request.form)
        uname = form.to_dict()['uname_login']
        pwd = form.to_dict()['pwd_login']
        rmb_me = form.to_dict()['remember_me']
        if ucheck.validate():
            user_object = db.session.query(UserModel).filter(UserModel.email == uname)
        elif uname.isdigit():
            user_object = db.session.query(UserModel).filter(UserModel.uid == uname)
        elif uname.isalnum():
            user_object = db.session.query(UserModel).filter(UserModel.name == uname)
        else:
            return {"message": ["无法识别用户名,请检查您的输入是否正确"]}
        if user_object.first() == None:
            return {"message": ["用户名/邮箱/uid错误"]}
        if check_password_hash(user_object.first().psw, pwd):
            status = 200
            if rmb_me == "true":
                ifsave = True
            else:
                ifsave = False
            return {"message": ["登陆成功,欢迎用户" + user_object.first().name],
                    "status": [status],
                    "uid": [user_object.first().uid],
                    "ifsave": [ifsave],
                    "username": [user_object.first().name]
                    }  # 若在此处返回response,cookie才会生效,否则无效
        else:
            return {"message": ["密码错误"]}


@bp.route('/register', methods=['GET', 'POST'])
def register():
    # name=request.args.get("name")
    # psw=request.args.get("psw")
    # engine = db.get_engine()
    # with engine.connect() as conn:
    #     abc = conn.execute("insert into book_user(uid,name,psw) value(0,'%s',MD5('%s'));" % (name,psw))
    # return render_template("register.html",**context)
    if request.method == 'GET':
        return render_template('/register.html')
    else:
        form = registerForm(request.form)
        if form.validate():
            na = form.name.data
            psw = form.pwd.data
            captcha = form.captcha.data
            ema = form.email.data
            if na.isdigit():
                return {"name": ["用户名不能为纯数字"]}
            if db.session.query(UserModel).filter(UserModel.name == na).first() != None:
                return {"name": ["该用户名已被注册,请换一个用户名"]}
            if db.session.query(UserModel).filter(UserModel.email == ema).first() == None:
                return {"email": ["该邮箱未发过验证码,请重新发送验证码"]}
            if db.session.query(UserModel).filter(UserModel.email == ema).first().limits != -1:
                return {"email": ["该邮箱已被注册"]}
            if captcha.lower() == db.session.query(captchaModel).filter(
                    captchaModel.email == ema).first().captcha.lower():
                if (datetime.datetime.now() - db.session.query(captchaModel).filter(
                        captchaModel.email == ema).first().captcha_time).total_seconds() < 300:
                    hash_pwd = generate_password_hash(psw)
                    # engine = db.get_engine()
                    # with engine.connect() as conn:
                    #     abc = conn.execute("insert into book_user(uid,name,psw) value(0,'%s',MD5('%s'));" % (name,psw))
                    #     return '注册成功,注册名'+name
                    abc = db.session.query(UserModel).filter(UserModel.email == ema).first()
                    abc.psw = hash_pwd
                    abc.name = na
                    abc.limits = 10
                    db.session.commit()
                    cap = db.session.query(captchaModel).filter(captchaModel.email == ema).first()
                    cap.captcha = ""
                    msg = user_msg(uid=abc.uid, msg="欢迎您注册本系统,您可以在本系统管理您的书籍借阅信息")
                    db.session.add(msg)
                    db.session.commit()
                    return {"name": ["注册成功!用户名:" + na]}
                else:
                    return {"captcha": ["验证码过期,请重新获取验证码"]}
            else:
                return {"captcha": ["验证码错误"]}
        else:
            return form.errors


# 修改密码
@bp.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'GET':
        return render_template('/change_password.html')
    else:
        form = request.form
        ucheck = unameCheck(request.form)
        name = form.to_dict()['name']
        print(ucheck)
        if ucheck.validate():
            user_object = db.session.query(UserModel).filter(UserModel.email == name)
        elif name.isdigit():
            user_object = db.session.query(UserModel).filter(UserModel.uid == name)
        elif name.isalnum():
            user_object = db.session.query(UserModel).filter(UserModel.name == name)
        else:
            return {"message": "无法识别该用户"}
        if (user_object != None):
            user = user_object.first()
            email = user.email
            captcha_object = db.session.query(captchaModel).filter(captchaModel.email == email).first()
            captcha = form.to_dict()['captcha']
            if captcha.lower() == captcha_object.captcha.lower():
                if (datetime.datetime.now() - db.session.query(captchaModel).filter(
                        captchaModel.email == email).first().captcha_time).total_seconds() < 300:
                    if len(form.to_dict()['password']) > 16 or len(form.to_dict()['password']) < 6:
                        return {"message": ["密码长度不正确"]}
                    hash_pwd = generate_password_hash(request.form.to_dict()['password'])
                    user.psw = hash_pwd
                    db.session.commit()
                    return {"message": ["密码修改成功!"]}
                else:
                    return {"message": ["验证码过期,请重新获取验证码"]}
            else:
                return {"captcha": ["验证码错误"]}
        else:
            return {"message": ["未找到该用户"]}


# 查询用户名
@bp.route('/query_uname', methods=['POST'])
def query_uname():
    uid = request.cookies.get('uid')
    user = db.session.query(UserModel).filter(UserModel.uid == uid).first()
    if user == None:
        return {"status": [404], "uname": [None]}
    else:
        return {"status": [200], "uname": [user.name]}

