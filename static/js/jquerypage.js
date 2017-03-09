

function rePosition(){
   $('.danmu').each(function(){
    $(this).css({fontSize:getFontsize(),color:getRandomColor()});
    w = $(this).css('width')
    $(this).css('left',-parseFloat(w)+'px');
});
}


$(function(){
  rePosition()
});



function getRandomColor(){
return '#' + (function(h){
return new Array(7 - h.length).join("0") + h
}
)((Math.random() * 0x1000000 << 0).toString(16))
}

function getFontsize(){
Math.random()*12
var num = Math.random()*12 + 12;
num = parseInt(num, 10);
return num+'px'
}


$(function(){
$('.danmubar').click(function(){
  i = 1
   $('.danmu').each(function(){
      wwidth = document.documentElement.clientWidth
      wheight = document.documentElement.clientHeight 
      y = parseFloat($(this).prev('.danmu').css('top'))
      if ( y > wheight-100) 
      {
       y = 50
       i = i+0.8
      };
      $(this).css('top',y+30+'px');
      $(this).show()
      $(this).animate({left: wwidth},i*12000,function(){
      $(this).css('display','none');
      $(this).css('left',0+'px');
      w = $(this).css('width')
      $(this).css('left',-parseFloat(w)+'px');
      });
   })
})
})


