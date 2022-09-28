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
                if (message.status == 200){
                    $.post("/api/set_uid_cookie", {
                            uid: message.uid[0]
                        }
                    )
                    $.post("/api/set_login_session", {
                            username:message.username[0],
                            ifsave: message.ifsave[0]
                        }
                    )
                }
                    warn=$("#warn")
                    warn.text(message.message)
                    warn.slideToggle("slow")
                    setTimeout('$("#warn").slideToggle("slow")', 3000)
                }
            )

        }
    )
})