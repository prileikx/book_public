import datetime
from config import img_path
from api import check_user_limits, generate_photo, check_user_is_true
from flask import Blueprint, request, render_template, session
from Model import book_list, UserModel, book_list_Form, book_favourite, book_borrow
from blueprints.exts import db
from sqlalchemy import and_
import decimal

bp = Blueprint("library", __name__, url_prefix="/library")


# 返回对应图书
@bp.route("/books/<int:bid>")
def books_bid(bid):
    book_object = db.session.query(book_list).filter(book_list.bid == bid)
    if (book_object.first() == None):
        psrc = "/static/upload/books/img/" + "0.png"
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
        psrc = "/static/upload/books/img/" + str(bid) + ".png"
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


# GET返回library,POST获取书库列表
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
        page_size = 10
        if (user != None):
            if (user.first().limits >= 10):
                books = db.session.query(book_list).limit(10).offset((page) * page_size)
                start = page * page_size
                # 数据库中图书的总条目数
                count_book = db.session.query(book_list).count()
                bid_list = []
                bname_list = []
                last_book = 0
                for book in books.all():
                    bid_list.append(book.bid - 1)
                    bname_list.append(book.bname)
                    last_book = last_book + 1
                response = {
                    "status": [200],
                    "count_book": [count_book],
                    "last_book": [last_book],
                    "page_now": [page],
                    "bid": bid_list,
                    "bname": bname_list
                }
        return response


# 添加图书
@bp.route("/add_book", methods=['GET', 'POST'])
def add_book():
    if request.method == 'GET':
        return render_template('/add_book.html')
    else:
        check = check_user_limits(request.cookies.get('uid'), session['verify'], 100)
        if (check == 200):
            form = request.form
            book = book_list_Form(request.form)
            if book.validate():
                bname = form['bname']
                author = form['author']
                press = form['press']
                isbn_code = form['isbn_code']
                book_class = form['book_class']
                price = float(form['price'])
                number = int(form['number'])
                Issue_date = form['Issue_date']
                introduce = form['introduce']
                new_book = book_list(bname=bname, author=author, press=press, isbn_code=isbn_code,
                                     book_class=book_class,
                                     price=price, number=number, Issue_date=Issue_date, introduce=introduce)
                db.session.add(new_book)
                db.session.commit()
                bid = db.session.query(book_list).filter(book_list.isbn_code == isbn_code).first().bid
                generate_photo(bname, str(bid))
                return {"status": [200], "message": ["图书添加成功"]}
            err = str(book.errors)
            return {"status": [520], "message": [err]}
        return {"status": [502], "message": ["用户权限不足"]}


# 检查图书是否为收藏状态
@bp.route("/check_book_is_fav", methods=['POST'])
def check_book_is_fav():
    form = request.form
    uid = request.cookies.get('uid')
    result = db.session.query(book_favourite).filter(
        and_(book_favourite.uid == uid, book_favourite.bid == form['bid'])).first()
    if (result == None):
        return {"status": [404]}
    else:
        return {"status": [200], "fav_time": [result.fav_time.strftime("%Y/%m/%d, %H:%M:%S")]}


# 取消收藏
@bp.route("/cancel_fav", methods=['POST'])
def cancel_fav():
    form = request.form
    uid = request.cookies.get("uid")
    check = check_user_is_true(uid, session.get('verify'))
    if check == 200:
        db.session.query(book_favourite).filter(
            and_(book_favourite.uid == uid, book_favourite.bid == form['bid'])).delete()
        db.session.commit()
        db.session.close()
        return {"status": [200], "message": ["已取消收藏"]}
    return {"status": [502], "message": [check]}


# 添加收藏
@bp.route("/add_fav", methods=['POST'])
def add_fav():
    form = request.form
    uid = request.cookies.get("uid")
    check = check_user_is_true(uid, session.get('verify'))
    fav_time = datetime.datetime.now()
    print(check)
    if check == 200:
        bid = form['bid']
        if db.session.query(book_list).filter(book_list.bid == bid).first() != None:
            fav = book_favourite(uid=uid, bid=form['bid'], fav_time=fav_time)
            db.session.add(fav)
            db.session.commit()
            db.session.close()
            return {"status": [200], "message": ["已添加收藏"], "fav_time": [fav_time.strftime("%Y/%m/%d, %H:%M:%S")]}
        else:
            return {"status": [404], "message": ["该书不存在"]}
    return {"status": [502], "message": [check]}


# 预约图书
@bp.route("/add_pre_borrow", methods=['POST'])
def add_pre_borrow():
    form = request.form
    uid = request.cookies.get('uid')
    bid = form['bid']
    check = check_user_is_true(uid, session.get('verify'))
    appointment_time = datetime.datetime.now()
    if (check == 200):
        borrow_msg = db.session.query(book_borrow).filter(and_(book_borrow.uid == uid, book_borrow.bid == bid)).first()
        if borrow_msg == None:
            book = db.session.query(book_list).filter(book_list.bid == bid).first()
            if (book == None):
                return {"status": [503], "message": ["该书不存在"]}
            else:
                if book.number <= 0:
                    return {"status": [504], "message": ["书籍无剩余"]}
                else:
                    book.number = book.number - 1
                    bbrow = book_borrow(uid=uid, bid=bid, book_status=1, appointment_time=appointment_time)
                    db.session.add(bbrow)
                    db.session.commit()
                    db.session.close()
                    return {"status": [200], "message": ["成功预约图书,预约有效期为3天,请及时去图书馆借阅"],
                            "appointment_time": [appointment_time.strftime("%Y/%m/%d, %H:%M:%S")]}
        else:
            if borrow_msg.book_status == 2:
                return {"status": [505], "message": ["该书已被您借阅"]}
            elif borrow_msg.book_status == 0:
                book = db.session.query(book_list).filter(book_list.bid == bid).first()
                if (book == None):
                    return {"status": [503], "message": ["该书不存在"]}
                else:
                    if book.number <= 0:
                        return {"status": [504], "message": ["书籍无剩余"]}
                    else:
                        book.number = book.number - 1
                        borrow_msg.appointment_time = appointment_time
                        borrow_msg.book_status = 1
                        db.session.commit()
                        db.session.close()
                        return {"status": [200], "message": ["成功预约图书"],
                                "appointment_time": [appointment_time.strftime("%Y/%m/%d, %H:%M:%S")]}
            elif borrow_msg.book_status == 1:
                if (datetime.datetime.now() - borrow_msg.appointment_time).total_seconds() < 60 * 60 * 24 * 3:
                    return {"status": [506], "message": ["您已预约过该图书"]}
                else:
                    book = db.session.query(book_list).filter(book_list.bid == bid).first()
                    if (book == None):
                        return {"status": [503], "message": ["该书不存在"]}
                    else:
                        if book.number <= 0:
                            return {"status": [504], "message": ["书籍无剩余"]}
                        else:
                            book.number = book.number - 1
                            borrow_msg.appointment_time = appointment_time
                            borrow_msg.book_status = 1
                            db.session.commit()
                            db.session.close()
                            return {"status": [200], "message": ["成功预约图书"],
                                    "appointment_time": [appointment_time.strftime("%Y/%m/%d, %H:%M:%S")]}
    else:
        return {"status": [502], "message": [check]}


# 检查图书是否被预约
@bp.route("/check_book_is_pre_borrow", methods=['POST'])
def check_book_is_pre_borrow():
    form = request.form
    uid = request.cookies.get('uid')
    bid = form['bid']
    borrow_msg = db.session.query(book_borrow).filter(and_(book_borrow.uid == uid, book_borrow.bid == bid)).first()
    if (borrow_msg == None):
        return {"status": [200]}
    elif (borrow_msg.book_status == 1 and (
            datetime.datetime.now() - borrow_msg.appointment_time).total_seconds() > 60 * 60 * 24 * 3):
        book = db.session.query(book_list).filter(book_list.bid == bid).first()
        if (book == None):
            return {"status": [404]}
        else:
            book.number = book.number + 1
            db.session.query(book_borrow).filter(and_(book_borrow.uid == uid, book_borrow.bid == bid)).delete()
            db.session.commit()
            db.session.close()
            return {"status": [200]}
    elif (borrow_msg.book_status == 1 and (
            datetime.datetime.now() - borrow_msg.appointment_time).total_seconds() <= 60 * 60 * 24 * 3):
        return {"status": [201], "appointment_time": [borrow_msg.appointment_time.strftime("%Y/%m/%d, %H:%M:%S")]}
    elif borrow_msg.book_status == 0:
        return {"status": [200]}
    elif borrow_msg.book_status == 2:
        return {"status": [502]}


# 取消预约图书
@bp.route("/cancel_pre_borrow", methods=['POST'])
def cancel_pre_borrow():
    form = request.form
    uid = request.cookies.get('uid')
    bid = form['bid']
    check = check_user_is_true(uid, session.get('verify'))
    if (check == 200):
        borrow_msg = db.session.query(book_borrow).filter(and_(book_borrow.uid == uid, book_borrow.bid == bid)).first()
        if borrow_msg == None:
            return {"status": [404], "message": ["您未预约过此图书"]}
        elif borrow_msg.book_status == 1:
            book = db.session.query(book_list).filter(book_list.bid == bid).first()
            if (book == None):
                return {"status": [405], "message": ["图书不存在"]}
            else:
                book.number = book.number + 1
                if borrow_msg.borrow_time != None:
                    borrow_msg.book_status = 0
                else:
                    db.session.query(book_borrow).filter(and_(book_borrow.uid == uid, book_borrow.bid == bid)).delete()
                db.session.commit()
                db.session.close()
                return {"status": [200], "message": ["成功取消预约"]}
        elif borrow_msg.book_status == 0:
            return {"status": [404], "message": ["您未预约过此图书"]}
        elif borrow_msg.book_status == 2:
            return {"status": [502], "message": ["该图书已被您借阅"]}
        else:
            return {"status": [520], "message": ["未知图书状态,请联系网站管理员"]}

    else:
        return {"status": [502], "message": [check]}


# 删除图书
@bp.route("/del_book", methods=['POST'])
def del_book():
    form = request.form
    uid = request.cookies.get('uid')
    bid = form['bid']
    check = check_user_limits(request.cookies.get('uid'), session['verify'], 100)
    if (check == 200):
        db.session.query(book_list).filter(book_list.bid == bid).delete()
        db.session.commit()
        db.session.close()
        return {"status": [200], "message": ["删除成功"]}
    else:
        return {"status": [502], "message": [check]}


# 保存编辑图书信息
@bp.route("/edit_book", methods=['POST'])
def edit_book():
    form = request.form
    uid = request.cookies.get('uid')
    bid = form['bid']
    check = check_user_limits(request.cookies.get('uid'), session['verify'], 100)
    if (check == 200):
        book = db.session.query(book_list).filter(book_list.bid == bid).first()
        if (book == None):
            return {"status": [404], "message": ["书籍不存在,无法保存编辑"]}
        else:
            book.bname = form['bname']
            book.author = form['author']
            book.price = form['price']
            book.press = form['press']
            book.isbn_code = form['isbn_code']
            book.book_class = form['book_class']
            book.number = form['number']
            book.Issue_date = form['Issue_date']
            book.introduce = form['introduce']
            db.session.commit()
            db.session.close()
            return {"status": [200], "message": ["编辑保存成功"]}
    else:
        return {"status": [502], "message": [check]}


# 修改书籍封面
@bp.route('/up_book_photo', methods=['POST'])
def up_book_photo():
    check = check_user_limits(request.cookies.get('uid'), session['verify'], 100)
    if check == 200:
        img = request.files.get('photo')
        bid = request.form['bid']
        suffix = '.' + img.filename.split('.')[-1]  # 获取文件后缀名
        if suffix == ".png":
            img_save_str_path = img_path + bid + ".png"
            print(bid)
            img.save(img_save_str_path)
            return {"status": [200], "message": ["上传成功"]}
        else:
            return {"status": [502], "message": ["不支持的文件类型,目前仅支持png文件"]}
    else:
        return {"status": [502], "message": [check]}


# 图书借阅信息
@bp.route('/borrow_book_msg', methods=['POST'])
def borrow_book_msg():
    bid = request.form['bid']
    check = check_user_limits(request.cookies.get('uid'), session['verify'], 100)
    if check == 200:
        books = db.session.query(book_borrow).filter(and_(book_borrow.bid == bid, book_borrow.book_status == 2)).all()
        book_appointtime = []
        book_user = []
        book_borrowtime = []
        book_back_time = []
        book_status = []
        list_number = 0
        for book in books:
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
        return {"status": [200], "book_user": [book_user], "book_status": [book_status],
                "book_appointtime": [book_appointtime], "book_borrowtime": [book_borrowtime],
                'book_back_time': [book_back_time], "list_number": [list_number]}
    else:
        return {"status": [502]}


# 添加图书借阅信息
@bp.route('/add_borrow_book', methods=['POST'])
def add_borrow_book():
    bid = request.form['bid']
    uname = request.form['uname']
    print(uname)
    if (uname == ""):
        return {"status": [406], "message": ["请输入用户名"]}
    if uname.isdigit():
        uid = uname
        user = db.session.query(UserModel).filter(UserModel.uid == uid).first()
        if (user == None):
            return {"status": [405], "message": ["无法找到该用户,请检查您的输入是否正确"]}
    elif uname.isalnum():
        user = db.session.query(UserModel).filter(UserModel.name == uname).first()
        if (user == None):
            return {"status": [405], "message": ["无法找到该用户,请检查您的输入是否正确"]}
        else:
            uid = user.uid
    else:
        return {"status": [405], "message": ["无法找到该用户,请检查您的输入是否正确"]}
    check = check_user_limits(request.cookies.get('uid'), session['verify'], 100)
    if check == 200:
        book = db.session.query(book_list).filter(book_list.bid == bid).first()
        book_borrow_msg = db.session.query(book_borrow).filter(
            and_(book_borrow.bid == bid, book_borrow.uid == uid)).first()
        if book == None:
            return {"status": [404], "message": ["书籍不存在,无法借阅"]}
        else:
            if book.number > 0:
                if (book_borrow_msg == None):
                    borrow_time = datetime.datetime.now()
                    bor_book = book_borrow(uid=uid, bid=bid, book_status=2, borrow_time=borrow_time)
                    book.number = book.number - 1
                    db.session.add(bor_book)
                    db.session.commit()
                    db.session.close()
                    return {"status": [200], "message": ["借阅成功"]}
            else:
                return {"status": [503], "message": ["书籍无剩余,无法借阅"]}
        if book_borrow_msg.book_status == 0:
            if book.number > 0:
                borrow_time = datetime.datetime.now()
                book_borrow_msg.book_status = 2
                book_borrow_msg.borrow_time = borrow_time
                book_borrow_msg.back_time = None
                book.number = book.number - 1
                db.session.commit()
                db.session.close()
                return {"status": [200], "message": ["借阅成功"]}
            else:
                return {"status": [503], "message": ["书籍无剩余,无法预约"]}
        elif book_borrow_msg.book_status == 2:
            return {"status": [504], "message": ["您已借阅该图书,不能重复预约"]}
        elif book_borrow_msg.book_status == 1:
            borrow_time = datetime.datetime.now()
            book_borrow_msg.book_status = 2
            book_borrow_msg.borrow_time = borrow_time
            db.session.commit()
            db.session.close()
            return {"status": [200], "message": ["借阅成功"]}
        else:
            return {"status": [520], "message": ["未知图书状态,请联系系统管理员"]}


# 归还图书
@bp.route('/back_book', methods=['POST'])
def back_book():
    form = request.form
    bid = form['bid']
    check = check_user_limits(request.cookies.get('uid'), session['verify'], 100)
    if check == 200:
        uname = form['uname']
        uid = db.session.query(UserModel).filter(UserModel.name == uname).first().uid
        back_time = datetime.datetime.now()
        book = db.session.query(book_list).filter(book_list.bid == bid).first()
        if book == None:
            return {"status": [404], "message": ["该书不存在"]}
        else:
            book_borw_msg = db.session.query(book_borrow).filter(book_borrow.bid == bid).first()
            if book_borw_msg == None:
                return {"status": [404], "message": ["该用户未借阅该书,无需归还"]}
            elif book_borw_msg.book_status == 0 or book_borw_msg.book_status == 1:
                return {"status": [404], "message": ["该用户未借阅该书,无需归还"]}
            else:
                book_borw_msg.book_status = 0
                book_borw_msg.back_time = back_time
                db.session.commit()
                db.session.close()
                return {"status": [200], "message": ["归还成功"]}
    else:
        return {"status": [502], "message": [check]}


