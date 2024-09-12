def extract_enseignement_mode_with_email_as_key(recueil_besoins_records):
    DEBUG = False
    """This function extracts the teaching mode related to each teacher using their email as a key.
    Only the 'Mode' field is retained for each record."""
    student_dict = {}
    for record in recueil_besoins_records:
        if (DEBUG):
            print('record :', record)
        if 'Email' in record['fields']:
            email = record['fields'].get('Email', '').strip().lower()  # Strip whitespace and convert to lower case
            if (DEBUG):
                print('email key: ', email)
            # Extract only the 'Mode' field
            lieu = record['fields'].get('Lieu', None)  # Use .get() to avoid KeyError if 'lieu' does not exist
            if not lieu:
                lieu = 'Présentiel'
            student_dict[email] = {'Lieu': lieu}
    return student_dict