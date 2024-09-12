from datetime import datetime
from utils.date import convert_time, get_number_of_the_week_and_year


def clean_teachers_calendars(teachers_calendar_records, teachers_calendar_airtable):
    DEBUG = False
    today = datetime.now()
    
    clean_records = []

    # Loop through records to find matches and update or delete accordingly
    for record in teachers_calendar_records:
        # Handle deletion of records where the 'Creator' field matches the specific email
        if 'Creator' in record['fields'] and record['fields']['Creator'] == 'contact@example.fr':
            # # Delete the record if the creator email matches
            # teachers_calendar_airtable.delete(record['id'])
            # print('record contact', record)
            if DEBUG:
                print('Deleted record with ID:', record['id'])
            continue
        
        
                # Handle deletion if the 'End' date is in the past
        if 'End' in record['fields']:
            end_date = convert_time(record['fields']['End'])        
            end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M')
            
            if end_date < today:
                # print('record date', record)
                # teachers_calendar_airtable.delete(record['id'])
                # if DEBUG:
                #     print('Deleted record with ID:', record['id'], 'due to past end date')
                continue
        
        clean_records.append(record)

        

    return clean_records