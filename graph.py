import pulp

def graph_solve(teachers, students):
    """ Le fonctionnement de cette fonction est obscure. Des testeurs ont été crées pour s'assurer qu'elle fonctionne bien.
    Le but est d'assigner les eleves aux formateurs en respectant des contraintes de match entre élèves et formateurs. 
    
    On peut retrouver ces contraintes au dessus de chaque ligne de code concernée, mais pour rappel :
    - le salarié doit être favorisé par rapport au free-lance
    - il faut un match des compétences
    - il faut un match des lieux de formation (presentiel/distanciel)
    - match des creneaux
    - que le formateur ait assez de sessions
    
    Ensuite, cet algorithm va optimiser cela et on va créer une structure de sortie dans results comme celle-là pour qu'on puisse facilement mettre à jour la table: 
    {
        'eleve10@gmail.com': { 'Assigned Slots': { 18: ['2024-05-02 09:00'],
                                             19: ['2024-05-09 09:00']},
                         'Teacher': 'malom@example.fr'},
        'eleve11@gmail.com': { 'Assigned Slots': { 18: ['2024-05-02 14:00'],
                                             19: ['2024-05-09 14:00']},
                         'Teacher': 'malom@example.fr'},
        'eleve12@gmail.com': {'Assigned Slots': {}, 'Teacher': None}
    }
    """
    DEBUG = False
    
    model = pulp.LpProblem("Complete_Teacher_Student_Assignment", pulp.LpMaximize)

    # Define weights based on type
    weights = {'salarié': 2, 'freelance': 1}

    # Variables for assignment
    x = pulp.LpVariable.dicts("assign", 
                            ((s, t, slot) for s in students for t in teachers for slot in students[s]['courses'] 
                            if str(students[s]['weeks'][slot]) in teachers[t]['slots'] and slot in teachers[t]['slots'][str(students[s]['weeks'][slot])]),
                            cat=pulp.LpBinary)

    # Binary variables indicating if a student is assigned to a particular teacher
    y = pulp.LpVariable.dicts("teacher_assigned", ((s, t) for s in students for t in teachers), cat=pulp.LpBinary)

    # Objective: Maximize the weighted number of student-slot-teacher assignments
    model += pulp.lpSum(weights[teachers[t]['type']] * x[s, t, slot] 
                        for s in students 
                        for t in teachers 
                        for slot in students[s]['courses'] 
                        if (s, t, slot) in x), "Weighted_Maximize_assignments"

    # Constraint to ensure each student is assigned to at most one teacher
    for s in students:
        model += pulp.lpSum(y[s, t] for t in teachers) <= 1, f"At_most_one_teacher_per_student_{s}"

    # Constraint ensuring a teacher is assigned only if they cover all student slots
    for s in students:
        for t in teachers:
            model += pulp.lpSum(x[s, t, slot] for slot in students[s]['courses'] 
                                if str(students[s]['weeks'][slot]) in teachers[t]['slots'] and 
                                slot in teachers[t]['slots'][str(students[s]['weeks'][slot])]) >= len(students[s]['courses']) * y[s, t], f"All_Slots_Covered_{s}_{t}"

    # Constraints to ensure teachers do not exceed their maximum days of work per week
    for t in teachers:
        for w in teachers[t]['max_days']:
            model += pulp.lpSum(x[s, t, c] for s in students for c in students[s]['courses']
                                if (s, t, c) in x and students[s]['weeks'][c] == int(w)) <= teachers[t]['max_days'][w], f"Max_days_for_{t}_week_{w}"

    # Constraint to link assignment variables to teacher assignment indicators
    for s in students:
        for t in teachers:
            model += pulp.lpSum(x[s, t, slot] for slot in students[s]['courses'] if (s, t, slot) in x) <= len(students[s]['courses']) * y[s, t], f"Link_{s}_{t}"


    for s in students:
        for t in teachers:
            # Ensure that each assignment matches the possible modes of interaction (présentiel or distanciel)
            if students[s]['mode'] in teachers[t]['mode']:
                # If the modes are compatible, existing constraints for linking and slot coverage remain unchanged
                pass
            else:
                # If the modes do not match, ensure no assignment is possible
                model += y[s, t] == 0, f"Mode_Mismatch_{s}_{t}"


    for s in students:
        for t in teachers:
            # Make sure the teacher has all the skills required by the student
            if all(skill in teachers[t]['skills'] for skill in students[s]['skills']):
                # If the skills match, existing constraints handle assignment feasibility
                pass
            else:
                # If the teacher does not have the required skills, they cannot be assigned to this student
                model += y[s, t] == 0, f"Skills_Mismatch_{s}_{t}"

    # New constraint to ensure one teacher is assigned to only one student per time slot
    for t in teachers:
        for w in set(sum([list(students[s]['weeks'].values()) for s in students], [])):
            for slot in set(sum([list(students[s]['courses']) for s in students], [])):
                model += pulp.lpSum(x[s, t, slot] for s in students if (s, t, slot) in x and slot in students[s]['courses'] and students[s]['weeks'][slot] == w) <= 1, f"One_student_per_slot_{t}_{w}_{slot}"

    # Solve the problem
    # model.solve()
    model.solve(pulp.PULP_CBC_CMD(msg=False))

    # Print the results
    if (DEBUG):
        print("Final Assignments:")
        for s in students:
            assigned_teacher = None
            for t in teachers:
                if pulp.value(y[s, t]) == 1:
                    assigned_teacher = t
                    break
            if assigned_teacher:
                print(f"Student {s} is assigned to Teacher {assigned_teacher}:")
                for slot in students[s]['courses']:
                    if (s, assigned_teacher, slot) in x and pulp.value(x[(s, assigned_teacher, slot)]) == 1:
                        print(f"  - Slot {slot} in Week {students[s]['weeks'][slot]}")
            else:
                print(f"Student {s} is not assigned to any teacher.")

    # Check if any teacher has no assignments
        for t in teachers:
            if all(pulp.value(x.get((s, t, slot), 0)) == 0 for s in students for slot in students[s]['courses'] if (s, t, slot) in x):
                print(f"Teacher {t} has no assignments.")

    # This is a placeholder for your solution setup. You need to properly initialize and solve your pulp problem here.

    results = {}
    for s in students:
        for t in teachers:
            if pulp.value(y.get((s, t), 0)) == 1:
                if s not in results:
                    results[s] = {'Teacher': t, 'Assigned Slots': {}}
                for slot in students[s]['courses']:
                    if (s, t, slot) in x and pulp.value(x[(s, t, slot)]) == 1:
                        week = students[s]['weeks'][slot]
                        if week not in results[s]['Assigned Slots']:
                            results[s]['Assigned Slots'][week] = []
                        results[s]['Assigned Slots'][week].append(slot)
        if s not in results:
            results[s] = {'Teacher': None, 'Assigned Slots': {}}
    
    return results
