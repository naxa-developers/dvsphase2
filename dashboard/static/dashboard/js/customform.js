$(document).ready(function () {

contact_num = 1;
 $('#add_contact').on('click', function () {

 console.log("custom js")


 var contact_html = "";
 contact_html += '<div class="row" id="contact_div'+contact_num+'">'+


                '<div class="col-md-4">'+
                    '<div class="form-group ">'+
                        '<label for="id_contact_person_name" class="">Contact person name</label>'+
                       ' <input type="text" class="form-control" name="contact_person_name" maxlength="100" id="id_contact_person_name" placeholder="Name"/>'+
                    '</div>'+
                '</div>'+

                '<div class="col-md-3">'+
                    '<div class="form-group ">'+
                        '<label for="id_contact_person_email" class="">Contact person email</label>'+
                        '<input type="text" class="form-control" name="contact_person_email" maxlength="100" id="id_contact_person_email" placeholder="Email"/>'+
                    '</div>'+
                '</div>'+

                '<div class="col-md-3">'+
                    '<div class="form-group ">'+
                        '<label for="id_contact_person_ph" class="">Contact person ph</label>'+
                        '<input type="text" class="form-control" name="contact_person_ph" maxlength="100" id="id_contact_person_ph" placeholder="Number"/>'+
                    '</div>'+
                '</div>'+

                '<div class="col-md-2" id="test_a" >'+
                    '<span>'+
                        '<a href="javascript:void(0);" id="remove_contact" data-id="'+contact_num+'"><i class="material-icons" style="margin-top:50px">remove_circle</i></a>'+
                    '</span>'+
                '</div>'+

                '</div>';

                contact_num++
                $('#contact_form').append(contact_html);
 })


 $('#contact_form').on('click', '#remove_contact', function () {
 id=$(this).attr("data-id")
 $( '#contact_div'+id ).remove();


 })

new_notify_count = 'null';
setInterval(function(){
$.ajax({
    url: 'http://localhost:8000/api/v1/core/notification/',
//    headers: {
//        'Authorization': "Token 8933c5dd02de389ab5ee69c17a9af49f3d83b938",
//    },
    method: 'GET',
    success: function(result){
          item = localStorage.getItem('notify-item');
      if (item == null){
      localStorage.setItem('notify-item', 0)

      }else{

      if ( result.count <= item) {
//      localStorage.clear()
      localStorage.setItem('notify-item', result.count)


      }else{
//      localStorage.clear()

      $('#notify-active-bar').addClass('notify')


      }


      }

      new_notify_count = result.count
      $('#notifyBar').html('');
      var notify = '';
      notify += '<li class="dropdown-header">You have '+result.results.length+' notifications</li>';
      for (var i = 0; i < result.results.length; i++) {

        notify += '<li class = "notification-new"> <a href="'+result.results[i]['link']+'"> '+result.results[i]['message']+' <span class=" font-size-12 d-inline-block float-right">'+result.results[i]['date']+'</span></a></li>';

       }

       $('#notifyBar').append(notify);
       //localStorage.removeItem('notify-item');


    }
  });
  }, 5000);

$('#notify-id-div').on('click',function(){

   if(new_notify_count == 'null') {

   }else{
  localStorage.setItem('notify-item', new_notify_count)
   }
 $('#notify-active-bar').removeClass()

})

}); // document end