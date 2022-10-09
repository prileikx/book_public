var time = 60
var btndisable = function () {
    if (time == 0) {
        clearInterval(btn_inv)
        $("button#sd_em").removeAttr("disabled");
        $("button#sd_em").text("获取验证码")
        time = 60
        return
    }
    var tex = "获取验证码(" + time + ")"
    $("button#sd_em").text(tex)
    time = time - 1
}
$(document).ready(function () {
    $("#sd_em").click(function () {
        $("button#sd_em").attr("disabled", "true")
        btn_inv = setInterval("btndisable()", 1000)
        $.post("/api/send_change_password_email", {
            name: $("[name='name']").val()
        }, function (response) {
            // warn = $("#warn")
            // warn.text(response.message)
            // //滑动下滑
            // warn.slideToggle("slow")
            // //滑动下滑3秒后收起
            // setTimeout('$("#warn").slideToggle("slow")', 3000)
            Swal.fire({
                type: 'info',
                icon: 'info',
                title: response.message,
                showConfirmButton: false,
                timer: 1500
            })
        })
    })
    $("#change_password").click(function () {
        $.post("/user/change_password", {
            name: $("[name='name']").val(),
            captcha: $("[name='captcha']").val(),
            password: $("[name='pwd']").val()
        }, function (response) {
            // warn = $("#warn")
            // warn.text(response.message)
            // //滑动下滑
            // warn.slideToggle("slow")
            // //滑动下滑3秒后收起
            // setTimeout('$("#warn").slideToggle("slow")', 3000)
            Swal.fire({
                type: 'info',
                icon: 'info',
                title: response.message,
                showConfirmButton: false,
                timer: 1500
            })
        })
    })
})