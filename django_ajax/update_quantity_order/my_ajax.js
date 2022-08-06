$('button[id^="change_pls_"]').click(function(e){
    var qty_id = '#qty_'+$(this).attr('data-id');
    $.ajax({
        type:'GET',
        url: "{% url 'change_qty_pls' %}",
        data:{key_qty:$(this).attr('data-id')},
        dataType:"json",
        success: function(response){
            $(qty_id).html(response);
        },

        error: function(response){
            alert(response['responseJSON']['error']);
        }
    })
})

$('button[id^="change_mins_"]').click(function(e){
    var qty_id = '#qty_'+$(this).attr('data-id');
    $.ajax({
        type:'GET',
        url: "{% url 'change_qty_mins' %}",
        data:{key_qty:$(this).attr('data-id')},
        dataType:"json",
        success: function(response){
            $(qty_id).html(response);
        },
        
        error: function(response){
            alert(response['responseJSON']['error']);
        }
    })
})