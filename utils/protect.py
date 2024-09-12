import os
from airtable import Airtable
from dotenv import load_dotenv
load_dotenv()

def get_env_variable(var_name):
    """ Retrieve environment variable or raise an exception if not found. """
    
    value = os.getenv(var_name)
    # print('varname ', var_name, '\nvalue ', value)
    if value is None:
        raise ValueError(f"Environment variable {var_name} is not set")
    return value

def safe_init_airtable(base_id, table_name, api_key):
    """ Safely initialize an Airtable instance. """
    try:
        return Airtable(base_id, table_name, api_key)
    except Exception as e:
        raise ValueError(f"Failed to initialize Airtable instance for table {table_name} due to {str(e)}")

def safe_get_all(airtable_instance):
    """ Safely fetch all records from an Airtable instance. """
    try:
        return airtable_instance.get_all()
    except Exception as e:
        raise ValueError(f"Failed to fetch records due to {str(e)}")


def validate_records(records):
    """ Validate that records contain necessary fields. """
    for record in records:
        if 'fields' not in record or 'Mail' not in record['fields']:
            raise ValueError("Record is missing required fields")
        if not isinstance(record['fields']['Mail'], str):
            raise TypeError("Mail field must be a string")