// Functional Inherits Implemented
var debug_flag = true;

function IPTestObject(){
	var rb = Rollback();

	this.callback = function(r){
		console.log(r);
		if(r.user_data ==null)
			return;
		if(r.user_data.test_data==null)
			return;

		for(var i=0;i<r.user_data.test_data.length;i++){
			rb.addRollbackData(r.user_data.test_data[i]);	
		}			
		// console.log( JSON.stringify( rb.getData() ) );
	}

	this.endTest = function(){
		console.log("FINAL TESTE");
		rb.rollback();
	}

}

function DesignTest(ip){
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
			ip.test_callback.endTest();
		}

		stage = (stage+1);
	};
}

var Rollback = function(){
	var that = CallTest({testObject:null});

	var rollbackData = [];

	var fn_success = function(r){

	}

	var fn_error = function(r){

	}

	that.addRollbackData = function(data){
		rollbackData.push(data);
	}

	that.rollback = function(){
		that.serverRequest("POST",{ "rollbackObj":JSON.stringify(rollbackData) },"/rollback",fn_success,fn_error);
	}

	that.getData = function(){return rollbackData;}

	return that;
}