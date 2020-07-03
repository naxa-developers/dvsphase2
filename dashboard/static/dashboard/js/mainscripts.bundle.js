

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


function multipleMenu() {
    $(".menu .list > .submenu > a").click(function () {
      var e = $(this).next(".ml-menu")
        , a = ".menu .list > li.submenu > .ml-menu";
      0 === $(".minified-menu").length && ($(a).not(e).slideUp(function () {
        $(this).closest("li").removeClass("open")
      }),
        $(e).slideToggle(function () {
          var e = $(this).closest("li");
          $(e).hasClass("open") ? $(e).removeClass("open") : $(e).addClass("open")
        }))
    }),
      $(".menu .list > .submenu .ml-menu li.submenu > a").click(function () {
        if (0 === $(".minified-menu").length) {
          var e = $(this).next(".ml-menu");
          $(e).slideToggle()
        }
      });
  }
  multipleMenu();



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
  function tableAction (){
    $('.table-action a.more-action').on('click',function(e){
        e.preventDefault();
        $(this).closest('.table-action ').find('ul').slideToggle(200);
    })
  }
  tableAction();
  function minHeight (){
    var programmeHeight = $('.dfid-program .program-info').innerHeight();
    $('.dfid-program .about-program').css({'min-height': programmeHeight});
    var winWidth = $( window ).width();
    if(winWidth <= 767){
        $('.dfid-program .about-program').css({'min-height': 'auto'});
    }
  }
  minHeight();



$(function() {
    "use strict";
    CustomScrollbar(), CustomJs()
}); 

