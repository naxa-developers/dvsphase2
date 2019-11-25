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



}); // document end