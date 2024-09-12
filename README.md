# Project Name

A brief description of the project, what it does, and its main objectives.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Technologies Used](#technologies-used)
3. [Lessons Learned & Challenges](#Lessons_Learned_&_Challenges)
4. [Others informations](#others_informations)

---

## Project Overview

### Description
This project aims to match the schedules of students and teachers while adhering to several constraints and order of priority (see graph.py to learn about the constraints).
For instance, teacher with less skills must be privileged, or the mode of teaching is a constraint, etc. 
To achieve this, a significant amount of data extraction work is needed to format the data in order to feed it to the graph. Each function is explained. 
I recommend starting by reading the match_teachers_students.py and graph.py files to better understand the project.

## Technologies Used

- List all the programming languages, frameworks, libraries, or tools that you used in the project, e.g.:
  - **Language**: Python,
  - **Packages**: Pulp, AirTable
  - **Deployment**: Shadow PC.

### Lessons Learned & Challenges

I have face multiple challenge. I almost did not know about python, graph, airtable before doing this.

Finding a solution to the request has been challenging has I had no prior knowledge in graph solving problem with pulp. I first try with backtracking,
but the time to find the most efficent match between teacher and student was far too long. So I began learning about graph and pulp. 

Moreover, as the goal was to deploy it and it is possible that later another programmer take the lead on that, I put attention on :
- the making test,
- having a clear and understandable code (function name, commentaries). It is a kind of frenglish as the future developer will be French for sure.
- clear structure
- handling error with email sending

Another challenge was the deployment as this program will be used by non-tech people using Windows at their discretion.
I find the best price-to-practicality ratio by using Shadow PC and putting an shorcut to lunch the program. I handle error with email sending also
in order to be aware if any problem happened.

### Others informations
- There is only one commit as the production project is in a private repo to avoid linking any risky information
- All private information has been replaced by "EXAMPLE
- Lancer le programme : python match_teachers_students.py
- lancer les tests : python ./test/match_teachers_students/test_match_teachers_students.py
It is not available for you as a lot of .env are missing here.
---

