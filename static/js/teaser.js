function teaser_init(suggestions){
	var ip = new InteractionPanel(suggestions);

	var to = new TestObject(ip);
	var lt  = new LogicalTest(ip);
	var debug = false;

	$(".tab-code-container").click(function(){
		ip.showCodePanel();
	});


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
		}else if(stage==6){
			$(".tab-code-container").click();
		}else if(stage==7){
			ip.test_codeIsNotValid( {"user_data":{"type":"exception"}} );
		}else if(stage==8){
			ip.test_codeIsNotValid( {"user_data":{"type":"information"}} );
		}else if(stage==9){
			ip.test_codeError("ERRO");
		}else if(stage==10){
			ip.test_codeIsValid("OK");
		}else if(stage==11){
			ip.test_hideModal();
		}
		stage = (stage+1)%12;
	};
}

function LogicalTest(ip){
	var stage = 0;

	this.run = function(){	
		if(stage==0){
			$(".suggestions-container").click();
		}else if(stage==1){
			$("#field-question").val("My Activity Test");
		}else if(stage==2){
			$(".field-container .btn").click();			
		}else if(stage==3){
			ip.fn_share();
		}else if(stage==4){
			$(".tab-code-container").click();
		}else if(stage==5){
			$("#field-code").focus();
			$("#field-code").val("Mdb69nKHMln");
		}else if(stage==6){
			ip.validateCode( $("#field-code").val().trim() );
		}else if(stage==7){
			$("#field-question").val("My Activity Test");
		}else if(stage==8){
			$(".field-container .btn").click();			
		}else if(stage==9){
			// console.log("ROLLBACK");
			ip.rollback();
		}

		stage = (stage+1)%10;
	};
}

function Rollback(){
	var rollbackData = [];
	var that = this;

	var fn_success = function(r){

	}

	var fn_error = function(r){

	}

	this.addRollbackData = function(data){
		rollbackData.push(data);
	}

	this.rollback = function(){
		serverRequest("POST",{ "rollbackObj":JSON.stringify(rollbackData) },"rollback",fn_success,fn_error);
	}

	this.getData = function(){return rollbackData;}

}


function ValidationPanel(){

	var that = this;

	var curPanel = null;
	var showMessage = function(panel,fade,afterFade_fn){
		if(curPanel==null){
			panel.show();
			curPanel = panel;
		}else{
			showPanel(panel,fade)
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

	this.show = function(){
		$(".invalid-code").hide();
		$(".used-code").hide();
		$(".valid-code").hide();
		$(".error-code").hide();
		$("#myModal").modal( {"keyboard":true} );		
	}

	this.hide = function(){
		$("#myModal").modal('hide');			
	}

	this.validate = function(code){
		showMessage($("#myModal .loading-container"),false);

		$.ajax({
			url:"validate_code",
			type:"POST",
			data:{"code":code},
			dataType:"json",
			success:function(r){
				if(r.type=="exception"){
					that.codeIsNotValid(r);
				}else if(r.type=="success"){
					that.codeIsValid(r);
				}else if(r.type=="information"){
					that.codeIsNotValid("USED");
				}
			},
			error:function(r){
				that.codeError(r);
			}
		});
	}

	this.codeError = function(r){
		showMessage($(".error-code"));
		// console.log(r);
	}

	this.codeIsValid = function(r){

		$(".container-initial").hide();
		$(".tab-code-container").hide();
		$(".container-inter-blinker").show();


		showMessage($("#myModal .valid-code"),true,function(){
			setTimeout(function(){$("#myModal").modal("hide");},500);
		});
				
	}

	this.codeIsNotValid = function(r){
		if(r.user_data.type==="information"){
			showMessage($(".used-code"));
		}else{
			showMessage($(".invalid-code"));
		}		
	}

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

function serverRequest(method,formData,url,fn_success,fn_error,test_callback){

	$.ajax({
		"type":method,
		"url":url,
		"data": formData,
		"dataType":"json",
		success:function(r){
			// console.log(r);
			fn_success(r);			
			if(test_callback!=null) test_callback(r);		
		},
		error:function(r){
			// console.log(r);
			fn_error(r);
			if(test_callback!=null) test_callback(r);
		}
	})

}

function InteractionPanel(suggestions){
	var sp1 = new SuggestionsPanel($(".fluid .suggestions-container"),suggestions);
	var sp2 = new SuggestionsPanel($(".stacked .suggestions-container"),suggestions);

	var vp = new ValidationPanel();
	var rb = new Rollback();

	var cur_container = $(".field-container");

	var input_type = Math.round(Math.random());

	if(input_type==0){
		$("#question-label-1").css("display","block");
	}else{
		$("#question-label-2").css("display","block");
	}

	var that = this;

	var _test_callback = function(r){
		// console.log("TESTE",r);
		if(r.user_data ==null)
			return;
		if(r.user_data.test_data==null)
			return;

		for(var i=0;i<r.user_data.test_data.length;i++){
			rb.addRollbackData(r.user_data.test_data[i]);	
		}	

		// console.log( JSON.stringify( rb.getData() ) );
	}

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

			serverRequest("POST",formData,"",that.fn_success,that.fn_error,_test_callback)
		});
	}	

	this.login = _login;

	this.fn_error = function(r){
		// console.log(r);
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
		// console.log(r);
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

	this.showCodePanel = function(){vp.show();}
	this.validateCode = function(code){vp.validate(code);}

	this.test_codeIsValid = function(r){vp.codeIsValid();}
	this.test_codeIsNotValid = function(r){vp.codeIsNotValid(r);}
	this.test_codeError = function(r){vp.codeError(r);}
	this.test_hideModal = function(){vp.hide();}

	this.rollback = function(){
		rb.rollback();
	}
}
