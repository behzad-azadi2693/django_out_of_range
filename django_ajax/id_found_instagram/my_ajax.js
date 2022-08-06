$('#search_username').keyup(function(e){
    var name = $('#search_username').val()
    if( name.length > 4 ){
        $.ajax({
            url: "{% url 'search_username' %}",
            type: 'GET',
            data: {value:$('#search_username').val()},
            dataType:'json',

            success: function(response){
                var instance =JSON.parse(response['datas']);
                for(var i=0; i < instance.length; i++){
                        var fields = instance[i]['fields'];
                        $('#show_users').html("").removeClass();
                        $('#show_users').prepend(
                            `
                            <p class="text-success col-md-3 ml-3">
                                <a href="{% url 'user_find' name='felds.username' %}">${fields['username']}</a>
                            </p>
                            `
                        )
                }
                console.log(fields);
            },
            error: function(){
                $('#show_users').html("").removeClass();
                $('#show_users').html("nothing found").toggleClass('text-danger col-md-3 ml-3')
            }
        })
    }
});