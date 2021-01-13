    	/*$("#input-recherche").focusin(function () {
			$("#input-recherche").css("background-color", "yellow");
		});*/

    	$(document).ready(function () {

			"use strict";
			    
			$("#input-recherche").focus(function () {
			        
			$(".style").animate({width: "100%"}, 500);
			        
			});
			$("#input-recherche").blur(function () {
			        
			$(".style").css({width: "0%"});
			        
			    });

		});

    	$(function () {
    		'use strict';	
			$('.navbar').css({position:'fixed'});
			
    		$('.navbar li a').click(function (e) {
    			e.preventDefault();
    			$('html, body').animate({
    				scrollTop: $('#' + $(this).data('scroll')).offset().top + 5
    			}, 1000);
    		});

    		//active class
    		$('.navbar li a').click(function () {
    			//$(this).addClass('active').parent().siblings().find('a').removeClass('active');
    			$('.navbar a').removeClass('active');
    			$(this).addClass('active');
    		});

    		//au moment cherche moi le link et mis le dans le header syncronisation

    		$(window).scroll(function(){
    			$('.block').each(function(){
    				if($(window).scrollTop() > $(this).offset().top)
    				{
    					var blockID = $(this).attr('id');

    					$('.navbar a').removeClass('active');
    					$('.navbar li a[data-scroll="' + blockID + '"]').addClass('active');
    				}

    			});

    			//Bouton scroll to the top

    			var scrollToTop = $('.scroll-to-top');
    			if($(window).scrollTop() >= 100)
    			{
    				if(scrollToTop.is(':hidden'))
    				{
						scrollToTop.fadeIn(400);
    				}
    				
    			}
    			else
    			{
    				scrollToTop.fadeOut(400);
    			}	

    		});

    		//Click to go up -> directe + smooth

    		$('.scroll-to-top').click(function(event){
    			event.preventDefault();

    			$('html, body').animate({
    				scrollTop: 0
    			}, 1000);

    		});
    	});

		