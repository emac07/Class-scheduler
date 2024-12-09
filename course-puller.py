import requests
from bs4 import BeautifulSoup
import csv

url = "https://portal.simons-rock.edu/cg/Spring2025CourseGuide.php"
html_content = requests.get(url).text
soup = BeautifulSoup(html_content, 'html.parser')
rows = soup.find('table', id='myTable').find_all('tr') if soup.find('table', id='myTable') else soup.find_all('tr')

course_data = []
i = 0
while i < len(rows):
    tr = rows[i]
    crn_td = tr.find('td', align='CENTER')
    if crn_td and crn_td.get_text(strip=True).isdigit():
        tds = [x for x in tr.find_all('td') if x.get('style') != 'display:none']
        if len(tds) < 8:
            i += 1
            continue
        
        crn, course_number, title, credits, day_time_room, instructor = (
            tds[0].get_text(strip=True),
            tds[1].get_text(strip=True),
            tds[3].get_text(strip=True),
            tds[5].get_text(strip=True),
            tds[6].get_text(strip=True),
            tds[7].get_text(strip=True),
        )

        course_description, prerequisites, division_requirement = "", "", ""
        if i + 1 < len(rows):
            desc_div = rows[i + 1].find('div', style="display:none")
            if desc_div:
                full_desc = desc_div.get_text(" ", strip=True)
                if "----This course counts towards the" in full_desc:
                    prefix = "----This course counts towards the "
                    suffix = " Division requirement"
                    division_requirement = full_desc.split(prefix)[1].split(suffix)[0].strip()
                    full_desc = full_desc.split(prefix)[0].strip()
                if "No prerequisites." in full_desc:
                    course_description, prerequisites = full_desc.split("No prerequisites.")[0].strip(), "No prerequisites."
                elif "Prerequisites:" in full_desc:
                    course_description = full_desc.split("Prerequisites:")[0].strip()
                    prerequisites = full_desc.split("Prerequisites:")[1].split("<b>----")[0].strip()
                else:
                    course_description = full_desc.strip()
        
        course_data.append({
            'CRN': crn,
            'Course Number': course_number,
            'Title': title,
            'Credits': credits,
            'Day/Time/Room': day_time_room,
            'Instructor': instructor,
            'Description': course_description,
            'Prerequisites': prerequisites,
            'Division Requirement': division_requirement
        })
        i += 2
    else:
        i += 1

with open('courses.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=[
        'CRN', 'Course Number', 'Title', 'Credits', 'Day/Time/Room',
        'Instructor', 'Description', 'Prerequisites', 'Division Requirement'
    ])
    writer.writeheader()
    writer.writerows(course_data)

