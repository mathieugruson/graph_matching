from datetime import datetime
from extract_students_infos_and_slots import extract_students_infos_and_slots
from quota_control import check_for_quota
from airtable import Airtable
import pprint

def parse_datetime(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.000Z')
    except ValueError:
        return None

def check_for_duplicate_sessions(data):
    trainer_sessions = {}
    trainer_with_duplicate = []

    for entry in data:
        if 'Mail' in entry['fields'] and entry['fields']['Mail']:
            if 'Formateur Robot' in entry['fields'] and entry['fields']['Formateur Robot']:
                formateur = entry['fields']['Formateur Robot']

                # Extract and parse session start times
                sessions = [
                    parse_datetime(entry['fields'].get('Premiere partie', '')),
                    parse_datetime(entry['fields'].get('Deuxieme partie', '')),
                    parse_datetime(entry['fields'].get('Troisieme partie', '')),
                    parse_datetime(entry['fields'].get('Quatrieme partie', ''))
                ]

                # Filter out None values
                sessions = [session for session in sessions if session]

                if formateur not in trainer_sessions:
                    trainer_sessions[formateur] = sessions
                else:
                    # Append new sessions to existing list and avoid duplicates
                    for session_start in sessions:
                        if session_start not in trainer_sessions[formateur]:
                            trainer_sessions[formateur].append(session_start)
                        else:
                            print(f"Duplicate session time detected for {formateur} at {session_start}")
                            trainer_with_duplicate.append(f"Duplicate session for {formateur}: {session_start}")
                    
    return trainer_with_duplicate
                    
def check_for_skills_match(EXEMPLE, teachers_info):
    results = []
    for apprenant in EXEMPLE:
        if 'Mail' in apprenant['fields'] and apprenant['fields']['Mail'] and 'Formateur Robot' in apprenant['fields'] and apprenant['fields']['Formateur Robot']:
            formateur_email = apprenant['fields'].get('Formateur Robot', '')
            skill_apprenant = apprenant['fields'].get('Formation', '')
            for formateur in teachers_info:
                if formateur['fields'].get('Nom') == formateur_email:
                    # Check if the formateur has the required skill
                    if skill_apprenant not in formateur['fields'].get('Compétences', []):
                        results.append({
                            'Apprenant': apprenant['fields'].get('Mail'),
                            'Formateur': formateur_email,
                            'Required Skill': skill_apprenant,
                            'Issue': 'Formateur lacks required skill'
                        })
    return results

def check_for_availabilities_and_mode(EXEMPLE_after_match, recueil_besoins_records, current_week_num, teachers_graph_before_assignement):
    
    students_next_week = extract_students_infos_and_slots(EXEMPLE_after_match, recueil_besoins_records, current_week_num)
    # Extract the teacher's email from the student's preferences.
    results = {}
    # Iterate over each student in the list
    for student in students_next_week:
        teacher_email = student.get('Professeurs', None)
        if not teacher_email:  # This will be true for both None and empty strings
            continue
        
        # Retrieve the teacher's information from the teacher graph.
        teacher_info = teachers_graph_before_assignement.get(teacher_email)
        if not teacher_info:
            results[student['Nom']] = "Teacher not found in the teacher graph."
            continue
        
        # Check if the teaching modes are compatible.
        if student['Mode'] not in teacher_info['mode']:
            results[student['Nom']] = "Teaching mode mismatch."
            continue
        
        # Collect all slots from the student that are not None.
        student_slots = [time for time in [student[f'Creneaux {i}'] for i in range(1, 5)] if time is not None]
        
        # Collect all available slots for the teacher.
        teacher_available_slots = []
        for day_slots in teacher_info['slots'].values():
            # Loop over each slot in the day's slots
            for slot in day_slots:
                # Add the slot to the list of available teacher slots
                teacher_available_slots.append(slot)
        
        # Check if all student slots are available in the teacher's slots.
        # Initialize an empty list to hold slots that are not available with the teacher
        unavailable_slots = []

        # Loop through each slot requested by the student
        for slot in student_slots:
            # Check if the slot is not in the teacher's available slots
            if slot not in teacher_available_slots:
                # If the slot is unavailable, add it to the list of unavailable slots
                unavailable_slots.append(slot)

        # Check if there are any unavailable slots
        if unavailable_slots:
            # If there are unavailable slots, update the results dictionary with the student's name and the unavailable slots
            results[student['Nom']] = f"These slots are unavailable: {unavailable_slots}"

            
    return results


def matching_control(EXEMPLE_after_match, recueil_besoins_records, teachers_info_records, current_week_num, teachers_graph_availabilies_before_assignment, teachers_calendar):
    
    formateurs = check_for_duplicate_sessions(EXEMPLE_after_match)
    if (len(formateurs) > 0 ):
        print(f"formateurs:\n{formateurs}")
    else:
        print(f"No overlapping sessions.")

    skills_match = check_for_skills_match(EXEMPLE_after_match, teachers_info_records)
    if (len(skills_match) > 0 ):
        print(f"skills_match:\n{skills_match}")
    else:
        print(f"No skills_match issues.")
    
    
    slot_match_control = check_for_availabilities_and_mode(EXEMPLE_after_match, recueil_besoins_records, current_week_num, teachers_graph_availabilies_before_assignment)
    if len(slot_match_control) > 0:
        print(f"slot_match_control:\n{slot_match_control}")
    else:
        print(f"No slot_match and mode issues.")
        
    quota_control = check_for_quota(EXEMPLE_after_match, recueil_besoins_records, teachers_info_records, current_week_num, teachers_calendar)
    if len(quota_control) > 0:
        print(f"quota_control :\n{quota_control}")
    else:
        print(f"No quota_control issues")
        
    
    
    
    return 