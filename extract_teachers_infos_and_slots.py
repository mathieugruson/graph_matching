
from airtable import Airtable
from datetime import datetime, timedelta
import datetime
from utils.date import parse_datetime
from utils.print import print_airtable_records, print_students, print_teachers
from utils.teachers import reformat_teachers_info
import pprint
import difflib
from utils.email import send_email
from utils.protect import get_env_variable


def date_from_week(week_num, day_of_week, year):
    # ISO calendar: the first day of the first week of the year
    d = datetime.date(year, 1, 1)
    # If the year starts later than Monday, adjust the starting date
    if d.weekday() > 3:
        d = d + datetime.timedelta(7 - d.weekday())
    else:
        d = d - datetime.timedelta(d.weekday())
    # Calculate the date for the given week and day
    return d + datetime.timedelta(days=(week_num - 1) * 7 + day_of_week)

day_to_index = {
    "Lundi": 0,
    "Mardi": 1,
    "Mercredi": 2,
    "Jeudi": 3,
    "Vendredi": 4,
    "Samedi": 5,
    "Dimanche": 6
}

# Timeslot mappings
timeslots = {
    "Matin": "09:00",
    "Aprem": "14:00",
    "Soir (18h-20h)": "18:00"
}


def is_available(date_time_str, teachers_calendar, duration_hours=4):
    """Checks if a datetime string is available for a duration of hours according to the teacher's calendar."""
    session_start = parse_datetime(date_time_str)
    session_end = session_start + timedelta(hours=duration_hours)
    
    # on check si le slot testé n'overlap pas avec un une indisponibilité du formateur.
    # Si une indispo overlap, alors on retourne faux pour ne pas ajouter le slot comme etant disponible
    # Si aucune indispo overlap, cela veut dire que c'est libre donc on peut retourner True pour ajouter le slot comme libre. 
    
    for entry in teachers_calendar:
        entry_start = parse_datetime(entry['Start'])
        entry_end = parse_datetime(entry['End'])
        
        # Check if the session overlaps with the calendar entry
        # print('entry before check', entry)
        if session_start < entry_end and session_end > entry_start:
            # print('entry false', entry)
            return False  # The time slot overlaps with an unavailable period
        
    return True 


def extract_and_create_teachers_struct_for_graph(weeks_involved, teachers_info_records, teachers_calendar):
    """ Dans cette fonction on va extraire les sessions disponibles pour chaque formateur sur les semaines ou nos
    éleves extraient ont des créneaux. Comme les disponibilités sont données en string matin, aprem, soir, il faut convertir
    ces disponibilités en heures pour qu'il puisse y avoir match avec les élèves.
    
    On récupère également toutes les informations utiles comme le nombre de sessions disponibles ou les compétences ou le mode d'enseignement
    
    Voici un exemple de la structure de sortie : 
    {   'domitille@example.fr': { 'max_days': {'18': 12, '19': 12},
                                  'mode': ['distanciel'],
                                  'skills': ['Sketchup'],
                                  'slots': { '18': ['2024-05-03 09:00'],
                                             '19': ['2024-05-10 09:00']},
                                  'type': 'freelance'},
        'macron@example.fr': { 'max_days': {'18': 12, '19': 12},
                               'mode': ['présentiel'],
                               'skills': ['Sketchup'],
                               'slots': { '18': [ '2024-05-05 09:00',
                                                  '2024-05-05 14:00',
                                                  '2024-05-04 09:00',
                                                  '2024-05-04 14:00'],
                                          '19': [ '2024-05-12 09:00',
                                                  '2024-05-12 14:00',
                                                  '2024-05-11 09:00',
                                                  '2024-05-11 14:00']},
                               'type': 'freelance'},
    }
    """
    DEBUG = False

    teachers_infos = reformat_teachers_info(teachers_info_records)
    EXEMPLE_EMAIL_RESP_EDT = get_env_variable('EXEMPLE_EMAIL_RESP_EDT')

    teachers = {}
    # import pprint
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(teachers_calendar)
    
    for email, info in teachers_infos.items():
            teacher_name = email  # Or extract name differently if email is not the desired identifier

            teacher_filtered_calendar = [entry for entry in teachers_calendar if entry.get('Creator') == teacher_name]
            if not teacher_filtered_calendar:
                if (DEBUG):
                    print('teacher name calendar', teacher_name)
                continue
            
            if teacher_name not in teachers:
                
                type = info.get('Statut', '').lower()
                if not type:
                    type = 'freelance'
                mode =  info.get('Mode', [])
                if not mode:
                    mode = 'distanciel'
                max_days = info.get('Session par semaine')
                if not max_days:
                    max_days = 0
                skills = info.get('Compétences', [])
                if not skills:
                    send_email("EXEMPLE EXEMPLE - Assignation élèves aux formateurs - Erreur",f"Attention {teacher_name} semble ne pas avoir de compétence définie", EXEMPLE_EMAIL_RESP_EDT)


                teachers[teacher_name] = {
                    'slots': {},
                    'max_days': {},
                    'type': type,
                    'mode': mode,
                    'skills': skills
                }
            
            # la logique est que si il est disponible, alors la string se trouve dans timeslot et donc on lui rajoute une disponibilité
            for week_num, year in weeks_involved:
                week_str = str(week_num)
                free_slots = []
                teachers[teacher_name]['slots'][week_str] = []
                teachers[teacher_name]['max_days'][week_str] = info.get('Session par semaine', 0)
                
                # EXEMPLE boucle for pour prendre en compte le changement de logique
                for day in day_to_index:
                    date = date_from_week(week_num, day_to_index[day], year)
                    for slot in timeslots:
                        if is_available(f"{date} {timeslots[slot]}", teacher_filtered_calendar):
                            free_slots.append(f"{date} {timeslots[slot]}")

                teachers[teacher_name]['slots'][week_str].extend(free_slots)

        # Debug: print full structure
    if DEBUG:
        import pprint
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(teachers)



    return teachers


