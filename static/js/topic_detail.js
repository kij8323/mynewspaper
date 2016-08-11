
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
  $(".jiathis_style_0").mouseenter(function(){
      $(this).children().children().children('.weichatshare').css("background-color","#46BC45");
  });
  $(".jiathis_style_0").mouseleave(function(){
      $(this).children().children().children('.weichatshare').css("background-color","#fafafa");
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
 $(".replyleftframe").mouseenter(function(){
      $(this).css("background-color","#3ca5f6");
      $(this).css("color","white");
  });
  $(".replyleftframe").mouseleave(function(){
      $(this).css("background-color","#fafafa");
      $(this).css("color","#bbb");
  });


 $(".paginator").mouseenter(function(){
      $(this).css("background-color","#67CA87");
      $(this).css("color","white");
  });
  $(".paginator").mouseleave(function(){
      $(this).css("background-color","#f5f5f5");
      $(this).css("color","#333");
  });


  $(".btn-dp").mouseenter(function(){
      $(this).children().css("background-position","-28px -37px");
      $(this).css("color","#3ca5f6");
  });
  $(".btn-dp").mouseleave(function(){
      $(this).children().css("background-position"," -28px -22px");
      $(this).css("color","#bbb");
  });
  $(".btn-dp-child").mouseenter(function(){
      $(this).children().css("background-position","-250px -79px");
      $(this).css("color","#3ca5f6");
  });
  $(".btn-dp-child").mouseleave(function(){
      $(this).children().css("background-position","-250px -92px");
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
  $(".btn-dp-reply").mouseenter(function(){
      $(this).children().css("background-position","-170px -223px");
      $(this).css("color","#3ca5f6");
  });
  $(".btn-dp-reply").mouseleave(function(){
      $(this).children().css("background-position","-170px -173px");
      $(this).css("color","#bbb");
  });  
 $(".articlecollection").mouseenter(function(){
      $(this).css("background-color","#3ca5f6");
      $(this).css("color","white");
  });
  $(".articlecollection").mouseleave(function(){
      $(this).css("background-color","#fafafa");
      $(this).css("color","#bbb");
  });

 $(".icon-delete").mouseenter(function(){
      $(this).css("background-position","-280px -434px");
  });
  $(".icon-delete").mouseleave(function(){
      $(this).css("background-position","-231px -434px");
  });
  
});


/*收起点评*/
$(function(){
  $("body").on("click", '.btn-dp', function(){
    var node = $(this).next(".form-comment-reply")
    /*commnetcount = node.children('.childcomment').length*/
    commnetcount = node.find('.childcomment').length
    $(this).next(".form-comment-reply").fadeToggle(function(){
      var display = node.css("display");
      if (display == 'none'){
        if (commnetcount == 0){
        $(this).parent().children('.btn-dp').html('<i class="icon-dp-checkbox"></i> 添加点评')
        }
        else{
        $(this).parent().children('.btn-dp').html('<i class="icon-dp-checkbox"></i> '+commnetcount+'条点评')
        }
      }
      else {
        $(this).parent().children('.btn-dp').html('<i class="icon-dp-checkbox"></i> 收起点评')
      }
    });
  });
})


/*回复评论按钮*/
/*$(function(){
  $("body").on("click", '.btn-dp-reply', function(){
    $(this).next().next(".form-comment-reply").fadeToggle();
    x = $(this).parent().attr("id");
    $(this).next().next('.form-comment-reply').children('#id_commentext').focus()
  });
})*/


/*回复评论的评论按钮*/
$(function(){
  $("body").on("click", '.btn-dp-child', function(){
    x = $(this).parent().attr("id");
    /*$(this).parent().parent().parent().children('#id_commentext').focus().append("@"+x+' ')*/
    $(this).parent().parent().parent().children('#id_commentext').focus().val($(this).parent().parent().parent().children('#id_commentext').val()+"@"+x+' ');
  });
})

