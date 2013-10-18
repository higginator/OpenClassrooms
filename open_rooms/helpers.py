def convert_to_day(num):
	mapping = {
				0: 'Monday',
				1: 'Tuesday',
				2: 'Wednesday',
				3: 'Thursday',
				4: 'Friday',
				5: 'Saturday',
				6: 'Sunday'
			}
	return mapping[num]