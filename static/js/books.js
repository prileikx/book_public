$(document).ready(function () {
    admin_btn = $("#admin_btn")
    if_fav = $("#if_fav")
    fav_book = $("#fav_book")
    pre_borrow = $("#pre_borrow")
    appointment_book = $("#appointment_book")
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
    $.post('/library/check_book_is_pre_borrow',{
        bid:$("#bid").text()
    },function (res) {
        if(res.status[0]==200){
            appointment_book.text("预约图书")
            appointment_book.removeClass("hidden")
        }
        else if(res.status[0]==201){
            appointment_book.text("取消预约")
            appointment_book.removeClass("hidden")
                                    pre_borrow.text('于' + res.appointment_time[0] + "预约此书")
                        pre_borrow.removeClass("hidden")
        }
        else if(res.status[0]==502){
            appointment_book.text("您已借阅该图书,请按时归还")
            appointment_book.attr("disabled","disabled")
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
                confirmButtonText: '删除!'
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
            appointment_book.click(function () {
            if (appointment_book.text() == "取消预约") {
                Swal.fire({
                    title: '是否确定取消预约?',
                    type: 'warning',
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonColor: '#3085d6',
                    cancelButtonColor: '#d33',
                    confirmButtonText: '取消预约'
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
                            showConfirmButton: false,
                            timer: 1000
                        })
                        appointment_book.text('取消预约')
                        pre_borrow.text('于' + res.appointment_time[0] + "预约此书")
                        pre_borrow.removeClass("hidden")
                    } else if (res.status[0] !=200) {
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
})