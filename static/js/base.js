$(document).ready(function () {

    $.post("/api/check_login_status", {
        toregis: "no",
        webtitle: document.title
    }, function (response) {
        if (response.status == "302") {
            window.location.href = '/user/login'
            $('#logre').show()
        }else if(response.status == "303"){
            window.location.href = '/user/change_password'
        }
        else if (response.status == "200") {
            $('#logmsg').show()
            $('#username').text($.cookie('username'))
        } else {
            $('#logre').show()
        }

    })
    $("#logout").click(function () {
        $.post("/api/del_session",{

        },function (){
            window.location.href='/user/login'
            }
        )
        }
    )
})
