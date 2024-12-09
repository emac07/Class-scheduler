import pandas as pd
import re

def parse_credits(credit_str):
    s = str(credit_str).lower().strip()
    s = s.replace('p/f', '').strip()

    if '/' in s:
        parts = s.split('/')
        for part in parts:
            match = re.search(r'(\d+)', part.strip())
            if match:
                return int(match.group(1))
        return 0
    else:
        match = re.search(r'(\d+)', s)
        if match:
            return int(match.group(1))
        return 0

def parse_schedule(day_time_str):
    if pd.isnull(day_time_str) or "TBD" in str(day_time_str):
        return [], (None, None)

    parts = day_time_str.split(' in ')
    time_part = parts[0]
    tokens = time_part.split()
    days = tokens[0]
    time_str = ' '.join(tokens[1:])
    time_range, ampm = time_str.rsplit(' ', 1)
    start_str, end_str = time_range.split('-')

    def convert_time(t_str, ampm_tag):
        hh, mm = t_str.split(':')
        hh = int(hh)
        mm = int(mm)
        if ampm_tag.upper() == "PM" and hh != 12:
            hh += 12
        if ampm_tag.upper() == "AM" and hh == 12:
            hh = 0
        return hh * 60 + mm

    start_minutes = convert_time(start_str, ampm)
    end_minutes = convert_time(end_str, ampm)
    day_list = list(days)
    return day_list, (start_minutes, end_minutes)

def check_conflicts(desired_crns, courses):
    selected = courses[courses['CRN'].isin(desired_crns)]
    schedules = []
    for idx, row in selected.iterrows():
        crn = row['CRN']
        dtr = row['DayTimeRoom']
        days, (start, end) = parse_schedule(dtr)
        schedules.append((crn, days, (start, end)))

    for i in range(len(schedules)):
        for j in range(i + 1, len(schedules)):
            c1, d1, t1 = schedules[i]
            c2, d2, t2 = schedules[j]
            if set(d1).intersection(d2):
                if t1[0] is not None and t2[0] is not None:
                    if (t1[0] < t2[1]) and (t2[0] < t1[1]):
                        print(f"Scheduling conflict: CRN {c1} conflicts with CRN {c2}")
                        return True
    return False

def check_aa_requirements(completed_crns, planned_crns, courses):
    all_taken = courses[courses['CRN'].isin(completed_crns + planned_crns)]
    total_credits = all_taken['Credits'].sum()
    seminar_credits = all_taken[all_taken['CourseNumber'].str.contains("FS 101|FS 100", na=False)]['Credits'].sum()
    fye_credits = all_taken[all_taken['CourseNumber'].str.contains("FYE", na=False)]['Credits'].sum()

    def division_credits(division_name):
        return all_taken[all_taken['Division'].str.contains(division_name, na=False)]['Credits'].sum()

    arts_credits = division_credits("Arts")
    lang_lit_credits = division_credits("Language and Literature")
    smc_credits = division_credits("Science, Math, and Computing")
    socs_credits = division_credits("Social Studies")
    cp_taken = all_taken[all_taken['Division'].str.contains("CP", na=False)]

    print("specifics of AA reqs")
    print(f"total credits: {total_credits} (Need 60)")
    print(f"sem credits: {seminar_credits} (Need 8)")
    print(f"FYE credits: {fye_credits} (Need 2)")
    print(f"art credits: {arts_credits} (Need 6)")
    print(f"lang & lit credits: {lang_lit_credits} (Need 6)")
    print(f"sci math comp credits: {smc_credits} (Need 6)")
    print(f"soc credits: {socs_credits} (Need 6)")
    print(f"cp taken: {len(cp_taken)} (Need 1)")

    if (total_credits >= 60 and seminar_credits >= 8 and fye_credits >= 2 and 
        arts_credits >= 6 and lang_lit_credits >= 6 and smc_credits >= 6 and socs_credits >= 6 and
        len(cp_taken) >= 1):
        print("AA reqs are met.")
    else:
        print("AA reqs are NOT met.")

if __name__ == "__main__":
    courses = pd.read_csv('courses.csv')
    courses.columns = ["CRN", "CourseNumber", "Title", "Credits", "DayTimeRoom", "Instructor", "Description", "Prerequisites", "Division"]
    courses['Credits'] = courses['Credits'].apply(parse_credits)

    print("Enter the CRNs of completed courses one at a time then type 'done':")
    completed = []
    while True:
        c = input().strip().lower()
        if c == 'done':
            break
        try:
            crn = int(c)
            completed.append(crn)
        except ValueError:
            print("enter a valid Crn")

    print("Enter the CRNs of the courses you want one at a time then type 'done':")
    desired = []
    while True:
        d = input().strip().lower()
        if d == 'done':
            break
        try:
            crn = int(d)
            desired.append(crn)
        except ValueError:
            print("enter a valid Crn")

    conflict = check_conflicts(desired, courses)
    if not conflict:
        print("No conflicts.")
    check_aa_requirements(completed, desired, courses)
