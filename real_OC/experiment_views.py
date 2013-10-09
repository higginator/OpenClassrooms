import urllib2, urllib
post_data = [('p_bldg', 'evans'), ('p_term', 'SP'), ('p_print_flag', 'Y')]
result = urllib2.urlopen('http://osoc.berkeley.edu/OSOC/osoc', urllib.urlencode(post_data))
content = result.read()
"""
	Content will contain all matches of building evans
	equivalent content to viewing the url at:
	http://osoc.berkeley.edu/OSOC/osoc?p_term=SP&p_bldg=evans&p_print_flag=Y
"""

"""
	So, we just need to subsititute all buildings to the tuple ('p_bldg', INSERT_BLDG_NAME_HERE).
	This will give us all matches of the print pages.
	From there, it is a matter of parsing to gather the appropriate information
"""