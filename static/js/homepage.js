$(document).ready(function () {
    var n
    var show_more = false
    var html = ""
    //返回我的收藏图书列表,加载到主页的我的收藏
    $.ajax({
        url: "/api/my_fav",
        type: "post",
        success: function (res) {
            if (res.status[0] == 200) {
                html = "<table style='width: 550px;'><tr><td style='text-align: center;border-right: 1px solid #c2c2d6;border-bottom: 1px solid #c2c2d6;width: 415px;max-width: 415px;'>书籍名称</td><td style='text-align: center;border-bottom: 1px solid #c2c2d6;width: 134px'>收藏时间</td></tr>"
                n = res.countb[0]
                if (n > 11) {
                    n = 11
                    show_more = true
                }
                for (i = 0; i < n; i++) {
                    if (i % 2 == 0) {
                        html += "<tr style='background-color:#DDDDDD;'>"
                    } else {
                        html += "<tr>"
                    }
                    html += "<td style='text-align: left;width: 415px;max-width: 415px;border-right: 1px solid #c2c2d6;border-bottom: 1px solid #c2c2d6'><a style='color: #0f0f0f;overflow: hidden;' href='/library/books/" + res.book_bid[i] + "'>" + res.book_name[i] + "</a></td><td style='text-align: center;border-bottom: 1px solid #c2c2d6;width: 134px'>" + res.book_fav_time[i] + "</td></tr>"
                }
                if (show_more == true) {
                    html += "<tr><td><a href='/user/account?choose=my_fav&mark=1'>[更多...]</a></td></tr></table>"
                }
                $("#my_fav").html(html)
            } else {
                html = res.message[0]
                $("#my_fav").html(html)
            }
        }

    })
    //返回我的预约图书列表,加载到主页的我的预约
    $.ajax({
        url: "/api/pre_borrow_book_msg",
        type: "post",
        success: function (res) {
            if (res.status[0] == 200) {
                html = "<tr><td style='text-align: center;border-right: 1px solid #c2c2d6;border-bottom: 1px solid #c2c2d6;width: 415px;max-width: 415px;'>书籍名称</td><td style='text-align: center;border-bottom: 1px solid #c2c2d6;width: 134px'>预约时间</td></tr>"
                n = res.countb[0]
                show_more = false
                if (n > 11) {
                    n = 11
                    show_more = true
                }
                for (i = 0; i < n; i++) {
                    if (i % 2 == 0) {
                        html += "<tr style='background-color:#DDDDDD;'>"
                    } else {
                        html += "<tr>"
                    }
                    html += "<td style='text-align: left;width: 415px;border-right: 1px solid #c2c2d6;border-bottom: 1px solid #c2c2d6;max-width: 415px;'><a style='color: #0f0f0f' href='/library/books/" + res.book_bid[i] + "'>" + res.book_name[i] + "</a></td><td style='text-align: center;border-bottom: 1px solid #c2c2d6;width: 134px'>" + res.book_appointtime[i] + "</td></tr>"
                }
                if (show_more == true) {
                    html += "<tr><td><a href='/user/account?choose=my_pre_borrow&mark=1'>[更多...]</a></td></tr>"
                }
                $("#my_pre_borrow").html(html)
            }else {
                html = res.message[0]
                $("#my_pre_borrow").html(html)
            }
        }
    })
        $.ajax({
        url: "/api/my_msg_find",
        type: "post",
        success: function (res) {
            if (res.status[0] == 200) {
                html = ""
                n = res.countb[0]
                show_more = false
                if (n > 11) {
                    n = 11
                    show_more = true
                }
                for (i = 0; i < n; i++) {
                    if (i % 2 == 1) {
                        html += "<tr style='background-color:#DDDDDD;'>"
                    } else {
                        html += "<tr>"
                    }
                    html += "<td style='text-align: left;width: 550px;border-bottom: 1px solid #c2c2d6;max-width: 550px;'>"+res.msg[i]+"</td></tr>"
                }
                if (show_more == true) {
                    html += "<tr><td><a href='/user/account?choose=my_msg&mark=1'>[更多...]</a></td></tr>"
                }
                $("#my_msg").html(html)
            }else {
                html = res.message[0]
                $("#my_msg").html(html)
            }
        }
    })
       $.ajax({
        url: "/api/borrow_book_msg",
        type: "post",
        success: function (res) {
            if (res.status[0] == 200) {
                html = "<tr><td style='text-align: center;border-right: 1px solid #c2c2d6;border-bottom: 1px solid #c2c2d6;width: 415px;max-width: 415px;'>书籍名称</td><td style='text-align: center;border-bottom: 1px solid #c2c2d6;width: 134px'>借阅时间</td></tr>"
                n = res.countb[0]
                show_more = false
                if (n > 11) {
                    n = 11
                    show_more = true
                }
                for (i = 0; i < n; i++) {
                    if (i % 2 == 0) {
                        html += "<tr style='background-color:#DDDDDD;'>"
                    } else {
                        html += "<tr>"
                    }
                    html += "<td style='text-align: left;width: 415px;border-right: 1px solid #c2c2d6;border-bottom: 1px solid #c2c2d6;max-width: 415px;'><a style='color: #0f0f0f' href='/library/books/" + res.book_bid[i] + "'>" + res.book_name[i] + "</a></td><td style='text-align: center;border-bottom: 1px solid #c2c2d6;width: 134px'>" + res.book_borrowtime[i] + "</td></tr>"
                }
                if (show_more == true) {
                    html += "<tr><td><a href='/user/account?choose=my_fav&mark=1'>[更多...]</a></td></tr>"
                }
                $("#my_borrow").html(html)
            }else {
                html = res.message[0]
                $("#my_borrow").html(html)
            }
        }
    })
})