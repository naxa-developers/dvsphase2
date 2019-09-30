(function($) {
    'use strict';

    
    if ($("#timepicker-example").length) {
      $('#timepicker-example').datetimepicker({
        format: 'LT'
      });
    }
    if ($(".color-picker").length) {
      $('.color-picker').asColorPicker();
    }
    if ($(".datepicker").length) {
      $('.datepicker').datepicker({
        enableOnReadonly: true,
        todayHighlight: true,
        autoclose: true,
      });
    }
    if ($("#inline-datepicker").length) {
      $('#inline-datepicker').datepicker({
        enableOnReadonly: true,
        todayHighlight: true,
      });
    }
    if ($(".datepicker-autoclose").length) {
      $('.datepicker-autoclose').datepicker({
        autoclose: true
      });
    }
    if ($('input[name="date-range"]').length) {
      $('input[name="date-range"]').daterangepicker();
    }
    if ($('input[name="date-time-range"]').length) {
      $('input[name="date-time-range"]').daterangepicker({
        timePicker: true,
        timePickerIncrement: 30,
        locale: {
          format: 'MM/DD/YYYY h:mm A'
        }
      });
    };
    
    

    function uploadFile() {
      $('[data-behaviour="custom-upload-input"]').on('change', updateButton);
      function updateButton(e) {
        var inputValue = $(e.currentTarget).val().split( '\\' ).pop();
        $('[data-element="custom-upload-button"]').text(inputValue)
        e.preventDefault;
      };
    };
    uploadFile();

    function checkbox(){
      $(".select-all").change(function () {
        $(this).closest('.card').find('.checkbox input').prop('checked', $(this).prop("checked"));
      });
    
      $(".checkbox input").change(function() {
          var checkboxes = $(this).closest('.checkbox').find('input');
          var checkedboxes = checkboxes.filter(':checked');
      
          if(checkboxes.length === checkedboxes.length) {
          $(this).closest('.card-header').find('.select-all').prop('checked', true);
          } else {
            $(this).closest('.card-header').find('.select-all').prop('checked', false);
          }
      });
    };
    checkbox();

    $(".cluster-accordion .card-body input").change(function () {
      $(this).closest('.card').find('.card-header .select-all').prop('checked', true);
     });

     function checkList(){
       $('.graph .select-option span').on('click', function(){
        var $optList = $(this).closest('.select-option').find('.select-list');
        $("body").mouseup(function(e) {
          e.preventDefault();
            if (!$optList.is(e.target) && $optList.has(e.target).length === 0) {
              $optList.removeClass('select-open');
            }
        });
        $(this).closest('.select-option').find('.select-list').toggleClass('select-open');
       });
       
     }
     checkList();
     
     $('.add-unit').on('click',function(){
      var newTarget = $('<div class="target flex"><div class="target-unit flex"><label>Target unit</label><input type="text" class="form-control" placeholder="1"></div><div class="target-number flex"><label>Target number</label><input type="text" class="form-control" placeholder="1"></div></div>');
     
      $('.target-group').append(newTarget);
    });

    
    $(".progress-bar").each(function () {
      var now=$(this).attr('aria-valuenow')
      var max=$(this).attr('aria-valuemax')
      var $percent = (now / max) * 100;
      each_bar_width = $(this).attr('aria-valuenow');
      $(this).width(Math.round($percent) + '%');
      $(this).find('.popOver').html(Math.round($percent) + '%');
      $(this).parent().find('.progress-value').html(" " + now);
  });
    // $('.select2').select2();
    $('.collapse').collapse()
  })(jQuery);


