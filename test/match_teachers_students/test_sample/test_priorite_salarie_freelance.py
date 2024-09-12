import sys
import os

sys.path.append('../matching_algorithm')
path_matching_algorithm = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(path_matching_algorithm)
path_to_match_teachers_students_data_test = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(path_to_match_teachers_students_data_test)

from match_teachers_students import match_teachers_students

formateurs_infos = [
{ 'createdTime': '2024-04-17T10:53:01.000Z',
    'fields': { 'Compétences': ['Fusion'],
                'Mode': ['distanciel'],
                'Nom': 'quentin@example.fr',
                'Session par semaine': 12,
                'Statut': 'Freelance'},
    'id': '1'},
{ 'createdTime': '2024-04-17T10:53:02.000Z',
    'fields': { 'Compétences': ['Fusion'],
                'Mode': ['distanciel'],
                'Nom': 'adrien@example.fr',
                'Session par semaine': 12,
                'Statut': 'Salarié'},
    'id': '774742'}]

EXEMPLE = [
    {'createdTime': '2024-03-19T09:11:49.000Z',
    'fields': {
                'Formateur': '',
                'Formateur Robot': '',
                'Formation': "Fusion 360 à destination d'un designer 3D",
                'Premiere partie': '2024-04-29T06:00:00.000Z',
                'Deuxieme partie': '2024-05-06T06:00:00.000Z',
                'Mail': 'eleve1@gmail.com'},
    'id': 'rec5AsOBDQmhLHEz5'}]

recueil_besoins_apprenants = [
{ 'createdTime': '2024-03-26T15:33:19.000Z',
    'fields': { 
                'Email': 'eleve1@gmail.com',
                'Lieu': 'Distanciel',},
    'id': 'rec0HWq51qAr4IlS'}]

formateurs_calendars = [
{'id': 'rec0DQAls8iP58yT9',
 'createdTime': '2024-06-13T15:41:50.000Z',
 'fields': {'Title': 'Indisponible',
            'Start': '2024-04-29T17:00:00.000Z',
            'End': '2024-04-29T19:00:00.000Z',
            'Creator': 'quentin@example.fr'}
},
{'id': 'rec0DQAls8iP5MyT9',
 'createdTime': '2024-06-13T13:41:50.000Z',
 'fields': {'Title': 'Indisponible',
            'Start': '2024-04-29T12:00:00.000Z',
            'End': '2024-04-29T16:00:00.000Z',
            'Creator': 'adrien@example.fr'}
}
]

# (function) def match_teachers_students(
#     EXEMPLE_airtable_test: Any,
#     EXEMPLE_test_records: Any,
#     teachers_calendar_records: Any,
#     recueil_besoins_records: Any,
#     teachers_info_records: Any,
#     current_week_num: Any,
#     CODE_TEST: Any
# ) -> Any

output_expected = { 'eleve1@gmail.com': { 'Assigned Slots': { 18: ['2024-04-29 09:00'],
                                            19: ['2024-05-06 09:00']},
                        'Teacher': 'adrien@example.fr'}}

def test_priorite_salarie_freelance(current_week_num, CODE_TEST):
    
    
    output = match_teachers_students(None, EXEMPLE, formateurs_calendars, recueil_besoins_apprenants, formateurs_infos, current_week_num, CODE_TEST)    
    
    try:
        assert output in [output_expected], f"Test failed: Expected {output_expected}, got {output}"
    except AssertionError as e:
        print(e)
        return False
    
    return True
