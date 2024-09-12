def check_key_presence(required_keys, records):
    if not records:
        return False
    
    unique_keys = set()
    
    # Iterate over each element in the list
    for element in records:
        # Add keys from the 'fields' dictionary to the set
        unique_keys.update(element['fields'].keys())

    # Convert the set to a list if you need it in list form
    keys_list = list(unique_keys)
    
    # Check if all required keys are in the keys_list
    missing_keys = [key for key in required_keys if key not in keys_list]

    # Print missing keys or a success message
    if missing_keys:
        return False
    else:
        return True

def check_teacher_form_table_name(teachers_form_records):
    required_keys = [
        'Numero de la semaine', 'année', 'Session', 'Formateur', 
        'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'
    ]
    return check_key_presence(required_keys, teachers_form_records)


def check_recueil_besoins_table_name(recueil_besoins_records):
    required_keys = [
            'Email', 'Lieu']
    return check_key_presence(required_keys, recueil_besoins_records)


def check_teachers_info_table_name(teachers_info_records):
    required_keys = [
            'Session par semaine', 'Nom', 'Compétences', 'Statut', 'Mode']
    return check_key_presence(required_keys, teachers_info_records)


def check_teachers_calendar_table_name(teachers_calendar_records):
    required_keys = [
            'Start', 'End', 'Creator'
        ]
    return check_key_presence(required_keys, teachers_calendar_records)
    

def check_EXEMPLE_table_name(EXEMPLE_records):
    required_keys = [
            'Mail', 'Formation', 'Formateur', 
            'Premiere partie', 'Deuxieme partie', 'Troisieme partie', 'Quatrieme partie'
        ]
    
    return check_key_presence(required_keys, EXEMPLE_records)
    

