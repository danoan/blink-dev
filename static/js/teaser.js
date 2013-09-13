var debug_flag;

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

var CallTest = function(spec){
	var serverRequest =	function(method,formData,url,fn_success,fn_error,callback){
		$.ajax({
			"type":method,
			"url":url,
			"data": formData,
			"dataType":"json",
			success:function(r){
				fn_success(r);			
				if(callback!=null) callback(r);		
			},
			error:function(r){
				fn_error(r);
				if(callback!=null) callback(r);
			}
		})
	};

	var that = {test_callback:spec.testObject};
	that.serverRequest = function(){
		var l = arguments;
		if(spec.testObject!=null){
			l = [];
			for(var i=0;i<arguments.length;i++){
				l.push(arguments[i]);
			}
			l.push(spec.testObject.callback);	
		}
		serverRequest.apply(that,l);
	}

	return that;
}

var ValidationPanel = function(){
	var that = CallTest({test_callback:null});	

	var curPanel = null;
	var showMessage = function(panel,fade,afterFade_fn){
		if(curPanel==null){
			panel.show();
			curPanel = panel;
		}else{
			showPanel(panel,fade,afterFade_fn)
		}
	}

	var showPanel = function(panel,fade,afterFade_fn){
		if(fade){
			curPanel.fadeOut(function(){
				panel.fadeIn(afterFade_fn);

				curPanel = panel;
			});
		}else{
			curPanel.hide();
			panel.show();

			curPanel = panel;
		}
	}	

	that.show = function(){		
		$(".invalid-code").hide();
		$(".used-code").hide();
		$(".valid-code").hide();
		$(".error-code").hide();
		$("#myModal").on("shown.bs.modal",function(){$("#field-code").focus();});
		$("#myModal").modal( {"keyboard":true} );				
	}

	that.hide = function(){
		$("#myModal").modal('hide');			
	}

	that.validate = function(code){
		showMessage($("#myModal .loading-container"),false);

		var fn_success = function(r){
			// console.log(r);
			if(r.type=="exception"){
				that.codeIsNotValid(r);
			}else if(r.type=="success"){
				that.codeIsValid(r);
			}else if(r.type=="information"){
				that.codeIsNotValid(r);
			}
		}

		var fn_error = function(r){
			that.codeError(r);
		}

		that.serverRequest("POST",{"code":code},"/validate_code",fn_success,fn_error);
	}

	that.codeError = function(r){
		showMessage($(".error-code"));
		// console.log(r);
	}

	that.codeIsValid = function(r){

		$(".container-initial").hide();
		$(".tab-code-container").hide();
		$(".container-inter-blinker").show();


		showMessage($("#myModal .valid-code"),true,function(){
			setTimeout(function(){$("#myModal").modal("hide");},500);
		});
				
	}

	that.codeIsNotValid = function(r){
		if(r.user_data.info==="USED"){
			showMessage($(".used-code"));
		}else{
			showMessage($(".invalid-code"));
		}		
	}

	return that;
}

var InteractionPanel=function(suggestions){
	if(debug_flag){
		var that = CallTest({testObject:new IPTestObject()});	
	}else{
		var that = CallTest({});	
	}	

	var sp1 = new SuggestionsPanel($(".fluid .suggestions-container"),suggestions);
	var sp2 = new SuggestionsPanel($(".stacked .suggestions-container"),suggestions);

	var vp = ValidationPanel();

	var cur_container = $(".field-container");
	var input_type = Math.round(Math.random());

	if(input_type==0){
		$("#question-label-1").css("display","block");
	}else{
		$("#question-label-2").css("display","block");
	}

	var afterLogin = function(response){
		FB.api('/me?fields=name,age_range,locale,gender,id,location,birthday',function(response){		
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
			//method,formData,url,fn_success,fn_error,test_callback

			that.serverRequest("POST",formData,"",that.fn_success,that.fn_error)
		});
	}	

	that.login = function login(){
		if($("#field-question").val().trim().length==0){
			$(".control-group").addClass("error");
			setTimeout(function(){$(".control-group").removeClass("error");},750);
			return;
		}

		$(".control-group").removeClass("error");
		that.fn_processing();

		FB.login(function(response){
			if(response.authResponse){
				afterLogin();
			}else{
				that.fn_error(response);
			}
		},{scope:"user_birthday,user_location"});			
	}	

	that.fn_error = function(r){
		// console.log(r);
		cur_container.fadeOut(function(){
			cur_container = $(".try-again-container");
			cur_container.fadeIn();
		});
	}

	that.fn_processing = function(){
		cur_container.fadeOut(function(){
			cur_container = $(".loading-container");
			cur_container.fadeIn();
		});
	}

	that.fn_success = function(r){
		// console.log(r);
		cur_container.fadeOut(function(){
		cur_container = $(".thanks-container");
		cur_container.fadeIn();
		});	
	}

	that.fn_share = function(r){
			cur_container.fadeOut(function(){
			cur_container = $(".field-container");
			cur_container.fadeIn();
		});	
	}	

	that.fn_resize = function(){
		sp1.adjust();
		sp2.adjust();
	}

	that.fn_focus = function(){
		sp1.stop();
		sp2.stop();
	}

	that.fn_blur = function(){
		if($("#field-question").val().trim().length==0){
			sp1.start();
			sp2.start();
		}		
	}

	that.showCodePanel = function(){vp.show();}
	that.validateCode = function(code){vp.validate(code);}

	return that;
}

function teaser_init(suggestions){
	var ip = new InteractionPanel(suggestions);

	$(".tab-code-container").click(function(){
		ip.showCodePanel();
	});


	$("#field-question").keydown(function(e){
		if(e.keyCode==13){
			ip.login();
		}
	});	

	$("#field-code").keydown(function(e){
		if(e.keyCode==13){
			ip.validateCode( $(e.target).val().trim() );		
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

	(function(){

		if(debug_flag){
			var dt = new DesignTest(ip);
			var lt  = new LogicalTest(ip);
		}
		
		$(window).keydown(function(event){
			// console.log(event.keyCode);
			if(event.keyCode == 13) {
				event.preventDefault();
				return false;
			}else if(event.keyCode == 39 ){ //LEFT
				if(debug_flag) lt.run();
			}				
		});	

	})();	
}

