
$(document).ready(function (){

        $.post("/api/check_login_status",{
            toregis:"no",
            webtitle:document.title
        },function (response) {
            if(response.status == "302"){
                window.location.href='/user/login'
            }
            else if(response.status == ""){
                window.location.href='/user/login'
            }

    })

})
