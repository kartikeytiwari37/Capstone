
var MainMenu = (function() {
    var MainMenu = function(config) {
        config = config || {};
        this.toggleBtn = $(config.toggleBtn);
        this.menu = $(config.menu);
        this.close = $(config.close);

        this.init();
        config = null;
    };
    // public interface
    MainMenu.prototype = {
        constructor: MainMenu,
        init: function() {
            this.eventManager();
        },
        eventManager: function() {
            this.toggleBtn.on('click.openMenu', onButtonClickHandler.bind(this));
            this.close.on('click.closeMenu', onCloseClickHandler.bind(this));
        }
    };
    // private interface
    function onButtonClickHandler(menu, evt) {
        if (!this.menu.hasClass('open')) {
            this.menu.addClass('open');
        };

    }

    function onCloseClickHandler(evt) {
        this.menu.removeClass('open')
    }

    function onDocumentClickHandler(evt) {
        var $target = $(evt.target);

        if (!$target.closest(this.menuForm).length && !$target.closest(this.menuContent).length && this.menu.hasClass('open')) {
            this.menu.removeClass('open')
        }
    }

    return MainMenu;
})();


$(document).ready(function() {
    var mainMenu = new MainMenu({
        menu: '.main-menu',
        toggleBtn: '.main-menu-btn',
        close: '.main-menu-close'
    });
});

$(document).ready(function() {
  var navOpen = false;
  $('.toggle-nav').click(function() {
    if (navOpen == false) {
      $('.wrapper').css("position", "absolute").animate({
        left: "30%"
      });
      $(this).animate({
        left: "30%"
      }).removeClass("entypo-menu").addClass("entypo-cancel");
      $('nav').animate({
        left: "0%"
      });
      navOpen = true;
    } else {
      $('.wrapper').animate({
        left: "0%"
      }, function() {
        $(this).css("position", "relative");
      });
      $(this).animate({
        left: "0%"
      }).removeClass("entypo-cancel").addClass("entypo-menu");
      $('nav').animate({
        left: "-30%"
      });
      navOpen = false;
    }
  });
  
  // Smooth Anchor Scrolling
  $('a').click(function(){
    $('html, body').animate({
        scrollTop: $($(this).attr('href')).offset().top
    }, 500);
    return false;
  });
});

