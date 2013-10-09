"""
buildingsfa12.db last updated: 06/29/2012
"""

import urllib2
import string
import time
from string import Template
import sqlite3

"""
Gets the source code of a web page
"""
def get_page(url):
    try:
        return urllib2.urlopen(url).read()
    except:
        return ""

"""
Returns 2 lists of building names: full names and abbreviations

fullName, abbr = buildingLists()
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

"""
Gets the source code of the web page, and checks whether it's an additional page
or not. For fall FL, spring SP, summer SU.
"""
def get_source(building, page, total):
    if " " in building:
        building = building.replace(" ", "+")
    if page > 0: #for search results >100
        url = Template("http://osoc.berkeley.edu/OSOC/osoc?p_term=FL&p_deptname=--+Choose+a+Department+Name+--&p_dept=&p_course=&p_presuf=--%20Choose%20a%20Course%20Prefix/Suffix%20--&p_title=&p_instr=&p_exam=&p_ccn=&p_day=&p_hour=&p_bldg=$bldg&p_units=&p_restr=&p_info=&p_updt=&p_classif=--+Choose+a+Course+Classification+--&p_session=&p_start_row=$nextstart&p_total_rows=$searchtotal")
        url = url.substitute(bldg = building, nextstart = page*100+1, searchtotal = total)
    else:
        url = Template("http://osoc.berkeley.edu/OSOC/osoc?y=0&p_term=FL&p_bldg=$bldg&p_deptname=--+Choose+a+Department+Name+--&p_classif=--+Choose+a+Course+Classification+--&p_presuf=--+Choose+a+Course+Prefix%2fSuffix+--&x=0")
        url = url.substitute(bldg = building)
    return get_page(url)

"""
>>> abbr[85]
'SODA'

soda = findTimes(abbr[85])
"""
def find_times(building):
    source = get_source(building, 0, 0)
    if source == '':
        return
    times = []
    
    #check for additional page results
    target = " match"
    num_index = source.find(target) - 1
    char = source[num_index]
    num = ''
    while char.isdigit():
        num = char + num
        num_index-=1
        char = source[num_index]
    if num:
        total = int(num)
    else:
        total = 0
    if total > 100: #if there are more than 100 results
        times += extract(source, building)
        pages = total // 100
        while pages > 0:
            source = get_source(building, pages, total)
            times += extract(source, building)
            pages-=1
    else:
        times += extract(source, building)
    return times

"""
Extract times from web page
"""
def extract(source, building):
    classes = []
    content = source[source.find(building) + len(building):]
    while content.find(building) != -1:
        initial_index = content.find(building)
        index = initial_index
        char = content[index]
        while char not in '>;:=': #searches backwards until encounters one of these symbols
            char = content[index]
            index-=1
        data = content[index + 2:initial_index + len(building)].strip()     
        if len(data) > len(building) + 1 and len(data) < len('MTuWThF 1230-1230P, 0000 ') + len(building): #filters invalid entries
            classes.append(data)
        content = content[initial_index + len(building):]
    return classes

"""
Organizes in to a workable data structure. {Classroom and Building: {Day:
[Hours]}}
#Still need to abstract further, into {Building: {Classroom: {Day: [Hours]}}}

sodaDictionary = timesDictionary(soda)
"""
def times_dictionary(times_list):
    result1 = {}
    for e in times_list:
        comma = e.find(",")
        if "UNSCHED" in e:
            first_blank = e.find(" ")
            second_blank = e.find(" ", first_blank + 1)
            classroom = e[first_blank + 1: second_blank]
            day_and_hours = 'unscheduled'
        else:
            second_blank = e.find(" ", comma + 2)
            classroom = e[comma + 2: second_blank]
            day_and_hours = e[:comma]
        if classroom in result1:
                result1[classroom].append(day_and_hours)
        else:
                result1[classroom] = [day_and_hours]
    result2 = {}
    every_day = ["M", "Tu", "W", "Th", "F"]
    for classroom in result1:
        result2[classroom] = {}
        for day_hour in result1[classroom]:
            for week_day in every_day:
                if week_day in day_hour:
                    whitespace = day_hour.find(" ")
                    hours = day_hour[whitespace+1:]
                    if week_day in result2[classroom]:
                        result2[classroom][week_day].append(hours)
                    else:
                        result2[classroom][week_day] = [hours]
    return result2

def generate_it():
    full_name, abbr = building_lists()
    big_dict = {}
    for abbreviation in abbr:
        big_dict[abbreviation] = times_dictionary(find_times(abbreviation))
        print abbreviation
    return big_dict
        

"""
Edit data to be SQL-friendly. Each entry will be [room, day, start, end] within a bigger []
"""
def dbFormatList(building):
    times = find_times(building)
    db_list = []
    for time in times:
        if "UNSCHED" in time:
            db_list.append([time[time.find(" "):-len(building)].strip(), "UNSCHED", "0", "0"])
        else:
            entry = db_format_entry(time, building)
            for ind_ent in entry:
                if ind_ent not in db_list: #prevents repeated entries
                    db_list.append(ind_ent)
    building = building.lower()
    if " " in building:
        building = building.replace(" ", "_")
        building = building.replace("\'", "")
    return building, db_list

"""
Split each entry into individual entries corresponding to just one day
"""
def db_format_entry(time, building):
    entries = []
    weekdays = ["M", "Tu", "W", "Th", "F"]
    for day in weekdays:
        if day in time[:time.find(" ")]:
            ind_ent = []
            ind_ent.append(time[time.find(",")+1:-len(building)].strip())
            ind_ent.append(day)
            num1 = time[time.find(" "):time.find("-")].strip()
            num2 = time[time.find("-")+1:time.find(",")]
            num1, num2 = time_of_day(num1, num2)
            ind_ent.append(num1)
            ind_ent.append(num2)
            entries.append(ind_ent)
    return entries

"""
Finds time of day and assigns an 'A' or 'P' to the first number
"""
def time_of_day(num1, num2):
	hour1, hour2 = "", ""
	if len(num1) == 3 or len(num1) == 1:
		hour1 = num1[0]
	if len(num1) == 4 or len(num1) == 2:
		hour1 = num1[:2]
	if len(num2[:-1]) == 3 or len(num2[:-1]) == 1:
		hour2 = num2[0]
	if len(num2[:-1]) == 4 or len(num2[:-1]) == 2:
		hour2 = num2[:2]
	if int(hour1) < int(hour2) and hour2 != "12":
		num1 += num2[-1:]
	else:
		if hour1 == "12":
			num1 += "P"
		else:
			num1 += "A"
	return num1, num2

#creates lists
#fullName, abbr = building_lists()
"""
#Putting list into buildings.db
conn = sqlite3.connect('buildingsfa12.db')
with conn:
    c = conn.cursor()
    for building in abbr:
        name, times = dbFormatList(building)
        c.execute("CREATE TABLE " + name + "(Room TEXT, Day TEXT, Start TEXT, End TEXT)")
        print "Table created: " + name
        for entry in times:
            c.execute("INSERT INTO " + name + " (Room, Day, Start, End) VALUES(\'" + entry[0] + "\', \'" + entry[1] + "\', \'" + entry[2] + "\', \'" + entry[3] + "\')")

"""

