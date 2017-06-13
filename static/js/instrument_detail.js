
$(document).ready(function(){
  $("#star1").mouseenter(function(){
  	  $("#grage-star .glyphicon-star").css("color","#bababa");
      $("#star1").css("color","#e48f15");
      $("#star-exp").text(" 很差");
  });
  $("#grage-star .glyphicon-star").mouseleave(function(){
  	if ($("#star-grade-score").text()=="")
      {
	  	  $("#grage-star .glyphicon-star").css("color","#bababa");
	      $("#star-exp").text("");
        $("#star-grade-score").text("");
       }
     else if ($("#star-grade-score").text()=="2")
      {
	  	  $("#grage-star .glyphicon-star").css("color","#bababa");
	      $("#star1").css("color","#e48f15");
	      $("#star-exp").text(" 很差");
	      $("#star-grade-score").text("2");
      }
     else if ($("#star-grade-score").text()=="4")
      {
	  	  $("#grage-star .glyphicon-star").css("color","#bababa");
	      $("#star2").css("color","#e48f15");
	      $("#star1").css("color","#e48f15");
	      $("#star-exp").text(" 较差");
	      $("#star-grade-score").text("4");
      }
     else if ($("#star-grade-score").text()=="6")
      {
	  	  $("#grage-star .glyphicon-star").css("color","#bababa");
	      $("#star3").css("color","#e48f15");
	      $("#star1").css("color","#e48f15");
	      $("#star2").css("color","#e48f15");
	      $("#star-exp").text(" 还行");
	      $("#star-grade-score").text("6");
      }
     else if ($("#star-grade-score").text()=="8")
      {
	  	  $("#grage-star .glyphicon-star").css("color","#bababa");
	      $("#star4").css("color","#e48f15");
	      $("#star1").css("color","#e48f15");
	      $("#star2").css("color","#e48f15");
	      $("#star3").css("color","#e48f15");
	      $("#star-exp").text(" 推荐");
	      $("#star-grade-score").text("8");
      }
     else if ($("#star-grade-score").text()=="10")
      {
	  	  $("#grage-star .glyphicon-star").css("color","#bababa");
	      $("#star5").css("color","#e48f15");
	      $("#star1").css("color","#e48f15");
	      $("#star2").css("color","#e48f15");
	      $("#star3").css("color","#e48f15");
	      $("#star4").css("color","#e48f15");
	      $("#star-exp").text(" 力荐");
	      $("#star-grade-score").text("10");
      }
  });


  $("#star2").mouseenter(function(){
  	  $("#grage-star .glyphicon-star").css("color","#bababa");
      $("#star2").css("color","#e48f15");
      $("#star1").css("color","#e48f15");
      $("#star-exp").text(" 较差");
  });


  $("#star3").mouseenter(function(){
  	  $("#grage-star .glyphicon-star").css("color","#bababa");
      $("#star3").css("color","#e48f15");
      $("#star1").css("color","#e48f15");
      $("#star2").css("color","#e48f15");
      $("#star-exp").text(" 还行");
  });


  $("#star4").mouseenter(function(){
  	  $("#grage-star .glyphicon-star").css("color","#bababa");
      $("#star4").css("color","#e48f15");
      $("#star1").css("color","#e48f15");
      $("#star2").css("color","#e48f15");
      $("#star3").css("color","#e48f15");
      $("#star-exp").text(" 推荐");
  });


  $("#star5").mouseenter(function(){
  	  $("#grage-star .glyphicon-star").css("color","#bababa");
      $("#star5").css("color","#e48f15");
      $("#star1").css("color","#e48f15");
      $("#star2").css("color","#e48f15");
      $("#star3").css("color","#e48f15");
      $("#star4").css("color","#e48f15");
      $("#star-exp").text(" 力荐");
  });

  $("#star1").click(function(){
      $("#star1").css("color","#e48f15");
      $("#star-exp").text(" 很差");
      $("#star-grade-score").text("2");
  });

  $("#star2").click(function(){
      $("#star2").css("color","#e48f15");
      $("#star1").css("color","#e48f15");
      $("#star-exp").text(" 较差");
      $("#star-grade-score").text("4");
  });


  $("#star3").click(function(){
      $("#star3").css("color","#e48f15");
      $("#star1").css("color","#e48f15");
      $("#star2").css("color","#e48f15");
      $("#star-exp").text(" 还行");
      $("#star-grade-score").text("6");
  });

  $("#star4").click(function(){
      $("#star4").css("color","#e48f15");
      $("#star1").css("color","#e48f15");
      $("#star2").css("color","#e48f15");
      $("#star3").css("color","#e48f15");
      $("#star-exp").text(" 推荐");
      $("#star-grade-score").text("8");
  });

  $("#star5").click(function(){
      $("#star5").css("color","#e48f15");
      $("#star1").css("color","#e48f15");
      $("#star2").css("color","#e48f15");
      $("#star3").css("color","#e48f15");
      $("#star4").css("color","#e48f15");
      $("#star-exp").text(" 力荐");
      $("#star-grade-score").text("10");
  });

});

