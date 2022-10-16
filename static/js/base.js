$(document).ready(function () {

    $.post("/api/check_login_status", {
        toregis: "no",
        webtitle: document.title
    }, function (response) {
        if (response.status == "302") {
            swal.fire({
                title: "用户验证错误或尚未登录,请重新登录",
                icon: 'error',
                type: 'error',
                allowOutsideClick: false,
            }).then((res) => {
                if (res.value) {
                    window.document.location = '/user/login'
                }
            })
            $('#logre').show()
        } else if (response.status == "303") {
            window.location.href = '/user/change_password'
        } else if (response.status == "200") {
            $('#logmsg').show()
            $.ajax({
                url: '/user/query_uname',
                type: 'post',
                success: function (res) {
                    if (res.status[0] == 200) {
                        $('#username').text(res.uname[0])
                    } else {
                        swal.fire({
                            title: "用户名验证错误,请重新登录",
                            icon: 'error',
                            type: 'error',
                            allowOutsideClick: false,
                        }).then((res) => {
                            if (res.value) {
                                window.document.location = '/user/login'
                            }
                        })
                    }
                }
            })

        } else {
            $('#logre').show()
        }

    })
    $("#logout").click(function () {
            $.post("/api/del_session", {}, function () {
                    window.location.href = '/user/login'
                }
            )
        }
    )
})
