var beforePos = 0;


function ScrollAnime() {
    var elemTop = $('#up-section').offset().top;
	var scroll = $(window).scrollTop();
    if(scroll == beforePos) {
    }else if(elemTop > scroll || 0 > scroll - beforePos){
		$('#header').removeClass('UpMove');	
		$('#header').addClass('DownMove');
    }else {
        $('#header').removeClass('DownMove');
		$('#header').addClass('UpMove');
    }
    
    beforePos = scroll;
}



$(window).scroll(function () {
	ScrollAnime();
});

$(window).on('load', function () {
	ScrollAnime();
});

    var headerH = $("#header").outerHeight(true);
    $('#links li a').click(function () {
	var elmHash = $(this).attr('href'); 
	var pos = $(elmHash).offset().top-headerH;
	$('body,html').animate({scrollTop: pos}, 1000);
	return false;
});
