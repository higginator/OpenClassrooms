$(document).ready(function() {
	/*$("canvas").each(function() {
		var ctx = $(this).getContext("2d");
		ctx.font = "20px Georgia";
		ctx.fillText("Dream Xtreme", 20, 20);
	});*/
	var handle_normal = true;
	var input_time = $('#id_time').val();
	var input_day = $('#id_day').val();
	var input_building = $('#id_building').val();
	var input_number = $('#id_number').val();
	var input_ap = $('#id_ap').val();
	if (input_time && input_day && input_number && input_building) {
		var li = $('li');
		if (li.length > 0) {
			handle_normal = false;
			$('canvas').remove();
			$('#flash').html(input_number + ' ' + input_building + ' at ' + input_time + input_ap + ' on ' + input_day + ' is occupied.');
		};
	}
	if (handle_normal && input_time && input_number && input_building) {
		handle_normal = false;
		var weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];
		var building = $('#main_ul > ul');
		var times = $(building).children();
		for (var t=0; t < times.length; t++) {
			var data_day = ($(times[t]).attr('data-day'));
			if (weekdays.indexOf(data_day) > -1) {
				var index = weekdays.indexOf(data_day);
				weekdays.splice(index, 1);
			};
		};
		$('canvas').remove();
		if (weekdays) {
			var flash_days = "";
			for (var d=0; d < weekdays.length; d++) {
				flash_days = flash_days + weekdays[d] + ' ';
			}
		}
		$('#flash').html(input_number + ' ' + input_building + ' at ' + input_time + input_ap + ' is open on ' + flash_days);
	};

	if (handle_normal) {
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
		var all_buildings = $('#main_ul').children();
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
			//
			//for the UL with the same name as the canvas
			//grab the list items that represent that rooms times
			//and draw an appropriate clock
			//arc (x-center, y-center, radius, startAngle, endAngle, counterClockwise)
			var items = $(all_buildings[i]).children();
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
	};

	$('#main_ul').remove();
	$('#canvii_container').css('margin-top', '20px');
});