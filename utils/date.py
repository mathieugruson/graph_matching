from datetime import datetime, timedelta, date
from .email import send_email
from .protect import get_env_variable


def date_from_week(week_num, day_of_week, year):
    # ISO calendar: the first day of the first week of the year
    d = date(year, 1, 1)
    # If the year starts later than Monday, adjust the starting date
    if d.weekday() > 3:
        d = d + timedelta(7 - d.weekday())
    else:
        d = d - timedelta(d.weekday())
    # Calculate the date for the given week and day
    return d + timedelta(days=(week_num - 1) * 7 + day_of_week)


def convert_and_round_time(iso_date_str, hour_adjustment=2):
    if iso_date_str is None:
        return None  # or return a default value or an appropriate response
    
    # Parse the ISO formatted date string into a datetime object
    try:
        date_obj = datetime.fromisoformat(iso_date_str.replace("Z", "+00:00"))
    except Exception as e:  
        EXEMPLE_EMAIL_RESP_EDT = get_env_variable('EXEMPLE_EMAIL_RESP_EDT')      
        print(f"Error parsing date string: {iso_date_str}. Error: {e}")
        send_email("EXEMPLE EXEMPLE - Assignation élèves aux formateurs - Erreur",f"Erreur convert_and_round_time.py", EXEMPLE_EMAIL_RESP_EDT)
        return None

    # Retrieve the hour from the datetime object
    hour = date_obj.hour
    
    # Adjust the datetime object based on the hour range
    if 5 <= hour < 10:
        adjusted_date_obj = date_obj.replace(hour=9, minute=0, second=0, microsecond=0)
    elif 10 <= hour < 13:
        adjusted_date_obj = date_obj.replace(hour=14, minute=0, second=0, microsecond=0)
    elif hour >= 13:
        adjusted_date_obj = date_obj.replace(hour=18, minute=0, second=0, microsecond=0)
    else:
        # If the time does not match any of the conditions, leave as is or apply a different rule
        adjusted_date_obj = date_obj + timedelta(hours=hour_adjustment)

    # Format the datetime object to the desired format: YYYY-MM-DD HH:MM
    formatted_date_str = adjusted_date_obj.strftime('%Y-%m-%d %H:%M')
    return formatted_date_str


def convert_time(iso_date_str, hour_adjustment=2):
    if iso_date_str is None:
        return None  # or return a default value or an appropriate response
    
    # Parse the ISO formatted date string into a datetime object
    try:
        date_obj = datetime.fromisoformat(iso_date_str.replace("Z", "+00:00"))
    except Exception as e:  
        EXEMPLE_EMAIL_RESP_EDT = get_env_variable('EXEMPLE_EMAIL_RESP_EDT')      
        print(f"Error parsing date string: {iso_date_str}. Error: {e}")
        send_email("EXEMPLE EXEMPLE - Assignation élèves aux formateurs - Erreur",f"Erreur convert_and_round_time.py", EXEMPLE_EMAIL_RESP_EDT)
        return None

    # Retrieve the hour from the datetime object
    hour = date_obj.hour
    
    # If the time does not match any of the conditions, leave as is or apply a different rule
    adjusted_date_obj = date_obj + timedelta(hours=hour_adjustment)

    # Format the datetime object to the desired format: YYYY-MM-DD HH:MM
    formatted_date_str = adjusted_date_obj.strftime('%Y-%m-%d %H:%M')
    return formatted_date_str


def get_number_of_the_week_and_year(date_str):
    
    date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M")

    year, week_num, day_of_week = date_obj.isocalendar()

    return (week_num, year)

def get_number_of_the_week(date_str):
    
    date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M")

    year, week_num, day_of_week = date_obj.isocalendar()

    return week_num

def get_year(date_str):
    
    date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M")

    year, week_num, day_of_week = date_obj.isocalendar()

    return year

def current_week_number():
    # Get the current date
    today = datetime.now()
    # Return the ISO week number (week starts on Monday)
    return today.isocalendar().week


def parse_datetime(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d %H:%M")

def premiere_partie_date_is_not_in_weeks(premiere_partie_date, week_num=None, weeks_in_advance=3,):
    DEBUG = False
    current_week = week_num if week_num is not None else current_week_number()
    
    if premiere_partie_date:
        premiere_partie_week = get_number_of_the_week(premiere_partie_date)
        if current_week <= premiere_partie_week <= current_week + weeks_in_advance:
            if DEBUG:
                print(f"Date is within the next {weeks_in_advance} week(s).")
            return False
        else:
            if DEBUG:
                print(f"Date is not within the next {weeks_in_advance} week(s).")
            return True
    return True
