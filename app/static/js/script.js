$(document).ready(function() {
    var path_name = location.pathname.split('/').slice(1)

   function auth_checker(url, data){
        $.ajax({
            url:url,
            dataType:'json',
            method:'post',
            data:JSON.stringify(data),
            contentType:"application/json, charset=utf-8"

        }).done(function(r) {
            if(r.status == 'fail') {
                $('#message').html(r['errors'])
            }else{
                if (url == '/api/login') { 
                    $('#message').html('<p>Success, redirecting</p>')
                    window.location.href = '/dashboard'
                }else{
                    $('#message').html('<p>Registered, you can <a href="/auth/login" class="text-info">login now</a></p>')
                }
            }
        }
        )
   }
   function get_quiz(code) {
       var result = $.ajax({
           url:'/api/quiz/getQuestion/' + code,
           method: 'get'
       })
       return result 
   }
   
   function make_question(question) {
       var h3 = document.createElement('h3')
       h3.innerHTML = question 
       h3.className = 'mt-3 mb-2 question-title'
       return h3 
   }

   function make_option(option, option_name, value){
       var mt_div = document.createElement('div')
       var label_radio = document.createElement('label')
       var input_radio = document.createElement('input')
       var span = document.createElement('span')

       span.className = 'quiz_option'
       span.innerHTML = option
       
       input_radio.type = 'radio'
       input_radio.name = 'quest_' + option_name
       input_radio.value = value 
       input_radio.className = 'radio_input'
       
       label_radio.className = 'radio'
       mt_div.className = 'mt-2'

       label_radio.appendChild(input_radio)
       label_radio.appendChild(span)
       mt_div.appendChild(label_radio)

       return mt_div

   }
   function make_quiz(json, nums) {
       var content_quiz = document.getElementById('content-quiz');
       var obj_keys = Object.keys(json)
       var data = json[obj_keys[nums]]
       if(data){
            content_quiz.appendChild(make_question(data['question']))
            for(var another_keys in data){
                if (another_keys.endsWith('_option')){
                    var option_tag = make_option(data[another_keys], obj_keys[nums], another_keys.replace('_option',''))
                    content_quiz.appendChild(option_tag)
                    
                }
            }
       }
   }
   $('#register').on('click', function() {
       $('#message').html('<p>registering ...')
       inputs = document.getElementsByTagName('input')
       data_reg = {}
       for(var x=0; x < inputs.length;x ++ ){
           data_reg[
               inputs[x].name
           ] = inputs[x].value
       }
       auth_checker('/api/add-account', data_reg)
       
   })
   $('#login').on('click', function() {
       $('#message').html('Logging in ...')
       data_log = {}
       data_log['username'] = $('#username').val()
       data_log['password'] = $('#password').val()
       auth_checker('/api/login', data_log)

   })
   $('#submitsearch').on('click', function() {
       var search_value = $('#search').val()
       if(search_value.length != 0) {
           var data = {}
           data['search'] = search_value
           $('#messages').html('Loading..')
           $.ajax({
               url:'/api/quiz/search',
               data:JSON.stringify(data),
               contentType:'application/json, charset=utf-8',
               method:'post'
           }).done(function(r) {
               if(r['status'] == 'success') {
                   $('#messages').html('Result : ')
                   for(var i in r['data']) {
                       $('#messages').append('<p>' + r['data'][i] + '</p>')
                   }
               }else{
                   $('#messages').html('No result.')
               }
           })
       } 
   })

   if(path_name.length == 3 && path_name[1] == 'start' && path_name[0] == 'quiz'){
       $('#next').hide()
       var data_quiz = get_quiz(path_name[2])
       data_quiz.done(function(r) {
            if(Object.values(r)[0] == 'failed'){
                $('#content-quiz').html('<h1>Not Found</h1>')
            }else{
                var current = 0;
                $('#next').show()
                $('#next').on('click', function() {
                    var current_nums = current + 1 
                    current = current_nums
                    if(current == Object.keys(r).length -1 ) {
                        $('#next').html('Done')
                    }
                    if(current >= Object.keys(r).length) {
                        $('#next').hide()
                        var answer = $('input[type="radio"]:checked')
                        var data = {}
                        for(var y=0; y < answer.length; y++){
                            data[answer[y].name] = answer[y].value
                        }
                        if(Object.keys(data).length < Object.keys(r).length) {
                            alert('not finished yet!')
                        }else{
                            $.ajax({
                                url:'/api/quiz/nilai/' + path_name[2],
                                method:'post',
                                contentType:'application/json, charset=utf-8',
                                data:JSON.stringify(data)
                            }).done(function(r) {
                                if(r['status'] == 'success') {
                                    var id_result = r['data']['id_result']
                                    $('#content-quiz').html('<h1>Your Score : ' + r['data']['score'])
                                }
                            })
                        }
                        
                    }else{
                            make_quiz(r, current)
                    }
                    })
                    make_quiz(r, current)
                }
        })
   }
   
  

})