from utils.date import get_number_of_the_week, get_year

def get_weeks_and_years_involved(students_next_week):
    """ Cette fonction permet de savoir dans quelle année est la semaine concernée en renvoyant un set avec [(18, 2024), (19, 2024)]
    """
    # Initialize an empty set to hold unique combinations of weeks and years
    unique_weeks_and_years = set()

    for entry in students_next_week:
        for key in entry:
            if "Creneaux" in key and entry[key] is not None:
                date = entry[key]
                week_number = get_number_of_the_week(date)
                year = get_year(date)  # You need to have a function to get the year from the date
                unique_weeks_and_years.add((week_number, year))

    # Convert the set of tuples into a sorted list. 
    # The sorting is done first by year and then by week number within each year
    unique_weeks_and_years_list = sorted(unique_weeks_and_years, key=lambda x: (x[1], x[0]))
    return unique_weeks_and_years_list