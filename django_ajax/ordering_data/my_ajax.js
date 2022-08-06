        $("#my_aj").click(function(e) {
            $.ajax({
                type: 'GET',
                url: "{% url 'change' %}",
                data: {keyname:$('#my_aj option:selected').val()},
                dataType: 'json',

                success: function(response){
                    $('#my_div').html("");

                    var instance = JSON.parse(response["datas"]);
                    for(var i=0;i<instance.length;i++){
                    var fields = instance[i]['fields'];
                    $('#my_div').prepend(
                    `
                        <p>${fields['name'] }</p>
                        <p>${fields['family']}</p>
                        <p>${fields['price'] }</p>
                        <hr>
                    `);
                    };
                },

                error: function(){
                    alert('Error')
                }

            });
        });
