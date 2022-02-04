var current;
$.scrollify({
  section:".box",
  setHeights:false,
  before:function(i,box){
    current=i;
  },
});
$(window).on('resize',function(){
  if(current){
    var currentSrcl=$('.box').eq(current).offset().top;
    $(window).scrollTop(currentSrcl);
  }
});