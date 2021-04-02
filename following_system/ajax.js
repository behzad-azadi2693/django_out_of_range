$('#following').click(function(){
//csrf_token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});




var to_user_id = $('#following').attr('data-id')
var following_text = $('#following').text()

if(following_text == 'follow'){
    var go_url = '/account/follow/'
    var btn_text = 'unfollow'
    var btn_class = 'btn btn-warning'
}else{
    var go_url = '/account/unfollow/'
    var btn_text = 'follow'
    var btn_class = 'btn btn-primary'
}


    $ajax({
        url: go_url,
        method:'POST',
        data:{
            'user_id': to_user_id,
        },
        success: function(data){
            if(data['status'] == 'ok'){
                $('#following').text(btn_text)
                $('#following').attr({'class':btn_class})

            }
        }
    });
});