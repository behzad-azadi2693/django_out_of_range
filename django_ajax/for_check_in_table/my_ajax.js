$('#check_username').keyup(function(e){
    var name = $('#check_username').val()
    if( name.length < 5 ){
        $('#msg_check').html('the len character not less of 4').addClass("text-danger")
    }else{
        $.ajax({
            url: "{% url 'check_username' %}",
            type: 'GET',
            data: {value:$('#check_username').val()},
            dataType:'json',

            success: function(response){
                console.log(response);
                if( response['check'] == 'False'){
                    $('#msg_check').removeClass();
                    $('#msg_check').html("this id is ok").addClass('text-success');
                };
                if(response['check'] == 'True'){
                    $('#msg_check').removeClass();
                    $('#msg_check').html("this id is exists").toggleClass('text-danger');
                };
            }
        })
    }
});