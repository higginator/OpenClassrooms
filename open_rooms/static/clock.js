$(document).ready(function() {
	/*$("canvas").each(function() {
		var ctx = $(this).getContext("2d");
		ctx.font = "20px Georgia";
		ctx.fillText("Dream Xtreme", 20, 20);
	});*/
	var canviis = $('canvas');
	var day = $('ul > li').attr('data-day');
	var ap = $('ul > li').attr('data-ap');
	var start_x = 100;
	var start_y = 80;
	var clock_radius = 45;
	var color;
	var endAngle;
	var oldEndAngle;
	for (var i=0; i< canviis.length; i++) {
		oldEndAngle = 0;
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
		//arc (x-center, y-center, radius, startAngle, endAngle, counterClockwise)
		for (var j=0; j < 25; j++) {
			endAngle = j/12*Math.PI;
			if (j % 2 == 0) {
				color = 'red';
			} else {
				color = 'green';
			}
			ctx.beginPath();
			ctx.arc(start_x, start_y, clock_radius, oldEndAngle, endAngle, false);
			oldEndAngle = endAngle;
			ctx.lineTo(start_x, start_y);
			ctx.fillStyle = color;
			ctx.fill();
			ctx.strokeStyle = color;
			ctx.stroke();
			ctx.closePath();
		};
	};
});