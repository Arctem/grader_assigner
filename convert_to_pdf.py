import shlex
import subprocess
import os

import schedule_grading
import grader

base_start = r"""\documentclass[9pt, onecolumn]{extarticle}
%\usepackage[top=1.0in, left=1.0in, right=1.0in, bottom=1.0in]{geometry}
\usepackage{longtable}
\usepackage{hyperref}
\title{$ass_name}
\date{}
\begin{document}

\maketitle{}

$ass_desc

\begin{center}
\begin{longtable}{| l | l | l | l |}
\hline
\textbf{Student Last} & \textbf{Student First} & \textbf{Grader Name} & \textbf{Grader Email} \\
\hline
\endfirsthead
\multicolumn{4}{c}%
{\tablename\ \thetable\ -- \textit{Continued from previous page}} \\
\hline
\textbf{Student Last} & \textbf{Student First} & \textbf{Grader Name} & \textbf{Grader Email} \\
\hline
\endhead
\hline \multicolumn{4}{r}{\textit{Continued on next page}} \\
\endfoot
\hline
\endlastfoot""" + "\n"

base_end = r"""\end{longtable}
\end{center}
\end{document}""" + "\n"


def make_pdf(assignment, graders, output_filename=None):
    start_filename = assignment.id + '.csv'
    tex_filename = assignment.id + '.tex'
    if not output_filename:
        output_filename = '$ass_id'
    output_filename = output_filename.replace('$ass_name',
        assignment.long_name).replace('$ass_id', assignment.id)

    if not pdf_title:
        pdf_title = '$ass_name'
    
    pdf_title = pdf_title.replace('$ass_name', assignment.long_name)\
        .replace('$ass_id', assignment.id)

    with open(start_filename, 'r') as csv_file:
        lines = csv_file.readlines()
    lines = sorted(map(lambda x: x.strip().split(';'), lines), key=lambda l:l[3] + ', ' + l[2])
    print(lines)
    with open(tex_filename, 'w') as tex_file:
        start = base_start.replace('$ass_name', assignment.long_name)
        start = start.replace('$ass_desc', assignment.desc)
        tex_file.write(start)
        for line in lines:
            grader_name = line[0], line[1]
            grader = None
            for g in graders:
                if grader_name == g.name:
                    grader = g
            if not grader:
                schedule_grading.error('Could not match grader {}.'.format(grader_name))
            else:
                tex_file.write('\t{0} & {1} & {2} {3} & \\href{{mailto:{4}}}{{{4}}}\\\\\\hline\n'\
                    .format(line[3], line[2], grader.name[0], grader.name[1], grader.email))

        tex_file.write(base_end)

    #running this twice because LaTeX is dumb like that
    for i in range(2):
        proc=subprocess.Popen(shlex.split(
            'pdflatex -interactive=nonstopmode -jobname="{}" {}'
            .format(output_filename, tex_filename)))
        proc.communicate()
    proc=subprocess.Popen(shlex.split(
        'rm "{0}.tex" "{1}.out" "{1}.log" "{1}.aux"'.format(assignment.id,
            output_filename)))
    proc.communicate()


def main():
    graders = schedule_grading.load_graders('graders.csv')
    assignments = schedule_grading.load_assignments('assignment_list.txt')
    try:
        with open('output_pdf.txt', 'r') as output_pdf:
            output_filename = output_pdf.read().strip()
    except FileNotFoundError:
        schedule_grading.warning('Could not open output_pdf.txt.')
        output_filename = None

    for assignment in assignments:
        filename = assignment.id + '.csv'
        if os.path.isfile(filename):
            make_pdf(assignment, graders, output_filename)


if __name__ == '__main__':
    main()
