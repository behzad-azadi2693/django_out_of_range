$('#ajax_search').keyup(function(e){
            var word = $('#ajax_search').val()
            if(word.length > 4){
              setTimeout(() => { 
                $.ajax({
                  url: "{% url 'df:ajax_search' %}",
                  type: 'GET',
                  data: {word:$('#ajax_search').val()},
                  dataType:'json',
                  success: function(response){
                      $('#search_category').html("")
                      for (let i = 0; i < response.datas.length; i++) {
                          url = '/search/'+response.datas[i]+'/'+'?text='+word
                          $('#search_category').prepend(`
                             <p> <a href=${url}> جستجوی ${word} در دسته بندی ${response.datas[i]} </a> </p>
                             <p>frtew','vfgflklm|truncatechars:9</p>
                          `
                          )
                      }
                  },
                  error:function(e){
                            $('#search_category').html("")
                          }
                })
              }, 2000);
            }else{
                $('#search_category').html("")
              }
        })
