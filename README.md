# Grader Assigner
A script to assign graders for use by the New Mexico Tech CS department.

## Recommended use
Create a subdirectory, populate it with the required files as well as any desired optional
files.

Run `python ../schedule_grading.py` to generate a grading sheet for first assignment without
a corresponding CSV file. If an error occurs, a CSV for the assignment will not be produced.
In most cases, simply running the script again will result in a valid schedule being produced
(due to a different random seed being used), but if the error is due to invalid data in one
of the required or optional files, those errors will need to be corrected first.

Run `python ../convert_to_pdf.py` to convert all assignment CSVs into PDF files fit for
distribution.

## Prerequisites
These scripts are designed to be run under Python 3.4.

[`convert_to_pdf.py`](convert_to_pdf.py) requires pdflatex to be in the system's `PATH`.

Having the Python module `colorama` installed will allow errors and warning to display
with colored text.

#### Required Files
Examples of these files are in the [`test_case`](test_case) subdirectory of the project.

##### assignment_list.txt
This file should be a list of the assignments in the class that need to have graders assigned.
Each line should list one assignment, with all of the files being in chronological order.

##### graders.csv
This file should be a semicolon-delimited CSV of the graders for a class. The columns for the
file should be as follows:

| Grader First Name | Grader Last Name | Grader Email | Grader Hours |
|-------------------|------------------|--------------|--------------|

There should be no spaces around the semicolons. Hours should be in the form of an integer, with
an optional addition to specify "overflow" hours. Overflow hours indicate that a grader can be
assigned an additional number of grading hours, but only if no normal hours are available.
The syntax for this column should be <normal_hours>+<overflow_hours>. For example, a grader who
is not normally supposed to grade students but can grade 2 students in the case where a
scheduling conflict occurs would have 0+2 in their hours column.

##### students.csv
This file should be a semicolon-delimited CSV of the students for a class. The columns for the
file should be as follows:

| Student First Name | Student Last Name |
|--------------------|-------------------|

There should be no spaces around the semicolons.

#### Optional Files
Examples of these files are in the [`test_case`](test_case) subdirectory of the project.

##### weights.csv
This file should be a semicolon-delimited CSV specifying the weights for various graders
and students in a class. This cat be used to indicate whether a grader should not grade
a specific student (weight of 0), whether they should grade a student less frequently
than normal (weight < 1), or grade a student more frequently than normal (weight > 1).
If no weight is specified, it is assumed to be 1.

| Grader First Name | Grader Last Name | Student First Name | Student Last Name | Weight |
|-------------------|------------------|--------------------|-------------------|--------|

##### Historical files.
These files can be used to indicate previous grading assignments and should be in the same
format as the CSVs generated by running [`schedule_grading.py`](schedule_grading.py). They
should be simple lists of a grader followed by a student they graded. A grader can appear
multiple times, though a student should appear at most once. A student appearing multiple
times will not produce an error, but may result in a schedule being less likely to be
produced.

| Grader First Name | Grader Last Name | Student First Name | Student Last Name |
|-------------------|------------------|--------------------|-------------------|

## Known Bugs
* Graders with underscores in their emails will produce incorrect PDFs. This can be fixed by
placing a backslash before the underscore inside graders.csv.

## TODO
* Make a better name.