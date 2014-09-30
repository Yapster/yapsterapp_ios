function getBrowserWidth(){
	if (window.innerWidth){
		return window.innerWidth;}
		else if (document.documentElement && document.documentElement.clientWidth != 0){
			return document.documentElement.clientWidth;    }
			else if (document.body){return document.body.clientWidth;}      
			return 0;
	};

	function dynamicLayout(){
		var browserWidth = getBrowserWidth();
		if ( 641 > browserWidth){
			$('link').attr('href', '/static/yap/css/yap_mobile.css');
			alert("1");
			$('#header_text2').text("y");
			$('#download_icon_container').text("Download App");
		}
		else if ( 641 < browserWidth && browserWidth < 1019){
			$('link').attr('href', '/static/yap/css/yap_thin.css');
			alert("2");
			$('#header_text2').text("yapster");
			$('#download_icon_container').text("");
		}
	//Load Wide CSS Rules
	else if (1280 >= browserWidth  && browserWidth >= 1020){
		$('link').attr('href', '/static/yap/css/yap_wide.css');
		$('#header_text2').text("yapster");
		$('#download_icon_container').text("");
	}
	//Load Wider CSS Rules
	else if (browserWidth > 1280){
		$('link').attr('href', '/static/yap/css/yap_wider.css');
		$('#header_text2').text("yapster");
		$('#download_icon_container').text("");
	}
}
//addEvent() by John Resig
function addEvent( obj, type, fn ){ 
	if (obj.addEventListener){ 
		obj.addEventListener( type, fn, false );
	}
	else if (obj.attachEvent){ 
		obj["e"+type+fn] = fn; 
		obj[type+fn] = function(){ obj["e"+type+fn]( window.event ); } 
		obj.attachEvent( "on"+type, obj[type+fn] ); 
	} 
} //Run dynamicLayout function when page loads and when it resizes.
addEvent(window, 'load', dynamicLayout);
addEvent(window, 'resize', dynamicLayout);

$(document).ready(function(){
	var i = 1;
	setInterval(function() {
		$('#slideshow' + i.toString()).hide();
		i = i + 1;
		if (i == 5)
		{
			i = 1;
		}

		$('#slideshow' + i.toString()).show();
	}, 10000);

	$("#jquery_jplayer_1").jPlayer({
		ready: function () {
			$(this).jPlayer("setMedia", {
				mp3: $('#yap_audio_url').val()
			});
		},
		swfPath: "/js",
		supplied: "mp3"
	});

	//var yap_picture = $("#yap_picture")

	var yap_picture = $("#yap_picture")[0]; // Get my yap_picture elem
	var yap_picture_width, yap_picture_height;
	$("<img/>") // Make in memory copy of image to avoid css issues
	.attr("src", $(yap_picture).attr("src"))
	.load(function() {
	        yap_picture_width = this.width;   // Note: $(this).width() will not
	        yap_picture_height = this.height; // work for in memory images.
	        if (yap_picture_width > yap_picture_height) {
	        	yap_picture.className = "rotated_yap_picture";
	        	var yap_picture_container = $('#yap_picture_container')[0];
	        	yap_picture_container.className = "rotated_yap_picture"};
	        });
});

