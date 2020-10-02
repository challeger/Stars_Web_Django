document.querySelector('.img__btn').addEventListener('click', function () {
    document.querySelector('.content').classList.toggle('s--signup')
});


function check_click(obj_id, time) {
    if (!isNaN(time) && time > 0) {
        let btn = $('#' + obj_id);
        btn.html("倒计时" + time + "秒");
        btn.attr('disabled', true);
        let b = setInterval(function () {
            time--;
            if (time <= 0) {
                btn.html('重新发送');
                btn.attr('disabled', false);
                clearInterval(b);
            } else {
                btn.html("倒计时" + time + "秒");
            }
        }, 1000);
        $.ajax({
            type: 'POST',
            url: '/users/email_register_verify/',
            contentType: 'application/json', //以json格式传数据
            dataType: 'json',
            data: {
                email:'799613500@qq.com',
                csrfmiddlewaretoken:'{{ csrf_token }}'
            },
            success: function (data) {
                
            },
            error: function (e) {
                
            }
        })
    } else {
        alert('时间有误')
    }
}

