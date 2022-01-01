function openNav() {
      document.getElementById("sidebar").style.width = "200px";
      document.getElementById("sidebar").style.backgroundColor = 'white';

}

function closeNav() {
      document.getElementById("sidebar").style.width = "0";
      document.getElementById("main").style.marginLeft= "0";
}

function makeid() {
  var characters = 'abcdefghijklmnopqrstuvwxyz0123456789'
  var result = '';
  for(var x=0;x < 6;x++) {
    result += characters.charAt( 
      Math.random() * characters.length
    )
  }
  return result
}

async function uploadfile() {
  var formdata = new FormData()

  formdata.append('csv',document.getElementById('csv').files[0])
  formdata.append('quiz_title', document.getElementById('quiz_title').value)

  var result = await fetch(
    '/api/quiz/uploadCsv',
    {
      method:'POST',
      headers:new Headers({'X-CSRFToken':csrf_token}),
      body:formdata
    }
  )
  var json_response = await result.json()
  return json_response
}

$(document).ready(function () {  
  var path_name = location.pathname.split('/').splice(1)

  $('#addquest').on('click', function() {
    $('#question-wrapper').clone().appendTo('#question-box').find('input').val('')
  })
  $('#submitquest').on('click', function() {
    var completed_data = {}
    var final_data = {}
    var valid = true 
    var data = {}
    var my_list = Array()
    var question_wrapper = document.getElementsByClassName('question-wrapper')
    for(var i =0; i < question_wrapper.length; i++){
      var inputs = question_wrapper[i].getElementsByTagName('input')
      for(var y=0; y<inputs.length; y++){
        var name_input = inputs[y].name 
        var value_input = inputs[y].value 

        if((name_input == 'answer' || name_input == 'question') && value_input.length == 0){
          valid = false 
        }
        data[name_input] = value_input
      }

      my_list.push(data)

      completed_data['quiz_title'] = document.getElementById('q').value
      completed_data['data'] = my_list
      

      data = {}

    }
    completed_data['data'] = my_list

    if(valid ) {
      if(path_name.length == 3 & path_name[1] == 'edit-quiz'){
        var endpoint = '/api/quiz/edit/' + path_name[2]
      }else{
        var endpoint = '/api/quiz/add-quiz'
      }
      $('#message').html('adding your data ...')
      $.post({
        url:endpoint,
        dataType:'json',
        contentType:"application/json, charset=utf-8",
        data:JSON.stringify(completed_data)
      }).done(function(e) {
        $('#message').html(e['status'] + ' here is your link ' + e['url'])
      })

    }else{
      alert('data invalid, empty answer / question')
    }
   
  })
  $('#uploadquiz').on('click', async function() {
    var formdata = new FormData()
    var file = document.getElementById('csv').files[0];
    formdata.append('csv',file)
    formdata.append('quiz_title', document.getElementById('quiz_title').value)
    $('#message').html('uploading your csv...')
    var responses = await uploadfile();
    if (responses['status'] !== 'success') {
      $('#message').html(responses['message'])
    }else{
      $('#message').html(responses['status'])
    }

  })

  $('#editprofile').on('click', function() {
    var username = $('#username').val()
    var email = $('#email').val()
    var full_name = $('#full_name').val()
    var data = {'username':username, 'email':email, 'full_name':full_name}
    $('#message').html('Loading...')

    $.ajax({
      url:'/api/edit-profile',
      method:'post',
      data:JSON.stringify(data),
      contentType:'application/json'
    }).done(function(e) {
      $('#message').html(e['message'])
    })
  })
  $('#changepassword').on('click', function() {
    var old_password = $('#old_password').val()
    var new_password = $('#password').val()
    var password_confirmation = $('#password_confirmation').val()
    var data = {'old_password':old_password, 
                'password':new_password, 
                'password_confirmation':password_confirmation}

    $('#messages').html('loading..')
    var responses = $.ajax({
          url:'/api/change-password',
          method:'post',
          data:JSON.stringify(data),
          contentType:'application/json, charset=utf-8'
        }).then(function(r) {
          if(r['status'] == 'fail') {
            $('#messages').html(r['message'])
          }else{
            $('#messages').html('Changed')
          }
        })
  })
  if(path_name[1] == 'scores') {
    var scores_url = '/api/quiz/my-scores'
  }else if(path_name[1] == 'users-scores'){
    var scores_url = '/api/quiz/author/logged_in/getScores'
  }

  $('#list-users').DataTable({
    "processing":true,
    "ajax":"/api/users",
    "columns":[
      {"data":"username"},
      {"data":"full_name"},
      {"data":"joined_at.$date"},
      {"data":"type"},
      {"data":"username",
       "render":function(data, type, row) {
         return '<input type="checkbox" name="userslist[]" value="'+data+'">'  
       }
      }
    ]
  })

  $('#scores-users').DataTable({
        
    "processing":true, 
    "ajax":scores_url,
    "columns":[
      {"data":"name"},
      {"data":"score"},
      {"data":"quiz_title"},
      {"data":"do_at.$date"}
    ]
  })

  $('#optionsubmit').on('click', function() {
    var cheky = $("input[type='checkbox']:checked")
    var arr = Array()
    for(var i in cheky) {
      var data_checked = cheky[i].value
      if(data_checked) {
        arr.push(data_checked)
      }
    }
    var option = $('#option').find(':selected')
    if(option != '0') {
      var data = {"option":option.val(), "data":arr}
      $('#message').html('do some task :O')
      $.ajax({
        url:'/api/manage-users',
        method:'post',
        contentType:'application/json,charset=utf-8',
        data:JSON.stringify(data)
      }).done(function(r) {
        $('#message').html(r['message'])
        $('#list-users').DataTable().ajax.reload()
      })
    }
    console.log(option.val(), JSON.stringify(data))

  })
  
  $('#table-quiz').DataTable();

})
