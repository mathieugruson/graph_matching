from datetime import datetime, timedelta
import re
from utils.extract_enseignement_mode_with_email_as_key import extract_enseignement_mode_with_email_as_key

def sanitize_mail(email_field):
    # Use regular expression to split on common separators (slash, comma, semicolon, whitespace)
    emails = re.split(r'[;/,\s]\s*', email_field)
    # Filter out empty strings in case of multiple separators and strip spaces, then convert to lower case
    cleaned_emails = [email.strip().lower() for email in emails if email.strip()]
    # Return the first email if there are any, otherwise return an empty string
    return cleaned_emails[0] if cleaned_emails else ''


def format_word(word):
    if word:  # Check if the word is not empty
        return word[0] + word[1:].lower()
    return word 

def extract_formation_name(input_string):
    # Regular expression to find "Fusion" or "SketchUp"
    match = re.search(r"\b(Fusion|SketchUp)\b", input_string)
    if match:
        # Return the matched string in lowercase
        
        return format_word(match.group(1))
    else:
        # Return None if no match is found
        return None
    

def get_number_of_the_week(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
    year, week_num, day_of_week = date_obj.isocalendar()
    return week_num

def create_students_struct_for_graph(eleves_dispos_records):
    """ On va créer aussi une data structure qui permet de savoir quel semaine sont les créneaux des étudiants en plus des autres informations.
    Cela va nous permettre ensuite de passer ce graph à notre algorithm de match.add()
    
    En voici un exemple : 
    {   'eleve10@gmail.com': { 'courses': ['2024-05-02 09:00', '2024-05-09 09:00'],
                         'mode': 'distanciel',
                         'skills': ['Sketchup'],
                         'weeks': { '2024-05-02 09:00': 18,
                                    '2024-05-09 09:00': 19}},
        'eleve11@gmail.com': { 'courses': ['2024-05-02 14:00', '2024-05-09 14:00'],
                         'mode': 'distanciel',
                         'skills': ['Sketchup'],
                         'weeks': { '2024-05-02 14:00': 18,
                                    '2024-05-09 14:00': 19}}
    }
    """
    DEBUG = False

    # Dictionary to hold the transformed student data
    student_schedule = {}
    
    if DEBUG:
        print('len ', len(eleves_dispos_records))

    for record in eleves_dispos_records:
        try:
            if 'Nom' in record and record['Nom']:
                student_name = sanitize_mail(record.get('Nom').strip().lower())
                if DEBUG:
                    print('student_name ', student_name)
                # Prepare lists to accumulate course slots and week frequencies
                courses = []
                # Change defaultdict(list) to a regular dictionary
                weeks = {}  # Using a simple dictionary instead of defaultdict(list)

                for i in range(1, 5):
                    time_slot_key = f'Creneaux {i}'
                    if DEBUG:
                        print("f'Creneaux {i}'", f'Creneaux {i}')
                        print('time_slot_key ', time_slot_key)
                    if time_slot_key in record:
                        time_slot = record.get(time_slot_key)
                        if DEBUG:
                            print("record.get(time_slot_key) ", record.get(time_slot_key))
                            print('time_slot ', time_slot)                        
                        if time_slot:
                            week_num = get_number_of_the_week(time_slot)
                            courses.append(time_slot)
                            weeks[time_slot] = week_num  # Store just the week number

                # Extract mode and skills
                mode = record.get('Mode', '').strip().lower()
                skills_raw = record.get('Formation', '')
                skills = [skill.strip() for skill in skills_raw.split(',') if skill.strip()]  # Assuming skills are comma-separated
                if DEBUG:
                    print('courses ', courses)
                # If courses were found, store them under the student's name
                if courses:
                    student_schedule[student_name] = {
                        'courses': courses,
                        'weeks': weeks,  # Directly assign the dictionary
                        'mode': mode,
                        'skills': skills
                    }


        except Exception as e:
            print(e)
            # Handle exception or log error
    # Debug: print full structure
    if DEBUG:
        import pprint
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(student_schedule)

    return student_schedule
