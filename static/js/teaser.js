function teaser_init(suggestions){
	var ip = new InteractionPanel(suggestions);

	var to = new TestObject(ip);
	var debug = false;

	$(window).keydown(function(event){
		// console.log(event.keyCode);
		if(event.keyCode == 13) {
			event.preventDefault();
			return false;
		}else if(event.keyCode == 39 ){ //LEFT
			if(debug) to.run();
		}				
	});


	$("#field-question").keydown(function(e){
		if(e.keyCode==13){
			ip.login();
		}
	});	

	$(".button-container button").click(function(){ip.login();});		
	$("#btn-try-again").click(function(){ip.fn_share();});	

	$("#field-question").focus(function(){ip.fn_focus()});
	$("#field-question").blur(function(){ip.fn_blur()});
	$("#field-question").resize(function(){ip.fn_resize();});	

	$(".suggestions-container").click(function(){
		$("#field-question").focus();
	});
}

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

function InteractionPanel(suggestions){
	var sp1 = new SuggestionsPanel($(".fluid .suggestions-container"),suggestions);
	var sp2 = new SuggestionsPanel($(".stacked .suggestions-container"),suggestions);

	var cur_container = $(".field-container");

	var input_type = Math.round(Math.random());

	if(input_type==0){
		$("#question-label-1").css("display","block");
	}else{
		$("#question-label-2").css("display","block");
	}

	var that = this;

	var _login = function login(){
		if($("#field-question").val().trim().length==0){
			$(".control-group").addClass("error");
			setTimeout(function(){$(".control-group").removeClass("error");},750);
			return;
		}

		$(".control-group").removeClass("error");
		this.fn_processing();

		FB.login(function(response){
			if(response.authResponse){
				afterLogin();
			}else{
				this.fn_error(response);
			}
		},{scope:"user_birthday,user_location"});			
	}

	var afterLogin = function(response){
		FB.api('/me?fields=name,age_range,locale,gender,id,location,birthday',function(response){		
			console.log(response);
			var formData = {
				"field-name": response.name,
				"field-birthday": response.birthday,
				"field-locale": response.locale,
				"field-location": response.location.name,
				"field-gender": response.gender,
				"field-fbid": response.id,
				"field-question":$("#field-question").val(),
				"field-request-type": input_type
			};

			// console.log(formData);

			$.ajax({
				type:"POST",
				url:"",
				data: formData,
				dataType:"text",
				success:function(r){
					that.fn_success(r);					
				},
				error:function(r){
					that.fn_error(r);				
				}
			})

		});
	}	

	this.login = _login;

	this.fn_error = function(r){
		console.log(r);
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
		console.log(r);
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
