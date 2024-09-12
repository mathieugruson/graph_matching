from airtable import Airtable
from datetime import datetime, timedelta
from utils.date import convert_and_round_time, get_number_of_the_week, current_week_number, premiere_partie_date_is_not_in_weeks
from utils.mail import sanitize_mail
from utils.extract_enseignement_mode_with_email_as_key import extract_enseignement_mode_with_email_as_key
from utils.email import send_email
from utils.protect import get_env_variable


                        
def extract_students_infos_and_slots(EXEMPLE_records, recueil_besoins_records, current_week_num):
    """On utilise la base gestion des apprenants et recueil des besoins ainsi que la semaine actuelle pour extraire
    les informations pertinentes des étudiants afin de créer une data structure avec ces informations.
    
    La base receuil des besoins ne sert qu'à extraire le mode d'enseignement (à distance ou en présentiel).
    
    On va récuper tous les étudiants dont la premiere session démarre dans la semaine actuelle ou les prochaines semaines
    (même s'ils ont déja un prof car cela nous permet de savoir si le prof est pris ou pas dej́a à cette date)

    """
    DEBUG = False
    DEBUG1 = False

    EXEMPLE_EMAIL_RESP_EDT = get_env_variable('EXEMPLE_EMAIL_RESP_EDT')

    students_next_weeks = []

    #ici on reformule le receuille des besoins pour pouvoir extraire l'information qui nous intéresse grace a la clé qui sera l'email
    student_teach_mode_records = extract_enseignement_mode_with_email_as_key(recueil_besoins_records)
    if (DEBUG):
        print(student_teach_mode_records)

    # Loop through each record in the retrieved data
    for record in EXEMPLE_records:
        # Check if 'Mail' field exists and is not empty
        try:
            if 'Mail' in record['fields'] and record['fields']['Mail']:
                if 'Formateur Robot' in record['fields'] and record['fields']['Formateur Robot']:
                    continue  # Skip if student already has a Formateur assigned

                # Extraire que les éleves dont la formation commence cette semaine ou celle d'après
                premiere_partie_date = convert_and_round_time(record['fields'].get('Premiere partie'))
                if not premiere_partie_date:
                    continue 
                if (premiere_partie_date_is_not_in_weeks(premiere_partie_date, current_week_num)):
                    continue
                
                # Creer l'object pour avec les informations nécessaires
                mail = record['fields'].get('Mail').strip().lower()
                sanitized_mail = sanitize_mail(mail)
                if not sanitized_mail:
                    continue

                
                # On récupère le mode, s'il n'est pas indiqué on met présentiel pour éviter tout problème
                mode_value = student_teach_mode_records.get(sanitized_mail, {}).get('Lieu', 'Présentiel')

                # If mode_value is None (either because 'Lieu' is set to None or the key is absent), use 'Présentiel'
                if mode_value is None:
                    mode_value = 'Présentiel'

                # Now apply strip() and lower() to clean and normalize the mode value
                mode = mode_value.strip().lower()
                # Check if the formation data exists and is not empty before proceeding
                formation_raw = record['fields'].get('Formation')
                if not formation_raw:
                    if DEBUG:
                        print('Formation is empty : ', formation_raw)
                    continue  # Skip this student if formation data is missing
                
                if (DEBUG1):
                    print('student mail ', record['fields'].get('Mail'))
                    print('after strip and lower: ', record['fields'].get('Mail').strip().lower())
                    print('after sanitize ', sanitize_mail(mail))
                    print('formateur : ', record['fields'].get('Formateur Robot'))
                student_info = {
                    'Nom': sanitize_mail(mail),
                    'Formation': formation_raw,
                    'Professeurs': record['fields'].get('Formateur Robot', None),
                    'Creneaux 1': convert_and_round_time(record['fields'].get('Premiere partie', None)),
                    'Creneaux 2': convert_and_round_time(record['fields'].get('Deuxieme partie', None)),
                    'Creneaux 3': convert_and_round_time(record['fields'].get('Troisieme partie', None)),
                    'Creneaux 4': convert_and_round_time(record['fields'].get('Quatrieme partie', None)),
                    'Mode' : mode
                }
                
                students_next_weeks.append(student_info)
        except Exception as e:
            print ('extract_students_infos_and_slots', e)
            raise Exception("Extract_students_infos_and_slots failed: " + str(e))

    return students_next_weeks

