class Assignment:
    def __init__(self, line):
        line = line.split(';', 3)
        self.id = line[0]
        self.long_name = line[1] if len(line) > 1 else self.id
        self.desc = line[2] if len(line) > 2 else ''


    def __repr__(self):
        return '{} ({}): {}'.format(self.id, self.long_name, self.desc)