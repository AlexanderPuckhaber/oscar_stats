import json
import csv


courses_json = '202102.json'
capacities_json = '202102_capacities.json'

with open(courses_json) as f:
    courses_data = json.load(f)

with open(capacities_json) as f:
    capacities_data = json.load(f)

caches = courses_data['caches']

course_mode_dict = {}

for course_mode in caches['attributes']:
    course_mode_dict[course_mode] = {}
course_mode_dict['total'] = {}

for label in course_mode_dict:
    course_mode_dict[label] = {'capacity': 0, 'enrollment': 0}
print(course_mode_dict)

# dict of array indices for csv labels
column_labels_dict = {}

for label in ['DEPT', 'NUM', 'CRN', 'CRED', 'CAMPUS', 'SCHED']:
    column_labels_dict[label] = len(column_labels_dict.keys())

#for scheduleType in courses_data['caches']['scheduleTypes']:
#    column_labels_dict[scheduleType] = len(column_labels_dict.keys())

for label in ['CAP', 'ENROL']:
    column_labels_dict[label] = len(column_labels_dict.keys())

for label in ['Hybrid Course', 'Remote Synchronous Course', 'Remote Asynchronous Course', 'Residential Course']:
    column_labels_dict[label] = len(column_labels_dict.keys())

print(column_labels_dict)

column_labels = []
for label in column_labels_dict:
    column_labels.insert(column_labels_dict[label], label)

print(column_labels)

columns = []
print(columns)

total_cap_sanity = 0
total_enroll_sanity = 0

def course_details_array_to_dict(course_details_array):
    course_details_dict = {}

    course_details_dict['crn'] = int(course_details_array[0])
    course_details_dict['meetings'] = course_details_array[1]
    course_details_dict['credits'] = course_details_array[2]
    course_details_dict['scheduleTypeIndex'] = course_details_array[3]
    course_details_dict['campusIndex'] = course_details_array[4]
    course_details_dict['attributeIndices'] = course_details_array[5]
    course_details_dict['gradeBasisIndex'] = course_details_array[6]

    return course_details_dict

for course in courses_data['courses']:
    #print(courses_data['courses'][course])

    dept = course.split(' ')[0]
    num = course.split(' ')[1]

    course_name =  courses_data['courses'][course][0]
    course_details = courses_data['courses'][course][1]

    new_row_pre = [0] * len(column_labels_dict.keys())

    new_row_pre[column_labels_dict['DEPT']] = dept
    new_row_pre[column_labels_dict['NUM']] = num


    for section_label in course_details:
        #print(section_label)

        details_array = course_details[section_label]
        #print(details_array)

        details_dict = course_details_array_to_dict(details_array)

        new_row = new_row_pre.copy()

        new_row[column_labels_dict['CRN']] = details_dict['crn']
        new_row[column_labels_dict['CRED']] = details_dict['credits']
        new_row[column_labels_dict['CAMPUS']] = courses_data['caches']['campuses'][details_dict['campusIndex']]

        new_row[column_labels_dict['SCHED']] = courses_data['caches']['scheduleTypes'][details_dict['scheduleTypeIndex']]

        if str(details_dict['crn']) in capacities_data.keys():
            details_dict['capacities'] = capacities_data[str(details_dict['crn'])]

            section_capacity = details_dict['capacities'][0]
            section_enrollment = details_dict['capacities'][1]

            new_row[column_labels_dict['CAP']] = section_capacity
            new_row[column_labels_dict['ENROL']] = section_enrollment


            for attrIdx in details_dict['attributeIndices']:
                attribute = courses_data['caches']['attributes'][attrIdx]
                if attribute in column_labels_dict:
                    new_row[column_labels_dict[attribute]] = 1

            # add capacities to running totals
            course_mode_dict_keys = list(course_mode_dict.keys())
            #print(course_mode_dict_keys)

            for idx in details_dict['attributeIndices'] + [len(course_mode_dict_keys) - 1]:
                course_mode_dict[course_mode_dict_keys[idx]]['capacity'] += section_capacity
                course_mode_dict[course_mode_dict_keys[idx]]['enrollment'] += section_enrollment

            total_cap_sanity += section_capacity
            total_enroll_sanity += section_enrollment

        else:
            details_dict['capacities'] = None

        print(new_row)
        #print(details_dict)

        columns.append(new_row)

for i in courses_data['caches']:
    pass
    print(i, courses_data['caches'][i])

for mode in course_mode_dict:
    print(mode, course_mode_dict[mode])

print('total_cap_sanity', total_cap_sanity)
print('total_enroll_sanity', total_enroll_sanity)

# write csv

with open('courses.csv', 'w+', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')

    writer.writerow(column_labels)
    for column in columns:
        writer.writerow(column)



