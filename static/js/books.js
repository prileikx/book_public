$(document).ready(function () {
    admin_btn = $("#admin_btn")
    if_fav = $("#if_fav")
    fav_book = $("#fav_book")
    pre_borrow = $("#pre_borrow")
    appointment_book = $("#appointment_book")
    edit_book_btn = $("#edit_book_btn")
    edit_photo_btn = $("#edit_photo_btn")
    borrow_book_btn = $("#borrow_book_btn")
    del_book_btn = $("#del_book_btn")
    book_edit_empty = $("#book_edit_empty")
    edit_book_save_btn = $("#edit_book_save_btn")
    bid = $("#bid").text()
    var uname = []
    borrow_table = $("#borrow_table")
    $.post('/api/check_admin', {}, function (res) {
        if (res.status[0] == 200) {
            admin_btn.removeClass("hidden")
        }
    })
    $.post('/library/check_book_is_fav', {
        bid: $("#bid").text()
    }, function (res) {
        if (res.status[0] == 200) {
            fav_book.text('取消收藏')
            fav_book.removeClass("hidden")
            if_fav.text('于' + res.fav_time[0] + "收藏此书")
            if_fav.removeClass("hidden")
        } else {
            fav_book.text('收藏图书')
            fav_book.removeClass("hidden")
        }
    })
    $.post('/library/check_book_is_pre_borrow', {
        bid: $("#bid").text()
    }, function (res) {
        if (res.status[0] == 200) {
            appointment_book.text("预约图书")
            appointment_book.removeClass("hidden")
        } else if (res.status[0] == 201) {
            appointment_book.text("取消预约")
            appointment_book.removeClass("hidden")
            pre_borrow.text('于' + res.appointment_time[0] + "预约此书")
            pre_borrow.removeClass("hidden")
        } else if (res.status[0] == 502) {
            appointment_book.text("您已借阅该图书,请按时归还")
            appointment_book.attr("disabled", "disabled")
            appointment_book.removeClass("hidden")
        }

    })
    fav_book.click(function () {
        if (fav_book.text() == "取消收藏") {
            Swal.fire({
                title: '是否确定取消收藏?',
                type: 'warning',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: '取消收藏',
                cancelButtonText: "关闭"
            }).then((result) => {
                if (result.value) {
                    $.post('/library/cancel_fav', {
                        bid: $("#bid").text()
                    }, function (res) {
                        if (res.status[0] == 200) {
                            Swal.fire(
                                res.message[0]
                            )
                            fav_book.text('收藏图书')
                            if_fav.text("")
                            if_fav.addClass("hidden")
                        } else if (res.status[0] == 502) {

                            Swal.fire(
                                {
                                    type: 'error',
                                    icon: 'error',
                                    title: res.message,
                                    showConfirmButton: false,
                                    timer: 2000
                                }
                            )
                        }

                    })

                }
            })

        } else if (fav_book.text() == "收藏图书") {
            $.post('/library/add_fav', {
                bid: $("#bid").text()
            }, function (res) {
                if (res.status[0] == 200) {
                    Swal.fire({
                        type: 'success',
                        icon: 'success',
                        title: res.message[0],
                        showConfirmButton: false,
                        timer: 1000
                    })
                    fav_book.text('取消收藏')
                    if_fav.text('于' + res.fav_time[0] + "收藏此书")
                    if_fav.removeClass("hidden")
                } else if (res.status[0] != 200) {
                    Swal.fire(
                        {
                            type: 'error',
                            icon: 'error',
                            title: res.message,
                            showConfirmButton: false,
                            timer: 2000
                        }
                    )
                }

            })
        }

    })
    appointment_book.click(function () {
        if (appointment_book.text() == "取消预约") {
            Swal.fire({
                title: '是否确定取消预约?',
                type: 'warning',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: '取消预约',
                cancelButtonText: "关闭"
            }).then((result) => {
                if (result.value) {
                    $.post('/library/cancel_pre_borrow', {
                        bid: $("#bid").text()
                    }, function (res) {
                        if (res.status[0] == 200) {
                            Swal.fire(
                                res.message[0]
                            )
                            appointment_book.text('预约图书')
                            pre_borrow.text("")
                            pre_borrow.addClass("hidden")
                        } else if (res.status[0] != 200) {
                            Swal.fire(
                                {
                                    type: 'error',
                                    icon: 'error',
                                    title: res.message,
                                    showConfirmButton: false,
                                    timer: 2000
                                }
                            )
                        }

                    })

                }
            })

        } else if (appointment_book.text() == "预约图书") {
            $.post('/library/add_pre_borrow', {
                bid: $("#bid").text()
            }, function (res) {
                if (res.status[0] == 200) {
                    Swal.fire({
                        type: 'success',
                        icon: 'success',
                        title: res.message[0],
                    })
                    appointment_book.text('取消预约')
                    pre_borrow.text('于' + res.appointment_time[0] + "预约此书")
                    pre_borrow.removeClass("hidden")
                } else if (res.status[0] != 200) {
                    Swal.fire(
                        {
                            type: 'error',
                            icon: 'error',
                            title: res.message,
                        }
                    )
                }

            })
        }
    })
    edit_book_btn.click(function () {
        $("#photo").addClass("hidden")
        $("#book_msg").addClass("hidden")
        $("#book_edit_div").removeClass("hidden")
    })
    $("#cancel_edit_book_btn").click(function () {
        location.reload(true)//设置为true为强制从服务器加载,可以不写
    })
    edit_book_save_btn.click(function () {
        $.post('/library/edit_book', {
            bid: $("#bid").text(),
            bname: $("[name='bname_edit']").val(),
            author: $("[name='author_edit']").val(),
            press: $("[name='press_edit']").val(),
            isbn_code: $("[name='isbn_code_edit']").val(),
            book_class: $("[name='book_class_edit']").val(),
            price: $("[name='price_edit']").val(),
            number: $("[name='number_edit']").val(),
            Issue_date: $("[name='Issue_date_edit']").val(),
            introduce: $("[name='introduce_edit']").val(),
        }, function (res) {
            if (res.status[0] == 200) {
                setTimeout("location.reload(true)", 1000)
                Swal.fire({
                    type: 'success',
                    icon: 'success',
                    title: res.message[0],
                    showConfirmButton: false,
                    timer: 1000
                })
            } else {
                Swal.fire({
                    type: 'error',
                    icon: 'error',
                    title: res.message[0],
                    showConfirmButton: false,
                    timer: 1000
                })
            }
        })
    })
    del_book_btn.click(function () {
        Swal.fire({
            title: '是否确定删除图书?删除后不可恢复',
            type: 'warning',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#3085d6',
            confirmButtonText: '删除',
            cancelButtonText: "不删除"
        }).then((result) => {
            if (result.value) {
                $.post('/library/del_book', {
                    bid: $("#bid").text()
                }, function (res) {
                    if (res.status[0] == 200) {
                        Swal.fire(
                            res.message[0]
                        )
                        setTimeout("location.reload(true)", 2000)
                    } else if (res.status[0] != 200) {
                        setTimeout("location.reload(true)", 2000)
                        Swal.fire(
                            {
                                type: 'error',
                                icon: 'error',
                                title: res.message[0],
                                showConfirmButton: false,
                                timer: 2000
                            }
                        )
                    }

                })

            }
        })

    })
    edit_photo_btn.click(function () {
        Swal.fire({
            title: '上传图片',
            html: `
            <form method="post" action="/library/up_book_photo" enctype="multipart/form-data" id="up1">
            <img src="#" id="pre_photo" class="hidden">
            <input type="file" name="photo" id="up_photo" form="up1" accept=".png">
<!--            <button type="submit" class="btn btn-sm btn-success" style="margin-top: 5px" form="up2" id="up_photo_btn">上传图片</button>-->
            </form>
            `,
            showCancelButton: true,
            showConfirmButton: true,
            confirmButtonText: '上传图片',
            cancelButtonText: "关闭",
            preConfirm: function () {
                return new Promise((resolve, reject) => {
                    resolve({
                        bid: bid,
                        photo: $("[name='photo']")
                    })
                })
            },
        }).then((res) => {
            if (res.value) {
                let formDateObj = new FormData();
                formDateObj.append('bid', bid)
                formDateObj.append('photo', $("#up_photo")[0].files[0])//获取文件详情
                $.ajax({
                    url: '/library/up_book_photo',
                    type: 'post',
                    data: formDateObj,
                    contentType: false,
                    processData: false,
                    success: function (response) {
                        setTimeout("location.reload(true)", 1000)
                        Swal.fire(
                            {
                                type: 'success',
                                icon: 'success',
                                title: response.message[0],
                                showConfirmButton: false,
                                timer: 2000
                            }
                        )
                    }
                })
            }
        })
    })
    borrow_book_btn.click(function () {
        Swal.fire({
            title: '请输入借阅人',
            html: `
            <form method="post" οnsubmit="return false;" action="/library/add_borrow_book" enctype="multipart/form-data" id="up5">
            <input type="text" name="uname" id="uname" onkeydown="if(event.keyCode == 13){return false;}" form="up5">
<!--            <button type="submit" class="btn btn-sm btn-success" style="margin-top: 5px" form="up2" id="up_photo_btn">上传图片</button>-->
            </form>
            `,
            showCancelButton: true,
            showConfirmButton: true,
            confirmButtonText: '确定',
            cancelButtonText: "取消",
            allowEnterKey:false,
            preConfirm: function () {
                return new Promise((resolve, reject) => {
                    resolve({
                        bid: bid,
                        photo: $("[name='photo']")
                    })
                })
            },
        }).then((res) => {
            if (res.value) {
                let formDateObj = new FormData();
                formDateObj.append('bid', $("#bid").text())
                formDateObj.append('uname', $("#uname").val())
                $.ajax({
                    url: '/library/add_borrow_book',
                    type: 'post',
                    data: formDateObj,
                    contentType: false,
                    processData: false,
                    success: function (response) {
                        if (response.status[0] == 200) {
                            Swal.fire(
                                {
                                    type: 'success',
                                    icon: 'success',
                                    title: response.message[0],
                                    showConfirmButton: false,
                                    timer: 2000
                                }
                            )
                        } else {
                            Swal.fire(
                                {
                                    type: 'error',
                                    icon: 'error',
                                    title: response.message[0],
                                    showConfirmButton: false,
                                    timer: 2000
                                }
                            )
                        }

                    }
                })
            }

        })
    })
    //归还图书按钮
    $("#back_book_btn").click(function () {
        $.post('/library/borrow_book_msg',{
            bid:bid
        },function (res) {
            uname = []
            html = "<tr><td>用户</td><td>预约时间</td><td>借阅时间</td><td>归还时间</td><td>操作</td></tr>"
            for(i=0;i<res.list_number[0];i++)
            {
                uname.push(res.book_user[0][i])
                if(i%2==1){
                    html+="<tr style='background-color:#DDDDDD;'>"
                }
                else{
                    html+="<tr>"
                }
                html+="<td>"+res.book_user[0][i]+"</td><td>"+res.book_appointtime[0][i]+"</td><td>"+res.book_borrowtime[0][i]+"</td><td>"+res.book_back_time[0][i]+"</td><td>"
                if(res.book_status[0][i]==2){
                    html+="<button class='back_book_btn_con'>归还图书</button></td></tr>"
                }
                else {
                    html+="</td></tr>"
                }

            }
            borrow_table.html("")
            borrow_table.append(html)
                borrow_table.toggle()

        })

    })
        $(document).on('click',".back_book_btn_con",function () {
            Swal.fire({
            title: '你确定要归还'+uname[$(".back_book_btn_con").index(this)]+'的借阅吗?',
            showCancelButton: true,
            showConfirmButton: true,
            confirmButtonText: '确定',
            cancelButtonText: "取消",
            allowEnterKey:false,
        }).then((res) => {
            if (res.value) {
                let formDateObj = new FormData();
                formDateObj.append('bid', $("#bid").text())
                formDateObj.append('uname', uname[$(".back_book_btn_con").index(this)])
                $.ajax({
                    url: '/library/back_book',
                    type: 'post',
                    data: formDateObj,
                    contentType: false,
                    processData: false,
                    success: function (response) {
                        if (response.status[0] == 200) {
                            Swal.fire(
                                {
                                    type: 'success',
                                    icon: 'success',
                                    title: response.message[0],
                                    showConfirmButton: false,
                                    timer: 2000
                                }
                            )
                        } else {
                            Swal.fire(
                                {
                                    type: 'error',
                                    icon: 'error',
                                    title: response.message[0],
                                    showConfirmButton: false,
                                    timer: 2000
                                }
                            )
                        }

                    }
                })
            }

        })
        })

})