def print_airtable_records(airtable):
    """Fetches and prints records from an Airtable table."""
    if airtable is None:
        return 
    records = airtable.get_all()  # Fetch all records from the table
    for record in records:
        print(record)  # Print each record

def print_teachers(teachers_records):
    if teachers_records is None:
        return 
    # Iterate through each record and print its fields
    for teacher in teachers_records:
        for field, value in teacher['fields'].items():
            print(f"{field}: {value}")
        print("\n")  # Add a newline for readability between records


def print_students(students_records):
    if students_records is None:
        return 
    # Iterate through each record and print its fields
    for student in students_records:
        for field, value in student['fields'].items():
            print(f"{field}: {value}")
        print("\n")  # Add a newline for readability between records
