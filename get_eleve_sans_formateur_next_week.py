from utils.date import convert_and_round_time, premiere_partie_date_is_not_in_weeks

def get_eleve_sans_formateur_next_week(EXEMPLE_after_match, current_week_num):
    
    student_without_teacher = []
    for record in EXEMPLE_after_match:
    # Check if 'Mail' field exists and is not empty
        try:
            if 'Mail' in record['fields'] and record['fields']['Mail']:
                # Extraire que les éleves dont la formation commence cette semaine ou celle d'après
                premiere_partie_date = convert_and_round_time(record['fields'].get('Premiere partie'))
                if not premiere_partie_date:
                    continue 
                if (premiere_partie_date_is_not_in_weeks(premiere_partie_date, current_week_num)):
                    continue
                
                if 'Formateur Robot' in record['fields'] and record['fields']['Formateur Robot']:
                    continue  # Skip if student already has a Formateur assigned
                else:
                    student_without_teacher.append(record['fields']['Mail'])
        except Exception as e:
            print ('extract_students_infos_and_slots', e)
            raise Exception("Extract_students_infos_and_slots failed: " + str(e))
        
    return student_without_teacher