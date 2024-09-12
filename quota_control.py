from datetime import datetime
from extract_teachers_infos_and_slots import extract_and_create_teachers_struct_for_graph
from extract_students_infos_and_slots import extract_students_infos_and_slots
from get_weeks_and_years_involved import get_weeks_and_years_involved
from update_teachers_availabilities_with_slot_taken import aggregate_slots
from airtable import Airtable
import pprint
from utils.date import get_number_of_the_week
from filter_teacher_availabilities import filter_teacher_availabilities_by_date
from get_teachers_email_list import get_teachers_email_list

def control_quota_teachers_availabilities_with_slot_taken(teachers_graph_obj, students_infos, weeks_involved):
    
    DEBUG = False
    quota_control = []

    if DEBUG:    
        print("PRINT TO EXTRACT OBJECT")
        print("teacher_graph_obj\n")
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(teachers_graph_obj)
        print("students_infos\n")
        pp.pprint(students_infos)
        print("weeks_involved\n")
        pp.pprint(weeks_involved)
    
    professor_slots = aggregate_slots(students_infos, weeks_involved)
    if DEBUG:
        print('professor_slots')
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(professor_slots)
        
    for student, slots in professor_slots.items():
        for slot in slots:
            # week_number = get_number_of_the_week(slot)
            week_number = str(get_number_of_the_week(slot))
            # Find the corresponding teacher and update their slots
            for teacher, info in teachers_graph_obj.items():
                if DEBUG:
                    print('student ', student, ' teacher ', teacher)
                if student != teacher:
                    continue
                if DEBUG:
                    print('c2  week_nb: ', week_number, ' in ', info['slots'])
                if week_number in info['slots']:
                    if slot in info['slots'][str(week_number)]:
                        if DEBUG:
                            print('teacher ', teacher)
                            print('info[slots][str(week_number)] BEFORE ', info['slots'][str(week_number)])
                        info['slots'][str(week_number)].remove(slot)
                        if DEBUG:
                            print('info[slots][str(week_number)] AFTER ', info['slots'][str(week_number)])
                        # Decrement the max_days for that week
                        if info['max_days'][str(week_number)] > 0:
                            info['max_days'][str(week_number)] -= 1
                        else:
                            quota_control.append(f"Quota problem for {week_number} for {teacher}")

    
    
    if DEBUG:
        print("PRINT OUTPUT OBJECT")
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(teachers_graph_obj)
    return quota_control


def check_for_quota(EXEMPLE_records_for_control, recueil_besoins_records, teachers_info_records, current_week_num, teachers_calendar):
    
    DEBUG = False

    try:
        students_next_week = extract_students_infos_and_slots(EXEMPLE_records_for_control, recueil_besoins_records, current_week_num)
        if DEBUG:
            pp = pprint.PrettyPrinter(indent=2)
            pp.pprint(students_next_week)
    except Exception as e:
        print(e)
        raise e
    else:
        print('Students sync successfully')

        
    try:
        weeks_involved = get_weeks_and_years_involved(students_next_week)
    except Exception as e:
        print(e)
        raise e
    
    
    try:
        teachers_email_list = get_teachers_email_list(teachers_info_records)
        if (DEBUG):
            print('teachers_email_list\n', teachers_email_list)
    except Exception as e:
        print(e)
        raise e 

    
    try:
        teachers_calendar_filtered = filter_teacher_availabilities_by_date(weeks_involved, teachers_calendar, teachers_email_list)
        if (DEBUG):
            print('teachers_calendar_filtered\n', teachers_calendar_filtered)
    except Exception as e:
        print(e)
        raise e 
    
    
    try:
        teachers_graph = extract_and_create_teachers_struct_for_graph(weeks_involved, teachers_info_records, teachers_calendar_filtered)
        if DEBUG:
            print('FIRST GRAPH')
            pp = pprint.PrettyPrinter(indent=2)
            pp.pprint(teachers_graph)
    except Exception as e:
        print(e)
        raise e
    
    try:
        quota_control = control_quota_teachers_availabilities_with_slot_taken(teachers_graph, EXEMPLE_records_for_control, weeks_involved)
        if DEBUG:
            print('Teacher graph after taking into account slot given to students')
            pp = pprint.PrettyPrinter(indent=2)
            pp.pprint(teachers_graph)    
    except Exception as e:
        raise e    
   
    
    return quota_control