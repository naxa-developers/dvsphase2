

function CustomScrollbar() {
    $(".marker-body, .category-body").slimscroll({
        height: "auto",
        color: "#D9002A",
        position: "right",
        size: "3px",
        alwaysVisible: 1,
        borderRadius: "3px",
        railBorderRadius: "0"
    }),
     
    $(".navbar-right .dropdown-menu .body").slimscroll({
        height: "330px",
        color: "#8c909a",
        size: "3px",
        alwaysVisible: !1,
        borderRadius: "3px",
        railBorderRadius: "0"
    });
}

function CustomJs() {
    $(".ls-toggle-btn").on("click", function() {
        $("body").toggleClass("ls-toggle-menu");
        // $('.menu .list li').addClass('submenu');
    }), 
    $(".mobile_menu").on("click", function() {
        $(".sidebar").toggleClass("open")
    });
     
};

function checkStatuForResize (a) {
    var b = $("body"),
        c = $(".navbar .navbar-header .bars"),
        d = b.width();
    a && b.find(".page-wrapper, .sidebar").addClass("no-animate").delay(1e3).queue(function() {
        $(this).removeClass("no-animate").dequeue()
    }), d < 1170 ? (d > 767 && b.addClass("ls-toggle-menu"), b.addClass("ls-closed"), c.fadeIn()) : (b.removeClass("ls-closed ls-toggle-menu"), c.fadeOut())
};
checkStatuForResize();


$(window).on('resize',function(){
    function checkStatuForResize (a) {
        var b = $("body"),
            c = $(".navbar .navbar-header .bars"),
            d = b.width();
        a && b.find(".page-wrapper, .sidebar").addClass("no-animate").delay(1e3).queue(function() {
            $(this).removeClass("no-animate").dequeue()
        }), d < 1170 ? (d > 767 && b.addClass("ls-toggle-menu"), b.addClass("ls-closed"), c.fadeIn()) : (b.removeClass("ls-closed ls-toggle-menu"), c.fadeOut())
    };
    checkStatuForResize();
})

$('.menu .list li a.menu-toggle').on('click', function(e){
    e.preventDefault();
    $("body").addClass("ls-toggle-menu");
    
    if($(this).closest('li').next().hasClass('submenu')){
        $('.menu .list li').removeClass('submenu');
    }else{
        $('.menu .list li').removeClass('submenu');
    }
    $(this).closest('li').addClass('submenu');
});

$('.program-footer a').on('click',function(e){
    e.preventDefault();
    $(this).closest('.dfid-program').find('.hide-details').slideToggle('300');
});

function checkbox(){
    $(".checklist-header .custom-control-input").change(function () {
      $(this).closest('.checklist-card').find('.custom-checkbox input').prop('checked', $(this).prop("checked"));
      $(this).closest('.checklist-header').toggleClass('active');
      $(this).closest('.checklist-card').find('ul').slideToggle(300);
    });
  
    $(".checklist-card .custom-checkbox input").change(function() {
        var checkboxes = $(this).closest('.custom-checkbox').find('input');
        var checkedboxes = checkboxes.filter(':checked');
    
        if(checkboxes.length === checkedboxes.length) {
        $(this).closest('.checklist-header').find('.custom-checkbox input').prop('checked', true);
        
        } else {
          $(this).closest('.checklist-header').find('.custom-checkbox input').prop('checked', false);
        }
    });
  };
  checkbox();

var programmeHeight = $('.dfid-program .program-info').height();
$('.dfid-program .about-programme').css({'min-height': programmeHeight});


$(function() {
    "use strict";
    CustomScrollbar(), CustomJs()
}); 

