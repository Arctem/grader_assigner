class Grader:
    def __init__(self, line):
        line = line.split(';')
        self.name = (line[0], line[1])
        self.email = line[2]
        
        hours = line[3].split('+')
        self.overflow = int(hours[-1]) if len(hours) > 1 else 0
        self.hours = int(hours[0])

    def __repr__(self):
        return '{} {} ({})'.format(self.name[0], self.name[1], self.email)