from flask import Blueprint, request, render_template
import datetime
from blueprints.exts import db
from werkzeug.security import generate_password_hash, check_password_hash
from Model import UserModel, registerForm, captchaModel, unameCheck,usernameCheck

bp = Blueprint("user", __name__, url_prefix="/user")


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
                    db.session.commit()
                    return {"name": ["注册成功!用户名:" + na]}
                else:
                    return {"captcha": ["验证码过期,请重新获取验证码"]}
            else:
                return {"captcha": ["验证码错误"]}
        else:
            return form.errors


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
                    if len(form.to_dict()['password'])>16 or len(form.to_dict()['password'])<6:
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

