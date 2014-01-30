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
	var times;
	for (var i=0; i< canviis.length; i++) {
		times = [3, 330, 4, 430, 5, 530, 6, 630, 7, 730, 8, 830, 9, 930, 10, 1030, 11, 1130, 12, 1230, 1, 130, 2, 230];
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
		var building_name = $(canviis[i]).attr('name');
		var items = $('ul[name*=' + building_name + '] > li');
		for (var q=0; q < items.length; q++) {
			var position = times.indexOf(parseInt($(items[q]).html()));
			if (position > -1 ) {
				//false meaning half-hour is occupied
				times[position] = false;
			};
		};
		for (var z=0; z < times.length; z++) {
			if (typeof times[z] ==='number') {
				times[z] = true;
			};
		};

		for (var j=1; j < 25; j++) {
			endAngle = j/12*Math.PI;
			if (times[j-1]) {
				color = '#32CD32';
			} else {
				color = '#DC143C';
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

	$('#main_ul').remove();
	$('#canvii_container').css('margin-top', '20px');
});