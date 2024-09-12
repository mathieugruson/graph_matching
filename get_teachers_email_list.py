def get_teachers_email_list(teachers_info_records):

    """The goal of this function is to convert the teacher infos records from airtable to make the
    name of the formateur, which is unique, a key to easily retrieve useful other informations"""
    teachers_array = []

    for record in teachers_info_records:
        if 'Nom' in record['fields'] and record['fields']['Nom']:
            teachers_array.append(record['fields']['Nom'])
            
    return teachers_array
    