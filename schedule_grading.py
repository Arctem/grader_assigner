import os
import random
import sys

try:
    import colorama
    colorama.init()
    from colorama import Fore
except ImportError:
    print('For extra useless functionality, install colorama.')
    colorama = None

from grader import Grader
from student import Student

error_occured = False


def load_graders(filename):
    graders = []
    with open(filename, 'r') as gfile:
        for line in gfile:
            line = line.strip()
            if line != '':
                graders.append(Grader(line))
    return graders

def load_students(filename):
    students = []
    with open(filename, 'r') as sfile:
        for line in sfile:
            line = line.strip()
            if line != '':
                students.append(Student(line))
    return students

def load_assignments(filename):
    assignments = []
    with open(filename, 'r') as afile:
        for line in afile:
            assignments.append(line.strip())
    return assignments

def load_weights(filename, graders, students):
    weights = {}
    for grader in graders:
        weights[grader] = {}
    try:
        with open(filename, 'r') as wfile:
            for line in wfile:
                line = line.split(';')
                grader_name = line[0], line[1]
                student_name = line[2], line[3]
                weight = float(line[4])

                grader = None
                student = None
                for g in graders:
                    if g.name == grader_name:
                        grader = g
                for s in students:
                    if s.name == student_name:
                        student = s

                if not grader:
                    error('Could not match grader {} in {}.'.format(grader_name, filename))
                    error('A former grader should be simply given a limit of 0 to grade.')
                if not student:
                    error('Could not match student {} in {}.'.format(student_name, filename))
                if grader and student:
                    weights[grader][student] = weight
    except FileNotFoundError:
        warning('No {} file found.'.format(filename))
    return weights

def load_history(assignments, graders, students):
    data = {}

    for assignment in assignments:
        filename = assignment + '.csv'
        if os.path.isfile(filename):
            data[assignment] = load_history_file(filename, graders, students)
        else:
            break
    print('Loaded history for first {} assignments.'.format(len(data.keys())))

    return data

def load_history_file(filename, graders, students):
    data = {}
    for grader in graders:
        data[grader] = []
    with open(filename, 'r') as history_file:
        for line in history_file:
            line = line.strip().split(';')
            if len(line) != 4 and line != []:
                error('Invalid line in {}: {}'.format(filename, line))

            grader_name = line[0], line[1]
            student_name = line[2], line[3]
            grader = None
            student = None
            for g in graders:
                if g.name == grader_name:
                    grader = g
            for s in students:
                if s.name == student_name:
                    student = s

            if not grader:
                error('Could not match grader {} in {}.'.format(grader_name, filename))
                error('A former grader should be simply given a limit of 0 to grade.')
            if not student:
                warning('Could not match student {} in {}.'.format(student_name, filename))
            if grader and student:
                data[grader].append(student)

    return data

#tslg: time since last graded
def calculate_tslg(assignments, history, graders, students):
    counter = 1
    tslg = {}
    for grader in graders:
        tslg[grader] = {}
    assignments = assignments[::-1]
    for assignment in assignments:
        data = history[assignment]

        for grader in data:
            for student in data[grader]:
                if student not in tslg[grader]:
                    tslg[grader][student] = counter

        counter += 1

    for grader in graders:
        for student in students:
            if student not in tslg[grader].keys():
                tslg[grader][student] = counter + 1

    return tslg

def apply_weights(tslg, weights):
    for grader in weights:
        for student in weights[grader]:
            tslg[grader][student] *= weights[grader][student]
    return tslg

def get_max_tslg(tslg, student):
    return max(map(lambda g: tslg[g][student], tslg))

def split_students_by_tslg(tslg, students):
    split_students = {}
    for student in students:
        max_tslg = get_max_tslg(tslg, student)
        if max_tslg not in split_students:
            split_students[max_tslg] = []
        split_students[max_tslg].append(student)

    return split_students

def split_graders_by_tslg(tslg, graders, student):
    split_graders = {}
    for grader in graders:
        time = tslg[grader][student]
        if time not in split_graders:
            split_graders[time] = []
        split_graders[time].append(grader)

    return split_graders

def make_grader_list(tslg, graders, students):
    #sorts students so that those with the longest tslg are first
    #sorted_students = sorted(students, key=lambda s: get_max_tslg(tslg, s), reverse=True)

    grader_list = {}
    overflow_graders = list(filter(lambda g: g.overflow > 0, graders))
    for grader in graders:
        grader_list[grader] = []

    split_students = split_students_by_tslg(tslg, students)

    for group in sorted(split_students.keys(), reverse=True):
        random.shuffle(split_students[group])
        print('Group {}: {}'.format(group, split_students[group]))

        for student in split_students[group]:
            split_graders = split_graders_by_tslg(tslg, graders, student)

            assigned = False

            for grader_group in sorted(split_graders.keys(), reverse=True):
                random.shuffle(split_graders[grader_group])

                for grader in split_graders[grader_group]:
                    if len(grader_list[grader]) < grader.hours and grader_group > 1:
                        assigned = True
                        grader_list[grader].append(student)
                        break
                if assigned:
                    break

            if not assigned:
                #print(overflow_graders, student)
                overflow_selection = sorted(overflow_graders,\
                    key=lambda g: tslg[g][student], reverse=True)
                overflow_selection = list(filter(lambda g:\
                    len(grader_list[g]) < g.overflow, overflow_selection))

                overflow_selection = overflow_selection[0] if overflow_selection else None

                #print()
                #print(student)
                #print(split_graders)
                #print(grader_list)
                #print()

                if not overflow_selection or tslg[overflow_selection][student] <= 1:
                    error('{} was not assigned a grader.'.format(student))
                else:
                    assigned = True
                    grader_list[overflow_selection].append(student)
                    warning('{} was assigned to an overflow grader.'.format(student))

    #print(grader_list)
    return grader_list

def write_to_csv(grader_list, assignment):
    lines = []
    for grader in grader_list:
        for student in grader_list[grader]:
            line = ';'.join(grader.name + student.name) + '\n'
            lines.append(line)

    with open(assignment + '.csv', 'w') as csv_file:
        csv_file.writelines(lines)


def error(msg):
    global error_occured
    error_occured = True

    if colorama:
        print('{} ERROR: {}{}'.format(Fore.RED, msg, Fore.RESET))
    else:
        print(' ERROR: {}'.format(msg))

def warning(msg):
    if colorama:
        print('{} WARNING: {}{}'.format(Fore.YELLOW, msg, Fore.RESET))
    else:
        print(' WARNING: {}'.format(msg))


def main():
    global error_occured

    seed = random.randint(0, 2**20)
    print('Using random seed {}.'.format(seed))
    random.seed(seed)

    graders = load_graders('graders.csv')
    students = load_students('students.csv')    
    assignments = load_assignments('assignment_list.txt')
    weights = load_weights('weights.csv', graders, students)

    graders.sort(key=lambda g:g.hours + 0.5 if g.overflow else 0)
    students.sort(key=lambda s:(s.name[1], s.name[0]))

    #print(graders)
    #print(students)
    #print(assignments)

    history = load_history(assignments, graders, students)

    graded_assignments = assignments[:len(history.keys())]
    if len(graded_assignments) == len(assignments):
        warning('All assignments have been graded.')
        sys.exit(0)
    next_assignment = assignments[len(history.keys())]

    tslg = calculate_tslg(graded_assignments, history, graders, students)
    tslg = apply_weights(tslg, weights)

    #to be used to specify which graders shouldn't grade certain students, for example
    #history = adjust_with_weights(history)

    next_list = make_grader_list(tslg, graders, students)

    if not error_occured:
        write_to_csv(next_list, next_assignment)
        print('Wrote to {}.csv.'.format(next_assignment))
        sys.exit(0)
    else:
        error('Did not write CSV due to error.')
        sys.exit(-1)

if __name__ == '__main__':
    main()
