$(document).ready(function() {
	mdpNotEmpty = false;
	remdpNotEmpty = false;
	emailNotEmpty = false;
	mdpValid = false;
	remdpValid = false;
	emailValid = false;
	
	/*
	$("#envoyer").click(function(){
		//mail

		
		//mdp
		if($("#id_in_re_mdp").val() == "")
		{
			$("#label-conmdp").next(".erreur").fadeIn().text("Required champs").css("color", "red");
			$("#id_in_re_mdp").css("border-color","red");
			mdpNotEmpty = false;

		} else {
			mdpNotEmpty = true;
		}
		
		//cnmdp
		if($("#id_in_mdp").val() == "") 
		{  
			$("#label-mdp").next(".erreur").fadeIn().text("Required champs").css("color", "red");
			$("#id_in_mdp").css("border-color","red");
			mdpNotEmpty = false;
		}
		else {
			mdpNotEmpty = true;			
		}
        });
*/
	$('#id_in_email').focusout(function(){
		if($("#id_in_email").val() == "")
		{
			$("#label-mail").next(".erreur").fadeIn().text("Required champs").css("color", "red");
			$("#id_in_email").css("border-color","red");
			emailValid = false;
		} else {		
		
		$('#id_in_email').filter(function(){
			var emil=$('#id_in_email').val();
			var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
                        
				if( (!emailReg.test( emil )) || ($('#id_in_email').val() == ""))  
				{
					$("#label-mail").next(".erreur").fadeIn().text("E-mail invalide").css("color", "red");
					$("#id_in_email").css("border-color","red");
					emailValid = false;
					
				}
				else 
				{
					emailValid = true;
					$("#label-mail").next(".erreur").fadeIn().text("E-mail valide").css("color", "green");
					$("#id_in_email").css("border-color","green");
				}
			});
		
			}
		});
	

	$('#id_in_mdp').focusout(function(){
		if ($('#id_in_mdp').val() == "") {
			mdpValid = false;
			$("#label-mdp").next(".erreur").fadeIn().text("Required champs").css("color", "red");
			$("#id_in_mdp").css("border-color","red");
        }
	});
	
	$('#id_in_mdp').keyup(function(){
		
			if (($('#id_in_mdp').val().length <= 3)){
					mdpValid = false;
			}
			else if (($('#id_in_mdp').val().length <= 7)){
				mdpValid = false;
				$("#label-mdp").next(".erreur").fadeIn().text("Allez! mieux").css("color", "red");
				$("#id_in_mdp").css("border-color","red"); 
			}
			else {
				if ( $('#id_in_mdp').val().match(/[A-z]/) ){
					if ( $('#id_in_mdp').val().match(/\d/) ){
						if ( $('#id_in_mdp').val().match(/[A-Z]/) ){
							mdpValid = true;
							$("#label-mdp").next(".erreur").fadeIn().text("C'est Fort").css("color", "green");
							$("#id_in_mdp").css("border-color","green");
						 }
						else {
							mdpValid = true;
							$("#label-mdp").next(".erreur").fadeIn().text("Un seul pas!").css("color", "orange");
							$("#id_in_mdp").css("border-color","orange");
							}
					  }
					else {
							mdpValid = false;
							$("#label-mdp").next(".erreur").fadeIn().text("Allez! mieux").css("color", "red");
							$("#id_in_mdp").css("border-color","red");  
					  }
				  	}

				else{
					mdpValid = false;
					$("#label-mdp").next(".erreur").fadeIn().text("Allez! mieux").css("color", "red");
					$("#id_in_mdp").css("border-color","red"); 	 
							 }
							 }
            });

    $('#id_in_re_mdp').focusout(function(){
                if ($('#id_in_re_mdp').val() == "") 
                {
					remdpValid = false;
                    $("#label-conmdp").next(".erreur").fadeIn().text("Required champs").css("color", "red");
                    $("#id_in_re_mdp").css("border-color","red");
                }
                else if ($('#id_in_mdp').val() != $('#id_in_re_mdp').val()) 
                {
					remdpValid = false;
                    $("#label-conmdp").next(".erreur").fadeIn().text("Different").css("color", "red");
                    $("#label-mdp").next(".erreur").fadeIn().text("Different").css("color", "red");
                    $("#id_in_re_mdp").css("border-color","red");
                    $("#id_in_mdp").css("border-color","red");
                }
                else
                {
					remdpValid = true;
                    $("#label-conmdp").next(".erreur").fadeIn().text("Bien").css("color", "green");
                    $("#id_in_re_mdp").css("border-color","green");
                }

            });
            
            //Placeholder
            var placeAttr = '';

            $('[placeholder]').focus(function(){
                placeAttr = $(this).attr('placeholder');
                $(this).attr('placeholder', '');

            }).blur(function(){
                $(this).attr('placeholder', placeAttr);
            });
            
	$("form").submit(function(e){
		if ( !mdpValid || !emailValid || !remdpValid){
		e.preventDefault(e);
		}
            });
	
        });