
$(document).ready(function(){
  $(".weiboshare").mouseenter(function(){
      $(this).css("background-color","#f63756");
  });
  $(".weiboshare").mouseleave(function(){
      $(this).css("background-color"," #fafafa");
  });
  $(".weichatshare").mouseenter(function(){
      $(this).css("background-color","#46BC45");
  });
  $(".weichatshare").mouseleave(function(){
      $(this).css("background-color","#fafafa");
  });
  $(".qqzoneshare").mouseenter(function(){
      $(this).css("background-color","#EFDC11");
  });
  $(".qqzoneshare").mouseleave(function(){
      $(this).css("background-color","#fafafa");
  });
  $(".search-tag").mouseenter(function(){
      $(this).css("background-color","#449d44");
      $(this).children("a").css("color","#fff");
  });
  $(".search-tag").mouseleave(function(){
      $(this).css("background-color","#CCF4D9");
      $(this).children("a").css("color","#449d44");
  });
 $("#morecomment-btn-block").mouseenter(function(){
      $(this).css("background-color","#f0f0f0");
  });
  $("#morecomment-btn-block").mouseleave(function(){
      $(this).css("background-color","white");
  });
 $(".articlecollection").mouseenter(function(){
      $(this).css("background-color","#3ca5f6");
      $(this).css("color","white");
  });
  $(".articlecollection").mouseleave(function(){
      $(this).css("background-color","#fafafa");
      $(this).css("color","#bbb");
  });
/*  $(".icon-dp").mouseenter(function(){
      $(this).css("background-position","-170px -223px");
  });
  $(".icon-dp").mouseleave(function(){
      $(this).css("background-position"," -170px -173px");
  });*/
  $(".btn-dp").mouseenter(function(){
      $(this).children().css("background-position","-170px -223px");
      $(this).css("color","#3ca5f6");
  });
  $(".btn-dp").mouseleave(function(){
      $(this).children().css("background-position"," -170px -173px");
      $(this).css("color","#bbb");
  });
  $(".icon-dp-positive").mouseenter(function(){
      $(this).css("background-position","-220px -223px");
  });
  $(".icon-dp-positive").mouseleave(function(){
      $(this).css("background-position","-220px -173px");
  });  
  $(".icon-dp-negtive").mouseenter(function(){
      $(this).css("background-position","-270px -221px");
  });
  $(".icon-dp-negtive").mouseleave(function(){
      $(this).css("background-position","-270px -171px");
  });  
});



$(function(){
  $("body").on("click", '.btn-dp', function(){
    $(this).next(".form-comment-reply").fadeToggle();
    x = $(this).parent().attr("id");
   $(this).next().children('#id_commentext').focus().text("@"+x+' ')
    /*$(this).next().children('#id_commentext').text("@"+x+' ')*/
  });
})