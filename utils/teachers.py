def reformat_teachers_info(teachers_info_records):
    """The goal of this function is to convert the teacher infos records from airtable to make the
    name of the formateur, which is unique, a key to easily retrieve useful other informations"""
    teachers_dict = {}

    for record in teachers_info_records:
        if 'Nom' in record['fields'] and record['fields']['Nom']:
            name = record['fields']['Nom']
            # Exclude the 'Nom' field from the value dictionary
            fields = {key: value for key, value in record['fields'].items() if key != 'Nom'}
            teachers_dict[name] = fields
            
    return teachers_dict