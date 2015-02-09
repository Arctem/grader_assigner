class Student:
    def __init__(self, line):
        line = line.split(';')
        self.name = (line[0], line[1])

    def __repr__(self):
        return '{} {}'.format(self.name[0], self.name[1])