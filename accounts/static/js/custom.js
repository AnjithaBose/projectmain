$(function() {
    'use strict'; // Start of use strict


    /*--------------------------
    scrollUp
    ---------------------------- */
    $.scrollUp({
        scrollText: '<i class="fa fa-angle-up"></i>',
        easingType: 'linear',
        scrollSpeed: 900,
        animation: 'fade'
    });
 
	/*------------------------------------------------------------------
        Year
    ------------------------------------------------------------------*/
	$(function(){
    var theYear = new Date().getFullYear();
    $('#year').html(theYear);
	});
	/* -- Bootstrap Popover -- */
	$('[data-toggle="popover"]').popover();
	 /* -- Bootstrap Tooltip -- */
	 $('[data-toggle="tooltip"]').tooltip();

	/*------------------------------------------------------------------
        Menu
    ------------------------------------------------------------------*/
	$(".menu-icon").on('click', function () {
		$('body').toggleClass("mobile_nav");
    });
    
    $(".dropdown-menu li a").on('click',function () {
		$(this).parents(".dropdown").find('.btn').html($(this).html() + ' <span class="caret"></span>');
		$(this).parents(".dropdown").find('.btn').val($(this).data('value'));
    });
		
    // collapse button in panel
	$(document).on('click', '.t-collapse', function () {
		var el = $(this).parents(".card").children(".card_chart");
		if ($(this).hasClass("fa-chevron-down")) {
			$(this).removeClass("fa-chevron-down").addClass("fa-chevron-up");
			el.slideUp(200);

		} else {
			$(this).removeClass("fa-chevron-up").addClass("fa-chevron-down");
			el.slideDown(200);

		}
	});
    
	//close button in panel
	$(document).on('click', '.t-close', function () {
		$(this).parents(".card, .stats-wrap").parent().remove();
	});

    	//Scroll_BAr
    if($(".scroll_auto").length){
	$(".scroll_auto").mCustomScrollbar({
		setWidth: false,
		setHeight: false,
		setTop: 0,
		setLeft: 0,
		axis: "y",
		scrollbarPosition: "inside",
		scrollInertia: 950,
		autoDraggerLength: true,
		autoHideScrollbar: false,
		autoExpandScrollbar: false,
		alwaysShowScrollbar: 0,
		snapAmount: null,
		snapOffset: 0
	});
}
    //Add_li
	$(".todo--panel").on("submit", "form", function (a) {
		a.preventDefault();
		a = $(this);
		var c = a.find(".form-control");

		$('<li class="list-group-item" style="display: none;"><label class="todo--label"><input type="checkbox" name="" value="1" class="todo--input"><span class="todo--text">' + c.val() + '</span></label><a href="#" class="todo--remove">&times;</a></li>').appendTo(".list-group").slideDown("slow");
		c.val("");
	}).on("click", ".todo--remove", function (a) {
		a.preventDefault();
		var c = $(this).parent("li");
		c.slideUp("slow", function () {
			c.remove();
		});
	});
	$('#dc_accordion').dcAccordion();
	
});

/*------------------------------------------------------------------
 Loader 
------------------------------------------------------------------*/
jQuery(window).on("load scroll", function() {
    'use strict'; // Start of use strict
    // Loader 
     $('#dvLoading').fadeOut('slow', function () {
            $(this).remove();
        });
	  
});
