$(document).ready(function () {

$('.datepicker').datepicker({
    format: 'yyyy/mm/dd',
    startDate: '-3d'
});

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
var getUrl = window.location;
var baseUrl = getUrl .protocol + "//" + getUrl.host + "/" + getUrl.pathname.split('/')[0];
new_notify_count = 'null';
setInterval(function(){
$.ajax({
    url: baseUrl+'api/v1/core/notification/',
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

//ajax request for district
$('#id_province_id').on('change',function(){
prov_id = $(this).val()
$.ajax({
    url: baseUrl+'api/v1/core/district/?province_id='+prov_id,
//    headers: {
//        'Authorization': "Token 8933c5dd02de389ab5ee69c17a9af49f3d83b938",
//    },
    method: 'GET',
    success: function(result){


    var district = result.results
    $('#id_district_id').html("");
    for(var i = 0 ; i<district.length;i++){
    var prov_div="<option value="+district[i].id+">"+district[i].name+"</option>"
    $('#id_district_id').append(prov_div);
    }

    }});
    }); // end

//ajax request for mun
$('#id_district_id').on('change',function(){
dist_id = $(this).val()
$.ajax({
    url: baseUrl+'api/v1/core/gapanapa/?district_id='+dist_id,
//    headers: {
//        'Authorization': "Token 8933c5dd02de389ab5ee69c17a9af49f3d83b938",
//    },
    method: 'GET',
    success: function(result){



    $('#id_municipality_id').html("");
    var mun = result.results
    for(var i = 0 ; i<mun.length;i++){
    var prov_div="<option value="+mun[i].id+">"+mun[i].name+"</option>"
    $('#id_municipality_id').append(prov_div);
    }

    }});
    }); // end

$('#id_program_id').on('change',function(){
dist_id = $(this).val()
$.ajax({
    url: baseUrl+'api/v1/core/project/?program_id='+dist_id,
//    headers: {
//        'Authorization': "Token 8933c5dd02de389ab5ee69c17a9af49f3d83b938",
//    },
    method: 'GET',
    success: function(result){



    $('#id_component_id').html("");
    var project = result.results
    for(var i = 0 ; i<project.length;i++){
    var prov_div="<option value="+project[i].id+">"+project[i].name+"</option>"
    $('#id_component_id').append(prov_div);
    }
    if(project.length < 1){
    console.log('comp', project.length)
    var prov_div="<option value=''>No component for selected program</option>";
    $('#id_component_id').append(prov_div);
    }

    }});
    }); // end


   $('#checkbox_id').on('change',function(){
     var sup=$('#id_supplier_id').val()
     var prog=$('#id_program_id').val()
     var comp=$('#id_component_id').val()
     var second=$('#id_second_tier_partner').val()
     console.log(second)
//   console.log('aaa');
//   console.log($('#checkbox_id').is(":checked"));
   var check=$('#checkbox_id').is(":checked")
   if (check){
   $('#second_tier').css('display','')
   $.ajax({
    url: baseUrl+'api/v1/core/five-filter/?supplier='+sup+'&second='+second+'&program='+prog+'&component='+comp,
//    headers: {
//        'Authorization': "Token 8933c5dd02de389ab5ee69c17a9af49f3d83b938",
//    },
    method: 'GET',
    success: function(result){

    if(result.results.length >= 1 ){
    console.log(result.results)
    }


    }});

   }else{
    $('#second_tier').css('display','None')
   }

   });

}); // document end

