import sys
import os

sys.path.append('../matching_algorithm')
path_matching_algorithm = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(path_matching_algorithm)
path_to_match_teachers_students_data_test = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(path_to_match_teachers_students_data_test)

from test_sample.test_priorite_salarie_freelance import test_priorite_salarie_freelance
from test_sample.test_match_skills import test_match_skills
from test_sample.test_double_assignation import test_double_assignation
from test_sample.test_priorite_competences import test_priorite_competences
from test_sample.test_assignation_available import test_assignation_available
from test_sample.test_limit_quota import test_limit_quota
from test_sample.test_teaching_mode import test_teaching_mode
from test_sample.test_student_already_taken import test_student_already_taken
from test_sample.test_calendar_format import test_calendar_format

def main():
    """Main function to run the script."""
    
    DEBUG = True
    CODE_TEST = True
    current_week_num = 18
    
    # s'assurer qu'il y a priorité du salarié sur le freelance
    success = test_priorite_salarie_freelance(current_week_num, CODE_TEST)
    if not success:
        print('test_priorite_salarie_freelance failed')
    else :
        print('test_priorite_salarie_freelance succeed')
            
    # assurer que les competences sont bien matches ou pas matches 
    success = test_match_skills(current_week_num, CODE_TEST)
    if not success:
        print('test_match_skills failed')
    else :
        print('test_match_skills succeed')
        
    # verifie qu'il n'y a pas de double assignation
    success = test_double_assignation(current_week_num, CODE_TEST)
    if not success:
        print('test_double_assignation failed')
    else :
        print('test_double_assignation succeed')

    
    # s'assurer que si un prof a une competence et l'autre deux compétences,
    # on attribue pas la compétence commune au prof avec la double compétence 
    # Cette fonctionnalité n'est pas hardcodé, mais est mis en lumiere par la recherche d'optimisation de l algorithme.
    # S'il y a plus de prof que necessaire. Il n'y aura pas forcement de priorité dans ce cas.
    success = test_priorite_competences(current_week_num, CODE_TEST)
    if not success:
        print('test_priorite_salarie_freelance failed')
    else :
        print('test_priorite_salarie_freelance succeed')
        
    ### s'assurer que si un un prof n'est disponible que sur un créneau pour un éleve, il n'est pas attribué
    success = test_assignation_available(current_week_num, CODE_TEST)
    if not success:
        print('test_assignation_available failed')  
    else :
        print('test_assignation_available succeed')
        
    ### s'assurer que le nombre de quota des profs est respecté
    success = test_limit_quota(current_week_num, CODE_TEST)
    if not success:
        print('test_limit_quota failed')  
    else :
        print('test_limit_quota succeed')
        
    ### s'assurer que il y a le respect des modes d'enseignement et que le prof n'est pas assigné, s'il ne peut enseigner qu'à distance, a un eleve en présentiel
    success = test_teaching_mode(current_week_num, CODE_TEST)
    if not success:
        print('test_teaching_mode failed')
    else :
        print('test_teaching_mode succeed')
        
    # s'assurer que l algorithm prend bien en comptes les eleves deja attribues pour ne pas remettre le slot du prof deja pris
    success = test_student_already_taken(current_week_num, CODE_TEST)
    if not success:
        print('test_student_already_taken failed')
    else :
        print('test_student_already_taken succeed')
        
    success = test_calendar_format(current_week_num, CODE_TEST)
    if not success:
        print('test_calendar_format failed')
    else :
        print('test_calendar_format succeed')
    
    return 

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        raise e