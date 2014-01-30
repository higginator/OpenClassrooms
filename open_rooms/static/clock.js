$(document).ready(function() {
	/*$("canvas").each(function() {
		var ctx = $(this).getContext("2d");
		ctx.font = "20px Georgia";
		ctx.fillText("Dream Xtreme", 20, 20);
	});*/
	var canviis = $('canvas');
	var day = $('ul > li').attr('data-day');
	var ap = $('ul > li').attr('data-ap');
	for (var i=0; i< canviis.length; i++) {
		var ctx = canviis[i].getContext("2d");
		ctx.font = "bold 16px sans-serif";
		ctx.fillText($(canviis[i]).attr("name"), 100, 20);
		if (day) {
			ctx.fillText(day, 180, 80);
			ctx.fillText(ap + 'M Clock', 180, 100);
		};
		//for the UL with the same name as the canvas
		//grab the list items that represent that rooms times
		//and draw an appropriate clock

		ctx.beginPath();
		//arc (x-center, y-center, radius, startAngle, endAngle, counterClockwise)
		ctx.arc(100, 80, 45, 0, 2* Math.PI, false);
		ctx.fillStyle = 'green';
		ctx.fill();
		ctx.closePath();
	};
});