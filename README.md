## Table of Contents
1. [Project Overview](#project-overview)
2. [Technologies Used](#technologies-used)
3. [Lessons Learned and Challenges](#lessons-learned-and-challenges)
4. [Other Information](#other-information)

---

## Project Overview

### Description
This project aims to match the schedules of students and teachers while adhering to several constraints and order of priority (see graph.py to learn about the constraints).
For instance, teacher with less skills must be privileged, or the mode of teaching is a constraint, etc. 
To achieve this, a significant amount of data extraction work is needed to format the data in order to feed it to the graph. Each function is explained. 
I recommend starting by reading the match_teachers_students.py and graph.py files to better understand the project.

## Technologies Used

- **Language**: Python,
- **Packages**: Pulp, AirTable
- **Deployment**: Shadow PC.

## Lessons Learned and Challenges

I have faced multiple challenges. I almost did not know about python, graph, airtable before doing this.

Finding a solution to the request has been challenging as I had no prior knowledge in graph solving problem with pulp. I first tried with backtracking,
but the time to find the most efficient match between teacher and student was far too long. So I began learning about graph and pulp. 

Moreover, as the goal was to deploy it and it is possible that later another programmer take the lead on that, I put attention on:
- the making of tests,
- having a clear and understandable code (function name, commentaries). It is a kind of Frenglish as the future developer will be French for sure.
- clear structure
- handling error with email sending

Another challenge was the deployment as this program will be used by non-tech people using Windows at their discretion.
I find the best price-to-practicality ratio by using Shadow PC and putting a shortcut to launch the program. I handle error with email sending also
in order to be aware if any problem happened.

## Other Information
- There is only one commit as the production project is in a private repo to avoid linking any risky information.
- All private information has been replaced by "EXAMPLE".
- Launch the program: `python match_teachers_students.py`
- Run tests: `python ./test/match_teachers_students/test_match_teachers_students.py`
It is not available for you as a lot of .env are missing here.
