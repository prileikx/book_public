$(document).ready(function () {
    // 发送登录信息
    $("button#loginbtn").click(function () {
            $.post("/user/login",
                {
                    uname_login: $("[name='uname_login']").val(),
                    pwd_login: $("[name='pwd_login']").val(),
                    remember_me: $("[name='remember_me']").prop("checked")
                },
                function (message) {
                    if (message.status == 200) {
                        //设置uid cookie
                        $.post("/api/set_uid_cookie", {
                                uid: message.uid[0],
                                username: message.username[0]
                            }
                        )
                        //设置session
                        $.post("/api/set_login_session", {
                                uid: message.uid[0],
                                ifsave: message.ifsave[0]
                            }
                        )
                        Swal.fire({
                            type: 'success',
                            icon:'success',
                            title: message.message,
                            showConfirmButton: false,
                            timer: 1000
                        })//1秒后跳转到主页
                        setTimeout("window.location.href='/homepage'", 1000)
                    } else {
                        Swal.fire({
                            position: 'top-end',
                            type: 'error',
                            icon:'error',
                            title: message.message,
                            showConfirmButton: false,
                            timer: 1500
                        })
                    }
                    // warn = $("#warn")
                    // warn.text(message.message)
                    // //滑动下滑
                    // warn.slideToggle("slow")
                    // //滑动下滑3秒后收起
                    // setTimeout('$("#warn").slideToggle("slow")', 3000)

                }
            )

        }
    )
})