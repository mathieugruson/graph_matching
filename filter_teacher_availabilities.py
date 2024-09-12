from utils.date import convert_time, get_number_of_the_week_and_year

def get_teacher_mail(record, teachers_email_list):
    DEBUG = False
    if DEBUG:
        print('record', record)
        print('teachers_email_list', teachers_email_list)
    # Check if the 'Creator' is 'contact@example'
    if record['fields']['Creator'] == 'contact@example.fr':
        # Loop through each email in 'Attendees'
        attendees = record['fields']['Attendees']
    
        # If attendees is a single string, split it into a list
        if isinstance(attendees, str):
            attendees = attendees.split(", ")  # Adjust the delimiter as needed

        for email in attendees:
            # Check if the email is in the teachers_email_list
            # print('email of attendees', email)
            if email in teachers_email_list:
                # print('teacher in attendees ', email)
                return email
        # Return None if no teacher email is found in 'Attendees'
        return None
    else:
        # Return the 'Creator' email if the creator is not 'contact@example'
        return record['fields']['Creator']


def filter_teacher_availabilities_by_date(weeks_involved, teachers_calendar_records, teachers_email_list):
    '''Cette fonction a pour objet : 
    - de ne garder que les horaires qui recoupes les semaines impliquees pour
    eviter d'avoir toutes les lignes du tableau et rendre plus efficace l'algorithme.
    - convertir le format des dates
    - extraire l'enseignant dans la liste des attendee'''
    
    DEBUG = False
    filtered_records = []

    for record in teachers_calendar_records:  # Slicing the list to get the first 10 records
        
        start =  record['fields']['Start']
        end = record['fields']['End']
        if DEBUG:
            print('start', start)
            print('end', record['fields']['End'])

        start_converted = convert_time(start)        
        start_week_nb_year = get_number_of_the_week_and_year(start_converted)

        end_converted = convert_time(end)        
        end_week_nb_year = get_number_of_the_week_and_year(end_converted)
        

        if start_week_nb_year in weeks_involved:
            teacher = get_teacher_mail(record, teachers_email_list)
            
            # Proceed only if a teacher email is found; otherwise, continue to the next iteration
            if teacher is not None:
                filtered_records.append({
                    'Creator': teacher,
                    'Start': start_converted,
                    'End': end_converted
                })
            continue
        
        if end_week_nb_year in weeks_involved:
            teacher = get_teacher_mail(record, teachers_email_list)
            
            # Proceed only if a teacher email is found; otherwise, continue to the next iteration
            if teacher is not None:
                filtered_records.append({
                    'Creator': teacher,
                    'Start': start_converted,
                    'End': end_converted
                })
            continue
        
        if DEBUG:
            print('start_week_nb', start_week_nb_year)
            print('end_week_nb', end_week_nb_year)
        
        # permet de mettre si la date d'indisponibilité encadre une semaine ex : si indispo de semaine 1 a 3 et que la
        # semaine impliqué est la 2, alors il faut la rajouter car au dessus n'aura pas detecter
        for week in weeks_involved:
            if ((start_week_nb_year[0] < week[0] and start_week_nb_year[1] <= week[1]) and (end_week_nb_year[0] > week[0] and end_week_nb_year[1] >= week[1])):
                teacher = get_teacher_mail(record, teachers_email_list)
                
                # Proceed only if a teacher email is found; otherwise, continue to the next iteration
                if teacher is  None:
                    continue
                filtered_records.append({
                    'Creator': teacher,
                    'Start': start_converted,
                    'End': end_converted
                })
                continue

    
    if DEBUG:
        print('weeks_involved', weeks_involved)
        import pprint
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(filtered_records)
    
    return filtered_records
