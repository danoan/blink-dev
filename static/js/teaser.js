function TestObject(ip){
	var stage = 1;

	this.run = function(){	
		if(stage==0){
			ip.fn_share()
		}else if(stage==1){
			ip.fn_processing();
		}else if(stage==2){
			ip.fn_error();	
		}else if(stage==3){
			$("#btn-try-again").click();	
		}else if(stage==4){
			ip.fn_processing();
		}else if(stage==5){
			ip.fn_success();	
		}
		stage = (stage+1)%6;
	};

}

function SuggestionsPanel(divPanel,suggestions){			
	var current = document.createElement("span");
	var other = document.createElement("span");
	var curs = 0;

	var toggle_current = function(){
		var temp = current;
		current = other;
		other = temp;
	}

	var myint;

	$(current).attr("style","display:none");
	$(other).attr("style","display:none");

	divPanel.append(current);
	divPanel.append(other);	

	this.start =function(){
		myint = setInterval(function(){
			$(current).fadeOut(function(){
				toggle_current();
				$(other).fadeOut();

				$(current).html(function(){
						return suggestions[curs++%suggestions.length];
				}()).fadeIn();						
				
			});

		},2500);	
	}

	this.stop = function(){
		clearInterval(myint);
		$(current).attr("style","display:none");
		$(other).attr("style","display:none");					
	}			

	this.adjust = function(){
		var newW = $(".field-container input").width();
		$(".suggestions-container").width( newW );					
		$(".suggestions-container").css( "margin-left", -newW/2 );	
	}

	this.adjust();
	this.start();				
}

function InteractionPanel(){
	var suggestions = ["Dançar Salsa","Manobras de Skate","Dicas para um mochilão na Europa","Posições de Ioga","Desenhar o Sr. Incrível","A importância da luz na fotografia","História da 2a Guerra Mundial","Programação em Python","Curiosidades sobre raças de cachorros"];

	var sp1 = new SuggestionsPanel($(".fluid .suggestions-container"),suggestions);
	var sp2 = new SuggestionsPanel($(".stacked .suggestions-container"),suggestions);

	var cur_container = $(".field-container");

	var input_type = Math.round(Math.random());

	if(input_type==0){
		$("#question-label-1").css("display","block");
	}else{
		$("#question-label-2").css("display","block");
	}

	var _login = function login(){
		if($("#field-question").val().trim().length==0){
			$(".control-group").addClass("error");
			setTimeout(function(){console.log("OI");$(".control-group").removeClass("error");},750);
			return;
		}

		$(".control-group").removeClass("error");
		fn_processing();

		FB.login(function(response){
			if(response.authResponse){
				afterLogin();
			}else{
				fn_error(response);
			}
		});			
	}

	var afterLogin = function(response){
		FB.api('/me?fields=name,age_range,locale,gender,id',function(response){		

			var formData = {
				"field-name": response.name,
				"field-age": response.age_range.min,
				"field-locale": response.locale,
				"field-gender": response.gender,
				"field-fbid": response.id,
				"field-question":$("#field-question").val(),
				"field-request-type": input_type
			};

			$.ajax({
				type:"POST",
				url:"",
				data: formData,
				dataType:"text",
				success:function(r){
					fn_success(r);					
				},
				error:function(r){
					fn_error(r);				
				}
			})

		});
	}	

	this.login = _login;

	this.fn_error = function(r){
		cur_container.fadeOut(function(){
			cur_container = $(".try-again-container");
			cur_container.fadeIn();
		});
	}

	this.fn_processing = function(){
		cur_container.fadeOut(function(){
			cur_container = $(".loading-container");
			cur_container.fadeIn();
		});
	}

	this.fn_success = function(r){
			cur_container.fadeOut(function(){
			cur_container = $(".thanks-container");
			cur_container.fadeIn();
		});	
	}

	this.fn_share = function(r){
			cur_container.fadeOut(function(){
			cur_container = $(".field-container");
			cur_container.fadeIn();
		});	
	}	

	this.fn_resize = function(){
		sp1.adjust();
		sp2.adjust();
	}

	this.fn_focus = function(){
		sp1.stop();
		sp2.stop();
	}

	this.fn_blur = function(){
		if($("#field-question").val().trim().length==0){
			sp1.start();
			sp2.start();
		}		
	}

}
