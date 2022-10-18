$(document).ready(function () {
    $("#user_msg").click(function () {
        window.location.href = "/user/account?choose=user_msg"
    })
    $("#account_manage").click(function () {
        window.location.href = "/user/account?choose=account_manage"
    })
    $("#my_fav").click(function () {
        window.location.href = "/user/account?choose=my_fav"
    })
    $("#my_pre_borrow").click(function () {
        window.location.href = "/user/account?choose=my_pre_borrow"
    })
    $("#my_borrow").click(function () {
        window.location.href = "/user/account?choose=my_borrow"
    })
    $("#my_msg").click(function () {
        window.location.href = "/user/account?choose=my_msg"
    })
    $("#change_username_btn").click(function () {
        Swal.fire({
            title: '修改用户名',
            html: `
            <form method="post" id="up1">
            <label>输入密码:
            <input type="password" name="password_confirm" id="password_confirm" form="up1">
            </label>
            <label>输入用户名:
            <input type="text" name="change_uname_text" id="change_uname_text" form="up1">
            </label>
            </form>
            `,
            showCancelButton: true,
            showConfirmButton: true,
            confirmButtonText: '修改',
            cancelButtonText: "取消",
            preConfirm: function () {
                return new Promise((resolve, reject) => {
                    resolve({
                        pwd: $("#password_confirm").val(),
                        uname_text: $("[name='change_uname_text']")
                    })
                })
            },
        }).then((res) => {
            if (res.value) {
                let formDateObj = new FormData();
                formDateObj.append('pwd', $("#password_confirm").val())
                formDateObj.append('uname_text', $("#change_uname_text").val())
                $.ajax({
                    url: '/user/change_uname',
                    type: 'post',
                    data: formDateObj,
                    contentType: false,
                    processData: false,
                    success: function (response) {
                        if (response.status[0] == 200) {
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

                    },
                    error: function () {
                        Swal.fire(
                            {
                                type: 'error',
                                icon: 'error',
                                title: "请求发送失败",
                                showConfirmButton: false,
                                timer: 2000
                            }
                        )
                    }
                })
            }
        })
    })
    $("#change_password_btn").click(function () {
        Swal.fire({
            title: '修改用户名',
            html: `
            <form method="post" id="up1">
            <label>输入原密码:
            <input type="password" name="password_confirm" id="ori_pwd" form="up1">
            </label>
            <label>输入新密码:
            <input type="password" name="change_uname_text" id="change_pwd" form="up1">
            </label>
            </form>
            `,
            showCancelButton: true,
            showConfirmButton: true,
            confirmButtonText: '修改',
            cancelButtonText: "取消",
            preConfirm: function () {
                return new Promise((resolve, reject) => {
                    resolve({
                        origin_pwd: $("#ori_pwd").val(),
                        change_pwd: $("#change_pwd").val()
                    })
                })
            },
        }).then((res) => {
            if (res.value) {
                let formDateObj = new FormData();
                formDateObj.append('origin_pwd', $("#ori_pwd").val())
                formDateObj.append('change_pwd', $("#change_pwd").val())
                $.ajax({
                    url: '/user/change_pwd_know_pwd',
                    type: 'post',
                    data: formDateObj,
                    contentType: false,
                    processData: false,
                    success: function (response) {
                        if (response.status[0] == 200) {
                            setTimeout("window.location.href='/user/login'", 1000)
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

                    },
                    error: function () {
                        Swal.fire(
                            {
                                type: 'error',
                                icon: 'error',
                                title: "请求发送失败",
                                showConfirmButton: false,
                                timer: 2000
                            }
                        )
                    }
                })
            }
        })
    })
    $("#change_email_btn").click(function () {
                Swal.fire({
            title: '发送验证码',
            html: `
            <form method="post" id="up1">
            <label>输入新邮箱:
            <input type="text" name="password_confirm" id="new_email_send" form="up1">
            </label>
            `,
            showCancelButton: true,
            showConfirmButton: true,
            confirmButtonText: '修改',
            cancelButtonText: "取消",
            preConfirm: function () {
                return new Promise((resolve, reject) => {
                    resolve({
                        origin_pwd: $("#ori_pwd").val(),
                        change_pwd: $("#change_pwd").val()
                    })
                })
            },
        }).then((res) => {
            if (res.value) {
                let formDateObj = new FormData();
                                    formDateObj.append('new_email_send', $("#new_email_send").val())
                $.ajax({
                    url: '/api/send_email_for_change_email',
                    type: 'post',
                                        data: formDateObj,
                    contentType: false,
                    processData: false,
                    success: function (response) {
                        if (response.status[0] == 200) {
                            Swal.fire({
                                title: '修改邮箱',
                                html: `
            <form method="post" id="up1">
            <label>邮箱验证码:
            <input type="text" name="password_confirm" id="captcha_for_change_email" form="up1">
            </label>
            </form>
            `,
                                showCancelButton: true,
                                showConfirmButton: true,
                                confirmButtonText: '修改',
                                cancelButtonText: "取消",
                                preConfirm: function () {
                                    return new Promise((resolve, reject) => {
                                        resolve({
                                            captcha_for_change_email: $("#captcha_for_change_email").val(),
                                        })
                                    })
                                },
                            }).then((res) => {
                                if (res.value) {
                                    let formDateObj = new FormData();
                                    formDateObj.append('captcha_for_change_email', $("#captcha_for_change_email").val())
                                    $.ajax({
                                        url: '/user/change_email',
                                        type: 'post',
                                        data: formDateObj,
                                        contentType: false,
                                        processData: false,
                                        success: function (response) {
                                            if (response.status[0] == 200) {
                                                setTimeout("window.location.href='/user/login'", 1000)
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

                                        },
                                        error: function () {
                                            Swal.fire(
                                                {
                                                    type: 'error',
                                                    icon: 'error',
                                                    title: "请求发送失败",
                                                    showConfirmButton: false,
                                                    timer: 2000
                                                }
                                            )
                                        }
                                    })
                                }
                            })
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

                    },
                    error: function () {
                        Swal.fire(
                            {
                                type: 'error',
                                icon: 'error',
                                title: "请求发送失败",
                                showConfirmButton: false,
                                timer: 2000
                            }
                        )
                    }
                })
            }})
    })
})