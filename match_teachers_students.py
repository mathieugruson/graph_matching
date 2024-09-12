from create_students_struct_for_graph import create_students_struct_for_graph
from extract_teachers_infos_and_slots import extract_and_create_teachers_struct_for_graph
from extract_students_infos_and_slots import extract_students_infos_and_slots
from update_teachers_availabilities_with_slot_taken import update_teachers_availabilities_with_slot_taken
from get_weeks_and_years_involved import get_weeks_and_years_involved
from matching_control import matching_control
from utils.mail import sanitize_mail
from utils.date import current_week_number
from utils.protect import get_env_variable, safe_init_airtable, safe_get_all
from graph import graph_solve
from airtable import Airtable
import pprint
from utils.email import send_email
from check_table_name import check_EXEMPLE_table_name, check_teacher_form_table_name, check_recueil_besoins_table_name, check_teachers_info_table_name, check_teachers_calendar_table_name
from get_eleve_sans_formateur_next_week import get_eleve_sans_formateur_next_week
from filter_teacher_availabilities import filter_teacher_availabilities_by_date
from clean_teachers_calendars import clean_teachers_calendars
from get_teachers_email_list import get_teachers_email_list

EXEMPLE_EMAIL_RESP_EDT = get_env_variable('EXEMPLE_EMAIL_RESP_EDT')
EXEMPLE_EMAIL_RESP_DEV = get_env_variable('EXEMPLE_EMAIL_RESP_DEV')
EXEMPLE_EMAIL_CONTACT = get_env_variable('EXEMPLE_EMAIL_CONTACT')

def update_airtable_with_results(results, EXEMPLE_records, EXEMPLE_airtable):
    
    DEBUG = False
    for record in EXEMPLE_records:
            if 'Mail' in record['fields'] and record['fields']['Mail']:                        
                email_raw = record['fields']['Mail']  # Using 'Mail' as key to match by email.
                email = sanitize_mail(email_raw)
                if (DEBUG):
                    print('record ', record)
                    print('email ', email)
                if email in results:
                    teacher_name = results[email].get('Teacher', None)
                    if DEBUG:
                        print('teacher ', teacher_name)
                    if teacher_name:
                        update_data = {'Formateur Robot': teacher_name}
                        # Update the record in Airtable
                        EXEMPLE_airtable.update(record['id'], update_data)  # Update the record.

def match_teachers_students(EXEMPLE_airtable_test, EXEMPLE_test_records, teachers_calendar_records, recueil_besoins_records, teachers_info_records, current_week_num, CODE_TEST):
    """
    This function, `match_teachers_students`, orchestrates the complex process of matching students with teachers based on availability and specific needs for a given week.
    The function handles multiple sources of data, constructs appropriate graph structures for both teachers and students, solves the matching problem using graph theory, and updates records accordingly.

    This function is central to the system, requiring careful management and optimization due to its complexity and the critical nature of its operation.
    """

    
    
    DEBUG = False
    

    # 1ère étape : synchroniser les données des bases de données en production
    # Dans students_next_week, j'ai besoin de tous les students car ca me permet ensuite de savoir qui a deja un prof
    try:
        students_next_week = extract_students_infos_and_slots(EXEMPLE_test_records, recueil_besoins_records, current_week_num)
        if DEBUG:
            pp = pprint.PrettyPrinter(indent=2)
            pp.pprint(students_next_week)
    except Exception as e:
        print(e)
        raise e
    else:
        if not CODE_TEST:
            print("Succès de l'extraction des données des étudiants")
    
    try:
        students_graph = create_students_struct_for_graph(students_next_week)
        if DEBUG:
            pp = pprint.PrettyPrinter(indent=2)
            print('students_graph')
            pp.pprint(students_graph)
    except Exception as e:
        raise e
        
    try:
        weeks_involved = get_weeks_and_years_involved(students_next_week)
        if (DEBUG):
            print('weeks_involved\n', weeks_involved)
    except Exception as e:
        print(e)
        raise e
    
    
    try:
        teachers_email_list = get_teachers_email_list(teachers_info_records)
        if (DEBUG):
            print('teachers_email_list\n', teachers_email_list)

    except Exception as e:
        print(e)
        raise e 
    else:
        if not CODE_TEST:
            print("Succès de l'extraction de la liste des formateurs")
    
    
    try:
        teachers_calendar_filtered = filter_teacher_availabilities_by_date(weeks_involved, teachers_calendar_records, teachers_email_list)
        if (DEBUG):
            print('teachers_calendar_filtered\n', teachers_calendar_filtered)
    except Exception as e:
        print(e)
        raise e 
    else:
        if not CODE_TEST:
            print("Succès de l'extraction des calendriers des formateurs")   
     
    
    try:
        teachers_graph = extract_and_create_teachers_struct_for_graph(weeks_involved, teachers_info_records, teachers_calendar_filtered)
        if DEBUG:
            print('FIRST GRAPH')
            pp = pprint.PrettyPrinter(indent=2)
            pp.pprint(teachers_graph)
    except Exception as e:
        print(e)
        raise e
    else:
        if not CODE_TEST:
            print("Succès de l'extraction des données des formateurs")
    
    
    try:
        teachers_grap_availabilities = update_teachers_availabilities_with_slot_taken(teachers_graph, EXEMPLE_test_records, weeks_involved)
        if DEBUG:
            print('Teacher graph after taking into account slot given to students')
            pp = pprint.PrettyPrinter(indent=2)
            pp.pprint(teachers_grap_availabilities)
        if not CODE_TEST:
            print("Les disponibilités des formateurs ont été mises à jour avec les créneaux déjà pris par les'elèves")

    except Exception as e:
        raise e

    
    results = graph_solve(teachers_grap_availabilities, students_graph)
    if (DEBUG):
        print('GRAPH RESULT')
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(results)
    
    if (CODE_TEST):
        return results
    
    
    update_airtable_with_results(results, EXEMPLE_test_records, EXEMPLE_airtable_test)
    
                    
    # Je retourne teachers_grap_availabilities car il me permet ensuite de vérifier si les
    # assignations d'eleves a ete faite en respectant les horaires des enseignants
    # par l'algorithm car une fois que c'est assigné je ne peux plus recréer cette data structure 
    return teachers_grap_availabilities




def main():
    """Main function to run the script."""
    DEBUG = False
    BASE_ID = get_env_variable('BASE_ID')
    API_KEY = get_env_variable('API_KEY')

    BASE_ID_EXEMPLE = get_env_variable('BASE_ID_EXEMPLE')
    API_KEY_EXEMPLE = get_env_variable('API_KEY_EXEMPLE')

    # Vrai base de gestion des apprenants 
    # EXEMPLE_airtable = Airtable(BASE_ID_EXEMPLE, EXEMPLE_TABLE_NAME, API_KEY_EXEMPLE)
    # EXEMPLE_records = EXEMPLE_airtable.get_all()
    
    # Base de gestion des apprenants pour faire des tests
    errors_database = []
    EXEMPLE_TABLE_NAME = get_env_variable('EXEMPLE_TABLE_NAME')
    EXEMPLE_airtable = safe_init_airtable(BASE_ID_EXEMPLE, EXEMPLE_TABLE_NAME, API_KEY_EXEMPLE)
    EXEMPLE_test_records = safe_get_all(EXEMPLE_airtable)
    success = check_EXEMPLE_table_name(EXEMPLE_test_records)
    if not success:
        errors_database.append(EXEMPLE_TABLE_NAME)
            
    if (DEBUG):
        print('EXEMPLE_test_records')
        for record in EXEMPLE_test_records:
            if 'Mail' in record['fields'] and record['fields']['Mail']:
                pp = pprint.PrettyPrinter(indent=2)
                pp.pprint(record) 
    
    RECUEIL_DES_BESOINS_TABLE_NAME = get_env_variable('RECUEIL_DES_BESOINS_TABLE_NAME')    
    recueil_besoins_airtable = safe_init_airtable(BASE_ID_EXEMPLE, RECUEIL_DES_BESOINS_TABLE_NAME, API_KEY_EXEMPLE)
    recueil_besoins_records = safe_get_all(recueil_besoins_airtable)
    success = check_recueil_besoins_table_name(recueil_besoins_records)
    if not success:
        errors_database.append(RECUEIL_DES_BESOINS_TABLE_NAME)

 
    TEACHERS_INFO_TABLE_NAME = get_env_variable('TEACHERS_INFO_TABLE_NAME')
    teachers_info_airtable = safe_init_airtable(BASE_ID, TEACHERS_INFO_TABLE_NAME, API_KEY)
    teachers_info_records = safe_get_all(teachers_info_airtable)
    success = check_teachers_info_table_name(teachers_info_records)
    if not success:
        errors_database.append(TEACHERS_INFO_TABLE_NAME)
        
    TEACHERS_CALENDAR = get_env_variable('TEACHERS_CALENDAR')
    teachers_calendar_airtable = safe_init_airtable(BASE_ID, TEACHERS_CALENDAR, API_KEY)
    teachers_calendar_records = safe_get_all(teachers_calendar_airtable)
    success = check_teachers_calendar_table_name(teachers_calendar_records)
    clean_teachers_calendar_records = clean_teachers_calendars(teachers_calendar_records, teachers_calendar_airtable)
    
    # a decommenter pour tester le fonctionnement de l'extraction de donnée
    # return 

    if not success:
        errors_database.append(TEACHERS_INFO_TABLE_NAME)
    

    if (len(errors_database) > 0):
        send_email("EXEMPLE EXEMPLE - Assignation élèves aux formateurs - Erreur",f"Il semblerait que le nom d'une table aiet changé dans {TEACHERS_INFO_TABLE_NAME}", EXEMPLE_EMAIL_RESP_EDT)
        print("Il semblerait qu'il y ait des problèmes dans les bases de données suivantes :\n", errors_database, "\nCorrigez avant de faire tourner car cela va faire crasher le programme")
        return
    else:
        print('La base de donnée est saine. Le programme peut commencer.')
    
    current_week_num = current_week_number()
    if (DEBUG):
        print('current_week_num ', current_week_num)
    
    CODE_TEST = False
    teachers_graph_availabilies_before_assignment = match_teachers_students(EXEMPLE_airtable, EXEMPLE_test_records, clean_teachers_calendar_records, recueil_besoins_records, teachers_info_records, current_week_num, CODE_TEST)
    print('Les formateurs ont été assignés aux étudiants.\nLa base de données a été mise à jour')

    # a decommenter pour ne pas faire fonctionner l'algorithme de vérification
    # return 
    
    # On extrait à nouveau la base de données gestions des apprenants car elle a éte mis à jour et on va regarder s'il n'y a pas d'erreur
    EXEMPLE_airtable_for_control = safe_init_airtable(BASE_ID_EXEMPLE, EXEMPLE_TABLE_NAME, API_KEY_EXEMPLE)
    EXEMPLE_test_records_for_control = safe_get_all(EXEMPLE_airtable_for_control)
    
    print("Vérification des des assignations pour voir s'il n'y a pas d'erreurs")
    matching_control(EXEMPLE_test_records_for_control, recueil_besoins_records, teachers_info_records, current_week_num, teachers_graph_availabilies_before_assignment, clean_teachers_calendar_records)
    eleve_sans_formateur = get_eleve_sans_formateur_next_week(EXEMPLE_test_records_for_control, current_week_num)
    if (len(eleve_sans_formateur) > 0):
        send_email("EXEMPLE EXEMPLE - Attention élèves sans formateurs",f"Il semblerait qu'il y ait des éleves cette semaine ou la prochaine qui n'aient pas de formateurs : {eleve_sans_formateur}", EXEMPLE_EMAIL_RESP_EDT)
        send_email("EXEMPLE EXEMPLE - Attention élèves sans formateurs",f"Il semblerait qu'il y ait des éleves cette semaine ou la prochaine qui n'aient pas de formateurs : {eleve_sans_formateur}", EXEMPLE_EMAIL_CONTACT)

        print("Il semblerait qu'il y ait des éleves cette semaine ou la prochaine qui n'aient pas de formateurs\n", eleve_sans_formateur)
    else :
        print('Tous les élèves de cette semaine et de la prochaine ont un formateur')
    return 

if __name__ == "__main__":
    try:
        main()
    except Exception as e:

        send_email("EXEMPLE EXEMPLE - Assignation élèves aux formateurs - Erreur",f"Erreur dans le deploiement du code. Checker", EXEMPLE_EMAIL_RESP_DEV)

        raise e