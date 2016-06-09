$(document).ready(function (){
	var inbox = $(".badge").html()
	if (parseFloat(inbox) == 0){
		$(".badge").css('background-color','#449d44')
	}
	else
	{
		$(".badge").css('background-color','#F13F47')
	}
})

