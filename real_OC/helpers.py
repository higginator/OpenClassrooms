import urllib2, urllib
from open_rooms.views import *

def set_building(errors, form):
	if 'building' in errors:
		bldg = False
	else:
		bldg = form.cleaned_data['building']

def set_num(errors, form):
	if 'number' in errors:
		num = False
	else:
		num = form.cleaned_data['number']
	return num

def set_time(errors, form):
	if 'time' in errors:
		time = False
	else:
		time = form.cleaned_data['time']
	return time

def set_day(errors, form):
	if 'day' in errors:
		day = False
	else:
		day = form.cleaned_data['day']
	return day

def determine_request(bldg, time, day, num):
	#Quadruple Input
	if bldg and time and day and num:
		return get_building_time_day_number(bldg, time, day, num)
	#Triple Input
	elif bldg and time and day:
		return get_building_time_day(bldg, time, day)
	elif bldg and time and num:
		return get_building_time_number(bldg, time, num)
	elif bldg and day and num:
		return get_building_day_number(bldg, day, num)
	elif time and day and num:
		return get_day_time_number(day, time, num)
	#Double Input
	elif time and day:
		return get_time_day(time, day)
	elif bldg and day:
		return get_building_day(bldg, day)
	elif bldg and time:
		return get_building_time(bldg, time)
	elif bldg and num:
		return get_building_number(bldg, num)
	elif time and num:
		return get_time_number(time, num)
	elif day and num:
		return get_day_number(day, num)
	#Single Input
	elif bldg:
		return get_building(bldg)
	elif time:
		return get_time(time)
	elif day:
		return get_day(day)
	elif num:
		return get_number(num)
	#else
		#throw error


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
	abbr = abbr.replace(' ', '+')

#def store_room():
#	#
#	#

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

file = str("""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
   "http://www.w3.org/TR/html4/loose.dtd">
<HTML>
<FONT FACE="Helvetica, Arial, sans-serif" SIZE="1">
10-OCT-13, Spring 2014
<TABLE  BORDER="0" CELLSPACING="0" CELLPADDING="0">
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TR><TD COLSPAN="11"><BR><FONT FACE="Verdana" SIZE="-2"><B>AFRICAN AMERICAN STUDIES</B><BR></TD></TR><TR><TD colspan="11"><HR SIZE="1"></TD></TR><TR><TD>&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Control<BR>Number&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Course<BR>Number&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Section</TD><TD><FONT FACE="Verdana" SIZE="-2">Day-Hour</TD><TD><FONT FACE="Verdana" SIZE="-2">Room</TD><TD><FONT FACE="Verdana" SIZE="-2">Course Title</TD><TD><FONT FACE="Verdana" SIZE="-2">Unit<BR>Credit&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Instructor</TD><TD><FONT FACE="Verdana" SIZE="-2">Exam<BR>Group&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Restrictions</TD></TR><TR><TD colspan="11"><HR SIZE="1"></TD></TR></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">00512&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;R1B</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">101&nbsp;DIS&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">W 11-12P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 237 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Freshman Composition</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">NANDA, A</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD>&nbsp;</TD><TD>&nbsp;</TD><TD>&nbsp;</TD><TD colspan="9"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"><B>Note: </B>SATISFIES READING AND COMPOSITION REQUIREMENT;&nbsp</TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">00677&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">P&nbsp;&nbsp;159</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">002&nbsp;LEC&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">TuTh 930-11A&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 241 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Special Topics in African American Literature</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">3</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">VINCENT, F</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">10</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD>&nbsp;</TD><TD>&nbsp;</TD><TD>&nbsp;</TD><TD colspan="9"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"><B>Note: </B>"The Anti Apartheid Movement: Global and Local"&nbsp</TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TR><TD COLSPAN="11"><BR><FONT FACE="Verdana" SIZE="-2"><B>BIOENGINEERING</B><BR></TD></TR><TR><TD colspan="11"><HR SIZE="1"></TD></TR><TR><TD>&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Control<BR>Number&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Course<BR>Number&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Section</TD><TD><FONT FACE="Verdana" SIZE="-2">Day-Hour</TD><TD><FONT FACE="Verdana" SIZE="-2">Room</TD><TD><FONT FACE="Verdana" SIZE="-2">Course Title</TD><TD><FONT FACE="Verdana" SIZE="-2">Unit<BR>Credit&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Instructor</TD><TD><FONT FACE="Verdana" SIZE="-2">Exam<BR>Group&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Restrictions</TD></TR><TR><TD colspan="11"><HR SIZE="1"></TD></TR></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">06524&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">P&nbsp;&nbsp;101</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">001&nbsp;LEC&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">TuTh 330-5P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 247 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Instrumentation in Biology and Medicine</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">4</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">CONOLLY, S</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">20</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">                                                                                                                                         BY CATEGORY</TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD>&nbsp;</TD><TD>&nbsp;</TD><TD>&nbsp;</TD><TD colspan="9"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"><B>Note: </B>($50 Course Materials Fee - subject to change)&nbsp</TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">06635&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">P&nbsp;&nbsp;163</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">001&nbsp;LEC&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">TuTh 930-11A&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 247 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Principles of Molecular and Cellular Biophotonics</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">4</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">MARRIOTT, G</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">NONE</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">                                                                                                                                         BY CATEGORY</TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">06638&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;163</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">101&nbsp;DIS&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">F 4-5P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 247 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Principles of Molecular and Cellular Biophotonics</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">07103&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">P&nbsp;&nbsp;263</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">001&nbsp;LEC&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">TuTh 930-11A&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 247 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Principles of Molecular and Cellular Biophotonics</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">4</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">MARRIOTT, G</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">10</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TR><TD COLSPAN="11"><BR><FONT FACE="Verdana" SIZE="-2"><B>GROUP IN BUDDHIST STUDIES</B><BR></TD></TR><TR><TD colspan="11"><HR SIZE="1"></TD></TR><TR><TD>&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Control<BR>Number&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Course<BR>Number&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Section</TD><TD><FONT FACE="Verdana" SIZE="-2">Day-Hour</TD><TD><FONT FACE="Verdana" SIZE="-2">Room</TD><TD><FONT FACE="Verdana" SIZE="-2">Course Title</TD><TD><FONT FACE="Verdana" SIZE="-2">Unit<BR>Credit&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Instructor</TD><TD><FONT FACE="Verdana" SIZE="-2">Exam<BR>Group&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Restrictions</TD></TR><TR><TD colspan="11"><HR SIZE="1"></TD></TR></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">07918&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;C128</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">103&nbsp;DIS&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Tu 1-2P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 237 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Buddhism in Contemporary Society</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TR><TD COLSPAN="11"><BR><FONT FACE="Verdana" SIZE="-2"><B>CHEMICAL & BIOMOLECULAR ENGINEERING</B><BR></TD></TR><TR><TD colspan="11"><HR SIZE="1"></TD></TR><TR><TD>&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Control<BR>Number&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Course<BR>Number&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Section</TD><TD><FONT FACE="Verdana" SIZE="-2">Day-Hour</TD><TD><FONT FACE="Verdana" SIZE="-2">Room</TD><TD><FONT FACE="Verdana" SIZE="-2">Course Title</TD><TD><FONT FACE="Verdana" SIZE="-2">Unit<BR>Credit&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Instructor</TD><TD><FONT FACE="Verdana" SIZE="-2">Exam<BR>Group&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Restrictions</TD></TR><TR><TD colspan="11"><HR SIZE="1"></TD></TR></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">10684&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">P&nbsp;&nbsp;C295Z</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">001&nbsp;LEC&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">TuTh 1230-2P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 247 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Energy Solutions: Carbon Capture and Sequestration</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">3</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">SMIT, B</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">NONE</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD>&nbsp;</TD><TD>&nbsp;</TD><TD>&nbsp;</TD><TD colspan="9"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"><B>Note: </B>Cross-listed with Chemistry C236 section 1 and Earth and Planetary Science C295Z section 1.&nbsp</TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TR><TD COLSPAN="11"><BR><FONT FACE="Verdana" SIZE="-2"><B>CHEMISTRY</B><BR></TD></TR><TR><TD colspan="11"><HR SIZE="1"></TD></TR><TR><TD>&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Control<BR>Number&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Course<BR>Number&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Section</TD><TD><FONT FACE="Verdana" SIZE="-2">Day-Hour</TD><TD><FONT FACE="Verdana" SIZE="-2">Room</TD><TD><FONT FACE="Verdana" SIZE="-2">Course Title</TD><TD><FONT FACE="Verdana" SIZE="-2">Unit<BR>Credit&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Instructor</TD><TD><FONT FACE="Verdana" SIZE="-2">Exam<BR>Group&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Restrictions</TD></TR><TR><TD colspan="11"><HR SIZE="1"></TD></TR></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">11603&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;C130</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">105&nbsp;DIS&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">F 10-11A&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 285 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Biophysical Chemistry: Physical Principles and the ...</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">12464&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">P&nbsp;&nbsp;C236</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">001&nbsp;LEC&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">TuTh 1230-2P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 247 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Energy Solutions: Carbon Capture and Sequestration</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">3</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">SMIT, B</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">NONE</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD>&nbsp;</TD><TD>&nbsp;</TD><TD>&nbsp;</TD><TD colspan="9"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"><B>Note: </B>Cross-listed with Chemical & Biomolecular Engineering C295Z section 1 and Earth and Planetary Science C295Z section 1.&nbsp</TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TR><TD COLSPAN="11"><BR><FONT FACE="Verdana" SIZE="-2"><B>CIVIL AND ENVIRONMENTAL ENGINEERING</B><BR></TD></TR><TR><TD colspan="11"><HR SIZE="1"></TD></TR><TR><TD>&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Control<BR>Number&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Course<BR>Number&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Section</TD><TD><FONT FACE="Verdana" SIZE="-2">Day-Hour</TD><TD><FONT FACE="Verdana" SIZE="-2">Room</TD><TD><FONT FACE="Verdana" SIZE="-2">Course Title</TD><TD><FONT FACE="Verdana" SIZE="-2">Unit<BR>Credit&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Instructor</TD><TD><FONT FACE="Verdana" SIZE="-2">Exam<BR>Group&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Restrictions</TD></TR><TR><TD colspan="11"><HR SIZE="1"></TD></TR></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">14108&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">P&nbsp;&nbsp;120</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">001&nbsp;LEC&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">MWF 11-12P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 277 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Structural Engineering</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">3</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">PANAGIOTOU, M A</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">8</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">14126&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">P&nbsp;&nbsp;130N</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">001&nbsp;LEC&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">MW 1-2P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 277 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Mechanics of Structures</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">3</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">GOVINDJEE, S</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">5</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TR><TD COLSPAN="11"><BR><FONT FACE="Verdana" SIZE="-2"><B>EARTH AND PLANETARY SCIENCE</B><BR></TD></TR><TR><TD colspan="11"><HR SIZE="1"></TD></TR><TR><TD>&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Control<BR>Number&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Course<BR>Number&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Section</TD><TD><FONT FACE="Verdana" SIZE="-2">Day-Hour</TD><TD><FONT FACE="Verdana" SIZE="-2">Room</TD><TD><FONT FACE="Verdana" SIZE="-2">Course Title</TD><TD><FONT FACE="Verdana" SIZE="-2">Unit<BR>Credit&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Instructor</TD><TD><FONT FACE="Verdana" SIZE="-2">Exam<BR>Group&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Restrictions</TD></TR><TR><TD colspan="11"><HR SIZE="1"></TD></TR></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">19372&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">P&nbsp;&nbsp;C295Z</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">001&nbsp;LEC&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">TuTh 1230-2P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 247 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Energy Solutions: Carbon Capture and Sequestration</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">3</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">REIMER, J A</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">NONE</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD>&nbsp;</TD><TD>&nbsp;</TD><TD>&nbsp;</TD><TD colspan="9"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"><B>Note: </B>Cross-listed with Chemistry C236 section 1 and Chemical & Biomolecular Engineering C295Z section 1.&nbsp</TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TR><TD COLSPAN="11"><BR><FONT FACE="Verdana" SIZE="-2"><B>EAST ASIAN LANGUAGES AND CULTURES</B><BR></TD></TR><TR><TD colspan="11"><HR SIZE="1"></TD></TR><TR><TD>&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Control<BR>Number&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Course<BR>Number&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Section</TD><TD><FONT FACE="Verdana" SIZE="-2">Day-Hour</TD><TD><FONT FACE="Verdana" SIZE="-2">Room</TD><TD><FONT FACE="Verdana" SIZE="-2">Course Title</TD><TD><FONT FACE="Verdana" SIZE="-2">Unit<BR>Credit&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Instructor</TD><TD><FONT FACE="Verdana" SIZE="-2">Exam<BR>Group&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Restrictions</TD></TR><TR><TD colspan="11"><HR SIZE="1"></TD></TR></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">20530&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;C128</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">103&nbsp;DIS&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Tu 1-2P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 237 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Buddhism in Contemporary Society</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TR><TD COLSPAN="11"><BR><FONT FACE="Verdana" SIZE="-2"><B>ECONOMICS</B><BR></TD></TR><TR><TD colspan="11"><HR SIZE="1"></TD></TR><TR><TD>&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Control<BR>Number&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Course<BR>Number&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Section</TD><TD><FONT FACE="Verdana" SIZE="-2">Day-Hour</TD><TD><FONT FACE="Verdana" SIZE="-2">Room</TD><TD><FONT FACE="Verdana" SIZE="-2">Course Title</TD><TD><FONT FACE="Verdana" SIZE="-2">Unit<BR>Credit&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Instructor</TD><TD><FONT FACE="Verdana" SIZE="-2">Exam<BR>Group&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Restrictions</TD></TR><TR><TD colspan="11"><HR SIZE="1"></TD></TR></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">22591&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;131</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">106&nbsp;DIS&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">M 2-3P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 237 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Public Economics</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TR><TD COLSPAN="11"><BR><FONT FACE="Verdana" SIZE="-2"><B>ELECTRICAL ENGINEERING</B><BR></TD></TR><TR><TD colspan="11"><HR SIZE="1"></TD></TR><TR><TD>&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Control<BR>Number&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Course<BR>Number&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Section</TD><TD><FONT FACE="Verdana" SIZE="-2">Day-Hour</TD><TD><FONT FACE="Verdana" SIZE="-2">Room</TD><TD><FONT FACE="Verdana" SIZE="-2">Course Title</TD><TD><FONT FACE="Verdana" SIZE="-2">Unit<BR>Credit&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Instructor</TD><TD><FONT FACE="Verdana" SIZE="-2">Exam<BR>Group&nbsp;&nbsp;</TD><TD><FONT FACE="Verdana" SIZE="-2">Restrictions</TD></TR><TR><TD colspan="11"><HR SIZE="1"></TD></TR></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25006&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;20</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">010&nbsp;LAB&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">M 12-3P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 105 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Structure and Interpretation of Systems and Signals</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25009&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;20</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">011&nbsp;LAB&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">M 3-6P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 105 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Structure and Interpretation of Systems and Signals</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25012&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;20</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">012&nbsp;LAB&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Tu 9-12P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 105 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Structure and Interpretation of Systems and Signals</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25015&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;20</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">013&nbsp;LAB&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Tu 3-6P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 105 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Structure and Interpretation of Systems and Signals</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25018&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;20</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">014&nbsp;LAB&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Th 3-6P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 105 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Structure and Interpretation of Systems and Signals</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25021&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;20</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">015&nbsp;LAB&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">F 9-12P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 105 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Structure and Interpretation of Systems and Signals</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25024&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;20</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">017&nbsp;LAB&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">F 12-3P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 105 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Structure and Interpretation of Systems and Signals</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25027&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;20</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">101&nbsp;DIS&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">W 9-10A&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 241 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Structure and Interpretation of Systems and Signals</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25030&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;20</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">102&nbsp;DIS&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">W 10-11A&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 285 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Structure and Interpretation of Systems and Signals</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25033&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;20</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">103&nbsp;DIS&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">W 11-12P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 285 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Structure and Interpretation of Systems and Signals</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25036&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;20</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">104&nbsp;DIS&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">W 12-1P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 241 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Structure and Interpretation of Systems and Signals</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25039&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;20</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">105&nbsp;DIS&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">W 1-2P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 241 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Structure and Interpretation of Systems and Signals</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25042&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;20</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">106&nbsp;DIS&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">W 2-3P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 285 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Structure and Interpretation of Systems and Signals</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25045&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;20</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">107&nbsp;DIS&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">W 4-5P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 241 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Structure and Interpretation of Systems and Signals</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25048&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">P&nbsp;&nbsp;24</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">001&nbsp;SEM&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">W 10-11A&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 125 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Freshman Seminar</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">1</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">BOKOR, J</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">TBA</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">                                                                                                                                         BY CATEGORY</TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25057&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;40</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">102&nbsp;DIS&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">M 9-10A&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 247 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Introduction to Microelectronic Circuits</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25060&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;40</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">103&nbsp;DIS&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">W 2-3P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 241 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Introduction to Microelectronic Circuits</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25063&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;40</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">104&nbsp;DIS&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">W 3-4P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 241 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Introduction to Microelectronic Circuits</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25066&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;40</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">105&nbsp;DIS&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">W 4-5P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 289 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Introduction to Microelectronic Circuits</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25069&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;40</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">106&nbsp;DIS&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">W 5-6P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 241 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Introduction to Microelectronic Circuits</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25072&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;40</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">010&nbsp;LAB&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">M 5-8P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 140 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Introduction to Microelectronic Circuits</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">MAHARBIZ, M M</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25075&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;40</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">011&nbsp;LAB&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Tu 8-11A&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 140 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Introduction to Microelectronic Circuits</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">MAHARBIZ, M M</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25078&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;40</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">012&nbsp;LAB&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Tu 11-2P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 140 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Introduction to Microelectronic Circuits</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">MAHARBIZ, M M</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25081&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;40</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">013&nbsp;LAB&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Tu 2-5P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 140 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Introduction to Microelectronic Circuits</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">MAHARBIZ, M M</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25084&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;40</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">014&nbsp;LAB&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Th 8-11A&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 140 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Introduction to Microelectronic Circuits</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">MAHARBIZ, M M</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25087&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;40</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">015&nbsp;LAB&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Th 11-2P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 140 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Introduction to Microelectronic Circuits</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">MAHARBIZ, M M</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25090&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;40</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">016&nbsp;LAB&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Th 2-5P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 140 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Introduction to Microelectronic Circuits</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">MAHARBIZ, M M</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25093&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;40</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">017&nbsp;LAB&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">F 2-5P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 140 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Introduction to Microelectronic Circuits</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">MAHARBIZ, M M</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25099&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">P&nbsp;&nbsp;98</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">001&nbsp;GRP&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">W 8-10P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 125 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Directed Group Study for Undergraduates</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">1-4: PF</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">NGUYEN, C T</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">NONE</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">  FR, SO</TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">P&nbsp;&nbsp;98</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">002&nbsp;GRP&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">M 6-8P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 521 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Directed Group Study for Undergraduates</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">1-4: PF</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">ABBEEL, P</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">NONE</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">  FR, SO</TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD>&nbsp;</TD><TD>&nbsp;</TD><TD>&nbsp;</TD><TD colspan="9"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"><B>Note: </B>"Pioneers in Engineering"&nbsp</TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">P&nbsp;&nbsp;98</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">003&nbsp;GRP&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Th 6-8P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 521 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Directed Group Study for Undergraduates</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">1-4: PF</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">ABBEEL, P</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">NONE</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">  FR, SO</TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD>&nbsp;</TD><TD>&nbsp;</TD><TD>&nbsp;</TD><TD colspan="9"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"><B>Note: </B>"Pioneers in Engineering"&nbsp</TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25114&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;105</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">010&nbsp;LAB&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">M 10-1P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 125 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Microelectronic Devices and Circuits</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25117&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;105</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">011&nbsp;LAB&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Tu 9-12P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 125 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Microelectronic Devices and Circuits</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25120&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;105</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">012&nbsp;LAB&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">W 3-6P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 125 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Microelectronic Devices and Circuits</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25123&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;105</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">101&nbsp;DIS&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">M 4-5P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 247 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Microelectronic Devices and Circuits</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25126&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;105</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">102&nbsp;DIS&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">W 11-12P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 241 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Microelectronic Devices and Circuits</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25129&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">P&nbsp;&nbsp;117</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">001&nbsp;LEC&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">MW 4-530P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 299 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Electromagnetic Fields and Waves</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">4</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">CHANG-HASNAIN, C J</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">17</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25132&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;117</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">101&nbsp;DIS&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">F 4-5P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 299 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Electromagnetic Fields and Waves</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25135&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;117</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">010&nbsp;LAB&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Tu 2-330P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 111 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Electromagnetic Fields and Waves</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25138&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">P&nbsp;&nbsp;118</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">001&nbsp;LEC&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">WF 1-230P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 521 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Introduction to Optical Engineering</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">3</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">WALLER, L</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">5</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25141&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;118</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">101&nbsp;DIS&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Tu 4-5P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 299 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Introduction to Optical Engineering</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25144&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">P&nbsp;&nbsp;120</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">001&nbsp;LEC&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">TuTh 4-6P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 277 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Signals and Systems</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">4</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">FEARING, R S</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">20</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25147&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;120</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">101&nbsp;REC&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">F 1-2P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 241 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Signals and Systems</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25150&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;120</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">102&nbsp;REC&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">F 2-3P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 241 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Signals and Systems</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25153&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;120</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">103&nbsp;REC&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">F 3-4P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 241 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Signals and Systems</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25159&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;122</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">101&nbsp;DIS&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Tu 4-5P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 285 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Introduction to Communication Networks</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25165&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">P&nbsp;&nbsp;123</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">001&nbsp;LEC&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">MWF 9-10A&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 521 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Digital Signal Processing</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">4</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">LUSTIG, S M</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">4</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25171&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">P&nbsp;&nbsp;126</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">001&nbsp;LEC&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">TuTh 930-11A&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 285 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Probability and Random Processes</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">4</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">WALRAND, J C</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">10</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25174&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;126</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">101&nbsp;DIS&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Th 1-2P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 285 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Probability and Random Processes</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25177&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">P&nbsp;&nbsp;127</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">001&nbsp;LEC&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">TuTh 1230-2P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 241 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Optimization Models in Engineering</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">4</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">EL GHAOUI, L</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">NONE</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25180&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;127</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">101&nbsp;DIS&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">W 12-1P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 285 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Optimization Models in Engineering</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25192&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">P&nbsp;&nbsp;130</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">001&nbsp;LEC&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">TuTh 330-5P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 241 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Integrated-Circuit Devices</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">4</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">SALAHUDDIN, S</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">20</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25195&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;130</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">101&nbsp;DIS&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">M 4-5P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 289 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Integrated-Circuit Devices</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25198&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">S&nbsp;&nbsp;130</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">102&nbsp;DIS&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">M 10-11A&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 285 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Integrated-Circuit Devices</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25201&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">P&nbsp;&nbsp;134</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">001&nbsp;LEC&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">MW 11-1230P&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 299 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Fundamentals of Photovoltaic Devices</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">4</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">ARIAS, A C</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">18</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>
<TD VALIGN="TOP" ALIGN="LEFT"><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">25210&nbsp;&nbsp;</TD><TD VALIGN="TOP" ALIGN="LEFT"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">P&nbsp;&nbsp;137B</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">001&nbsp;LEC&nbsp;&nbsp;</TD><TD VALIGN="TOP" NOWRAP><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">TuTh 930-11A&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"> 521 CORY&nbsp;&nbsp;</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">Introduction to Electric Power Systems</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">4</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">VON MEIER, A</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4">10</TD><TD VALIGN="TOP"><FONT FACE="Helvetica, Arial, sans-serif" SIZE="-4"></TD></TD>
</TR>
<TR>""")