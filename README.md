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

##### [`assignment_list.txt`](test_case/assignment_list.txt)
This file should be a semicolon-delimited CSV of the assignments for a class.
The columns for the file should be as follows:

| Assignment ID | Assignment Long Name | Assignment Description |
|---------------|----------------------|------------------------|

There should be no spacess around the semicolons. Assignment ID should generally
be a short descriptor like "lab4" or "hw2". Assignment Long Name will be used
on the grader sheet PDF and should generally be something like "Lab 4" or
"Homework 2". The assignment Description might include, for example,
instructions on the latest date on which a student could email their grader.

Assignment Long Name and Description are both optional. If the Long Name is
not defined, the ID will be used instead. If the Description is not defined, an
empty string will be used. The Long Name is required if the Description is used.

Assignments should be listed in chronological order.

##### [`graders.csv`](test_case/graders.csv)
This file should be a semicolon-delimited CSV of the graders for a class. The columns for the
file should be as follows:

| Grader First Name | Grader Last Name | Grader Email | Max Students |
|-------------------|------------------|--------------|--------------|

There should be no spaces around the semicolons. Maximum students per assignment
 should be in the form of an integer, with
an optional addition to specify "overflow" students. Overflow students indicate
that a grader can be
assigned an additional number of students, but only if it is impossible to use
up any grader's normal students for the assignment.
The syntax for this column should be <normal_students>+<overflow_students>. For
example, a grader who
is not normally supposed to grade students but can grade 2 students in the case
where a scheduling conflict occurs would have 0+2 in their max students column.

##### [`students.csv`](test_case/students.csv)
This file should be a semicolon-delimited CSV of the students for a class. The columns for the
file should be as follows:

| Student First Name | Student Last Name |
|--------------------|-------------------|

There should be no spaces around the semicolons.

#### Optional Files
Examples of these files are in the [`test_case`](test_case) subdirectory of the project.

##### [`weights.csv`](test_case/weights.csv)
This file should be a semicolon-delimited CSV specifying the weights for various graders
and students in a class. This can be used to indicate whether a grader should not grade
a specific student (weight of 0), whether they should grade a student less frequently
than normal (weight < 1), or grade a student more frequently than normal (weight > 1).
If no weight is specified, it is assumed to be 1.

| Grader First Name | Grader Last Name | Student First Name | Student Last Name | Weight |
|-------------------|------------------|--------------------|-------------------|--------|

##### [`output_pdf.txt`](test_case/output_pdf.txt)
This file should be a single line consisting of the desired naming style for the
output PDF, excluding the `.pdf` suffix. This line should include either the
string
`$ass_name`, which will be replaced by the Long Name of the relevant assignment
when the PDF is produced,
or `$ass_id`, which will be replaced by the ID of the relevant assignment.
If this file does not exist, the assignment's ID will
be used instead. If this file exists but neither `$ass_name` nor `$ass_id`
are inside, the produced
PDFs will overwrite one another due to name collisions. This line will also be
used for the title of the PDF.

The filename should not contain multiple lines, `/`, quotes, or any other
special file system characters.

##### [Historical files.](test_case/lab1.csv)
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