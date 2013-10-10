import urllib2, urllib

"""
	Returns the source code of a web page
"""
def get_page(url, post_data=''):
    try:
        return urllib2.urlopen(url, urllib.urlencode(post_data)).read()
    except:
        return ''


"""
	Returns all matches of a BUILDING in a given SEMESTER
	equivalent content to viewing the url at:
	http://osoc.berkeley.edu/OSOC/osoc?p_term={{SEMESTER}}&p_bldg={{BUILDING}}&p_print_flag=Y
"""
def get_building_source(semester, building):
	#semester should be two chars: SP, SU, or FL
	#one path for all requests
	path = 'http://osoc.berkeley.edu/OSOC/osoc'
	post_data = [('p_term', semester), ('p_print_flag', 'Y'), ('p_bldg', building)]
	source = get_page(path, post_data)
	return source

"""
	Replaces spaces with '+'. Needed for query parameter passing.
"""
def format(abbr):
	#Need to send query paramaters with + instead of ' '
	#
	#For all items in a list
	#	If there are spaces separating words
	#		replace the space with a +

def store_room():
	#
	#

def store_all_rooms(semester):
	full_name, abbreviations = building_lists()
	format(abbr)
	for abbr in abbreviations:
		source = get_building_source(semester, abbr)
		#For all rooms:
		#	Find all instances of a room from the source.
		#	Create a room object from these instances
		#	store room object in database

"""
	Returns 2 lists of building names: full names and abbreviations

	full_name, abbr = building_lists()
"""
def building_lists():
    source = get_page("http://registrar.berkeley.edu/Default.aspx?PageID=bldgabb.html")
    #make 2 lists
    full_name = []
    abbr = []

    #look for tags starting with <td valign
    target = "<td valign"
    target_index = source.find(target)
    content = source[target_index:]

    #extract building names
    while target_index != -1:
        word_start = content.find(">") + 1
        word = content[word_start:content.find("</td>")]
        if word.isupper() or word == "FOOTHILL 1" or word == "FOOTHILL 4":
            abbr.append(word)
        else:
            full_name.append(word)
        content = content[content.find("/td"):]
        target_index = content.find(target)
        content = content[target_index:]
    full_name.append("Li Ka Shing Center")
    abbr.append("LI KA SHING")
    return full_name, abbr