import urllib2, urllib


"""
	Will contain all matches of a BUILDING
	equivalent content to viewing the url at:
	http://osoc.berkeley.edu/OSOC/osoc?p_term=SP&p_bldg={{BUILDING}}&p_print_flag=Y
"""
def get_building_source(building):
	path = 'http://osoc.berkeley.edu/OSOC/osoc'
	post_data = [('p_term', 'SP'), ('p_print_flag', 'Y')]
	query_param = 'p_bldg'
	post_data.append((query_param, building))
	source = urllib2.urlopen(path, urllib.urlencode(post_data)).read()
	return source
