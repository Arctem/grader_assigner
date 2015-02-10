# Grader Assigner
A script to assign graders for use by the New Mexico Tech CS department.

### Recommended use

Create a subdirectory, put the lists of graders, students, assignments inside in the same
format as in test_case. If applicable, add any historical data in files named
{assignment_name}.csv. Then run `python ../schedule_grading.py` as many times as necessary.

### TODO
* Make a better name.
* Add script to convert assignment .csv files into .pdf (or at least .tex).
* Add weights to allow graders to prefer or avoid certain students.