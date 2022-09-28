
//用于按钮的禁用与启用和按钮倒计时
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
$(document).ready(function (){

    $("button#sd_em").click(function (){


            //发送邮件并接收返回信息
            $("button#sd_em").attr("disabled", "true")
            btn_inv=setInterval("btndisable()",1000)
            $.post("/api/send_email",
                {
                    email:$("[name='email']").val()
                },
                function (status){
                    $("#warn").text(status.email)
                    $("#warn").slideToggle("slow")
                    setTimeout('$("#warn").slideToggle("slow")',3000)
                }
                )

        }
    )
    // 发送注册信息
    $("button#regisbtn").click(function (){
            $.post("/user/register",
                {
                    name:$("[name='name']").val(),
                    email:$("[name='email']").val(),
                    captcha:$("[name='captcha']").val(),
                    pwd:$("[name='pwd']").val(),
                    confirm:$("[name='confirm']").val()
                },
                function (status){
                var message="注册成功"
                if(status.confirm!=undefined)
                    message=status.confirm
                if(status.pwd!=undefined)
                    message=status.pwd
                if(status.captcha!=undefined)
                    message=status.captcha
                if(status.email!=undefined)
                    message=status.email
                if(status.name!=undefined)
                    message=status.name
                $("#warn").text(message)
                    $("#warn").slideToggle("slow")
                    setTimeout('$("#warn").slideToggle("slow")',3000)
                }
                )

        }
    )
    }

)