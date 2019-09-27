

function CustomScrollbar() {
    $(".sidebar .menu .list").slimscroll({
        height: "calc(100vh - 65px)",
        color: "#8c909a",
        position: "right",
        size: "2px",
        alwaysVisible: !1,
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
    }), 
    // $(".project_list .table-responsive").slimscroll({
    //     height: "500px",
    //     color: "#8c909a",
    //     size: "2px",
    //     alwaysVisible: !1,
    //     borderRadius: "3px",
    //     railBorderRadius: "2px"
    // }),
    $(".help-content").slimscroll({
        height: "300px",
        color: "#8c909a",
        size: "2px",
        alwaysVisible: 1,
        borderRadius: "3px",
        railBorderRadius: "2px"
    }),
    $(".right-sidebar .slim_scroll").slimscroll({
        height: "calc(100vh - 70px)",
        color: "#8c909a",
        size: "2px",
        alwaysVisible: !1,
        borderRadius: "3px",
        railBorderRadius: "0"
    })
}

function CustomJs() {
    $(".ls-toggle-btn").on("click", function() {
        $("body").toggleClass("ls-toggle-menu")
    }), 
    $(".mobile_menu").on("click", function() {
        $(".sidebar").toggleClass("open")
    }), 
    $(".right_icon_toggle_btn").on("click", function() {
        $("body").toggleClass("right_icon_toggle")
    })
};

$.PracticalAction = {}, $.PracticalAction.options = {
    leftSideBar: {
        scrollColor: "#8c909a",
        scrollWidth: "4px",
        scrollAlwaysVisible: !1,
        scrollBorderRadius: "0",
        scrollRailBorderRadius: "0"
    },
    dropdownMenu: {
        effectIn: "fadeIn",
        effectOut: "fadeOut"
    }
}, 
$.PracticalAction.leftSideBar = {
    activate: function() {
        var a = this,
            b = $("body"),
            c = $(".overlay");
        // $(window).on("click", function(d) {
        //     var e = $(d.target);
        //     "i" === d.target.nodeName.toLowerCase() && (e = $(d.target).parent()), !e.hasClass("bars") && a.isOpen() && 0 === e.parents("#leftsidebar").length && (e.hasClass("js-right-sidebar") || c.fadeOut(), b.removeClass("overlay-open"))
        // }), 
        $.each($(".menu-toggle.toggled"), function(a, b) {
            $(b).next().slideToggle(0)
        }), 
        $.each($(".menu .list li.active"), function(a, b) {
            var c = $(b).find("a:eq(0)");
            c.addClass("toggled"), c.next().show()
        }), 
        $(".menu-toggle").on("click", function(a) {
            var b = $(this),
                c = b.next();
            if ($(b.parents("ul")[0]).hasClass("list")) {
                var d = $(a.target).hasClass("menu-toggle") ? a.target : $(a.target).parents(".menu-toggle");
                $.each($(".menu-toggle.toggled").not(d).next(), function(a, b) {
                    $(b).is(":visible") && ($(b).prev().toggleClass("toggled"), $(b).slideUp())
                })
            }
            b.toggleClass("toggled"), c.slideToggle(320)
        }), 
        a.checkStatuForResize(!0), $(window).resize(function() {
            a.checkStatuForResize(!1)
        })
        
    },
    checkStatuForResize: function(a) {
        var b = $("body"),
            c = $(".navbar .navbar-header .bars"),
            d = b.width();
        a && b.find(".content, .sidebar").addClass("no-animate").delay(1e3).queue(function() {
            $(this).removeClass("no-animate").dequeue()
        }), d < 1170 ? (d > 767 && b.addClass("ls-toggle-menu"), b.addClass("ls-closed"), c.fadeIn()) : (b.removeClass("ls-closed ls-toggle-menu"), c.fadeOut())
    },
    isOpen: function() {
        return $("body").hasClass("overlay-open")
    }
}, 
// $.PracticalAction.rightSideBar = {
//     activate: function() {
//         var a = this,
//             b = $("#rightsidebar"),
//             c = $(".overlay");
//         $(window).on("click", function(d) {
//             var e = $(d.target);
//             "i" === d.target.nodeName.toLowerCase() && (e = $(d.target).parent()), !e.hasClass("js-right-sidebar") && a.isOpen() && 0 === e.parents("#rightsidebar").length && (e.hasClass("bars") || c.fadeOut(), b.removeClass("open"))
//         }), $(".js-right-sidebar").on("click", function() {
//             b.toggleClass("open"), a.isOpen() ? c.fadeIn() : c.fadeOut()
//         })
//     },
//     isOpen: function() {
//         return $(".right-sidebar").hasClass("open")
//     }
// }, 
$.PracticalAction.navbar = {
    activate: function() {
        var a = $("body"),
            b = $(".overlay");
        $(".bars").on("click", function() {
            a.toggleClass("overlay-open"), a.hasClass("overlay-open") ? b.fadeIn() : b.fadeOut()
        }), $('.nav [data-close="true"]').on("click", function() {
            var a = $(".navbar-toggle").is(":visible"),
                b = $(".navbar-collapse");
            a && b.slideUp(function() {
                b.removeClass("in").removeAttr("style")
            })
        })
    }
} 

var edge = "Microsoft Edge",
    ie10 = "Internet Explorer 10",
    ie11 = "Internet Explorer 11",
    opera = "Opera",
    firefox = "Mozilla Firefox",
    chrome = "Google Chrome",
    safari = "Safari";
    $.PracticalAction.browser = {
    activate: function() {
        var a = this;
        "" !== a.getClassName() && $("html").addClass(a.getClassName())
    },
    getBrowser: function() {
        var a = navigator.userAgent.toLowerCase();
        return /edge/i.test(a) ? edge : /rv:11/i.test(a) ? ie11 : /msie 10/i.test(a) ? ie10 : /opr/i.test(a) ? opera : /chrome/i.test(a) ? chrome : /firefox/i.test(a) ? firefox : navigator.userAgent.match(/Version\/[\d\.]+.*Safari/) ? safari : void 0
    },
    getClassName: function() {
        var a = this.getBrowser();
        return a === edge ? "edge" : a === ie11 ? "ie11" : a === ie10 ? "ie10" : a === opera ? "opera" : a === chrome ? "chrome" : a === firefox ? "firefox" : a === safari ? "safari" : ""
    }
}, 
$(function() {
    $.PracticalAction.browser.activate(), $.PracticalAction.leftSideBar.activate(), $.PracticalAction.rightSideBar.activate(), $.PracticalAction.navbar.activate(), setTimeout(function() {
        $(".page-loader-wrapper").fadeOut()
    }, 50)
}), 
 
$(function() {
    "use strict";
    CustomScrollbar(), CustomJs()
}); 
// $(function() {
//     $('a[href="#search"]').on("click", function(a) {
//         a.preventDefault(), $("#search").addClass("open"), $('#search > form > input[type="search"]').focus()
//     }), $("#search, #search #close").on("click keyup", function(a) {
//         a.target != this && "close" != a.target.id && 27 != a.keyCode || $(this).removeClass("open")
//     });
//     $('.help-icon').on('click', function(e){
//         e.preventDefault();
//         var helpContent = $(this).parent().find('.helpContent-wrap').slideDown(300);
        
//         $("body").mouseup(function(e) {
//             if (!helpContent.is(e.target) && helpContent.has(e.target).length === 0) {
//                 helpContent.slideUp(300);
//             }
//         });
//     });
    
// });
