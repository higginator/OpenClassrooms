$(document).ready(function() {
	var buildingNames = ['BANCROFT LIB', 'BARKER', 'BARROWS', 'BECHTEL', 'BECHTEL AUD', 'BIRGE', 'BLUM', 'BOALT', 'BOT GARDEN', 'CALIFORNIA', 'CALVIN LAB', 'CAMPBELL', 'CAMPBELL ANX', 'CHANNING CTS', 'CHAVEZ', 'CHEIT', 'CORY', 'DAVIS', 'DOE LIBRARY', 'DONNER LAB', 'DURANT', 'DURHAM THTRE', 'DWINELLE', 'DWINELLE AN', 'ESHLEMAN', 'ETCHEVERRY', 'EVANS', 'FACULTY CLUB', 'FOOTHILL 1', 'FOOTHILL 4', 'GARDNERSTACK', 'GIANNINI', 'GIAUQUE', 'GILMAN', 'GPB', 'GSPP', 'HAAS', 'HAAS PAVIL', 'HANDBALL CTS', 'HARGROVE LIB', 'HAVILAND', 'HEARST ANNEX', 'HEARST EPOOL', 'HEARST GYM', 'HEARST MIN', 'HEARST POOL', 'HEARSTGYMCTS', 'HEARSTMUSEUM', 'HERTZ', 'HESSE', 'HILDEBRAND', 'HILGARD', "INTN'L HOUSE", 'KERR CAMPUS', 'KOSHLAND', 'KROEBER', 'LATIMER', 'LECONTE', 'LEWIS', 'LHS', 'LSA', 'MCCONE', 'MCENERNEY', 'MCLAUGHLIN', 'MEMORIAL STD', 'MINOR', 'MINOR ADDITN', 'MLK ST UNION', 'MOFFITT', 'MORGAN', 'MORRISON', 'MOSES', 'MULFORD', 'NORTH GATE', 'OBRIEN', 'OFF CAMPUS', 'PAC FILM ARC', 'PAULEY', 'PB GREENHOUS', 'PIMENTEL', 'PLAYHOUSE', 'RAQBALL CTS', 'REC SPRT FAC', 'RFS 112', 'RSF FLDHOUSE', 'SODA', 'SOUTH ANNEX', 'SOUTH HALL', 'SPIEKER POOL', 'SPROUL', 'SQUASH CTS', 'STANLEY', 'STARR LIB', 'STEPHENS', 'SUTARDJA DAI', 'TAN', 'TANG CENTER', 'TOLMAN', 'UCB ART MUSE', 'UNIT I CHNY', 'UNIT I CHRST', 'UNIT I CNTRL', 'UNIT II CNTL', 'UNIT II TOWL', 'UNIT II WADA', 'UNIT III DIN', 'UNIV HALL', 'VALLEY LSB', 'WELLMAN', 'WELLMAN CRT', 'WHEELER', 'WURSTER', 'ZELLERBACH', 'LI KA SHING'];
	$('#id_building').autocomplete({
		source: buildingNames
	});
	var searchDays = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY'];
	$('#id_day').autocomplete({
		source: searchDays
	});

	$('#big_button').click(function(e) {
		$('#flash').html('');
		var buildingVal = ($('#id_building').val()).toUpperCase();
		if (buildingVal) {
			if (buildingNames.indexOf(buildingVal) == -1) {
				var p = $('<p>').html(buildingVal + ' is not a building on the UC Berkeley campus.');
				$('#flash').append(p);
				e.preventDefault();
			};
		};
		var dayVal = ($('#id_day').val()).toUpperCase();
		if (dayVal) {
			if (searchDays.indexOf(dayVal) == -1) {
				var other_p = $('<p>').html(dayVal + ' is not a weekday.');
				$('#flash').append(other_p);
				e.preventDefault();
			};
		};
	});	
});