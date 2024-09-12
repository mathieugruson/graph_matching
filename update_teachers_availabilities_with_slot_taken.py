import pprint
import os
from airtable import Airtable
from utils.date import convert_and_round_time, get_number_of_the_week
from datetime import datetime, timedelta, date

def is_week_involved(date_str, weeks_involved):
    # Extract week number and year from the date
    date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
    year, week_num, day_of_week = date_obj.isocalendar()
    return (week_num, year) in weeks_involved

def aggregate_slots(students_infos, weeks_involved):
    """
    This function aggregates available time slots for professors based on student records.
    It processes a list of student information records, each containing scheduling details,
    and compiles a dictionary that maps each professor to their respective time slots during specified weeks.
    
    Parameters:
        students_infos (list of dicts): A list of dictionaries, each representing a student record.
            The record must contain a 'fields' dictionary with keys for the professor's name and up to four time slots.
        weeks_involved (list): A list of weeks during which the time slots are to be considered relevant.

    Returns:
        dict: A dictionary where keys are professor names and values are lists of time slots
              that fall within the specified weeks.

    The function filters out records without a specified professor, converts raw time data into
    a standardized format, and checks the relevance of each time slot against the provided weeks.
    It utilizes helper functions `convert_and_round_time` and `is_week_involved` to process time slots.
    Debugging output can be enabled by setting the DEBUG variable to True.
    """
    DEBUG = False
    professor_slots = {}

    for record in students_infos:
        if DEBUG:
            print('record : ', record)
        professor = record['fields'].get('Formateur Robot', None)  # Default to None if key is missing
        if (DEBUG):
            print('professeur ', professor)        
        if professor is None:
            continue
        
        if professor not in professor_slots:
            professor_slots[professor] = []
        
        # Extract time slots using the fields dictionary
        creneaux = {
            'Creneaux 1': convert_and_round_time(record['fields'].get('Premiere partie')),
            'Creneaux 2': convert_and_round_time(record['fields'].get('Deuxieme partie')),
            'Creneaux 3': convert_and_round_time(record['fields'].get('Troisieme partie')),
            'Creneaux 4': convert_and_round_time(record['fields'].get('Quatrieme partie'))
        }

        # Add valid slots to the professor's list
        for creneau_value in creneaux.values():
            if creneau_value and is_week_involved(creneau_value, weeks_involved):
                professor_slots[professor].append(creneau_value)
                
    return professor_slots

def update_teachers_availabilities_with_slot_taken(teachers_graph_obj, students_infos, weeks_involved):
    """
    Dans cette fonction, on va reprendre le graph et le mettre à jour, mais cette fois-ci avec les slots qui ont déja éte attribués aux formateurs
    pour éviter les doubles ou les dépassements de quota. 
    
    Nous utilisons les informations de tous les élèves, y compris ceux qui ne sont pas concernés par l'attribution d'un formateur,
    afin d'avoir une vue complète des créneaux déjà réservés pendant nos semaines de formation concernées dans weeks_involved.
    """
    DEBUG = False

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
    
    
    if DEBUG:
        print("PRINT OUTPUT OBJECT")
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(teachers_graph_obj)
    return teachers_graph_obj


