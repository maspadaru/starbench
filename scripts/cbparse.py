import string
import sys
import os

OPERATOR_BOX = "B"
OPERATOR_DIAMOND = "D"

def print_help():
    print ('Usage: python cbparse.py Option Arguments DirectoryPath')
    print ('Options: ')
    print ('    S: parse chasebench data dir - Source Instance')
    print ('        Arguments: timeline_size')
    print ('    T: parse chasebench dependecies dir - TGDs')
    print ('        Arguments: window_size percent_box percent_diamond '\
            'percent_event')
    print (' ')
    print ('Example: python cbparse.py D 1000 chasebench/scenarios/deep/100/data > out.stream')
    print ('Example: python cbparse.py T 3 20 60 50 '\
            ' chasebench/scenarios/deep/100/dependencies > out.laser')
    print (' ')


def validate_dir(dir_path):
    if not dir_path.endswith("/"): 
        return "%s/" % dir_path
    return dir_path


class Fact:
    def __init__(self, predicate, values):
        self._predicate = predicate 
        self._values = values 

    def __str__(self):
        var = ' '.join(self._values)
        return "%s %s" % (self._predicate, var)
 

def parse_fact_csv(filename, dir_path):
    # each file is a fact: <predicate>.csv
    result = []
    predicate = filename.replace(".csv","")
    predicate = predicate.replace('_','')
    full_path = "%s%s" % (dir_path, filename)
    with open(full_path) as openfileobject:
        for line in openfileobject:
            line = line.rstrip()
            if line:    
                line = line.replace('_','').replace('"','')
                values = line.split(',')
                # Eliminating tailing new line. Removing "" around string vlaues.
                fact = Fact(predicate, values)
                result.append(fact)
    return result 


def print_source(timeline_size, source_instance):
    # on the first line, Star expects the first and last timepoint
    print("%d %d" % (1, timeline_size))
    for time_point in range(timeline_size):
        for fact in source_instance:
            # one fact per line; each line contains values separated by space
            # first value is the predicate followed by constants
            print(fact)
        # empty line marks the end of imput for the current time point
        print("")  


def parse_source(timeline_size, dir_path):
    source_instance = []
    for filename in os.listdir(dir_path):
        if filename.endswith(".csv"): 
            fact_list = parse_fact_csv(filename, dir_path)
            source_instance.extend(fact_list)
    return source_instance


class Dependency:
    def __init__(self, line):
        self._parse_line(line)
        self._existential_variables = self._get_existential_variables()
        self.is_existential = len(self._existential_variables) > 0
        self._events = []


    def __str__(self):
        head_atoms = self._head[:]
        for event in self._events:
            event_atom = "[I, %s]" % (event) 
            head_atoms.append(event_atom)
        head = ' && '.join(head_atoms)
        body = ' && '.join(self._body) 
        rule = head + ' := ' + body
        return rule


    def _parse_line(self, line):
        line = line.replace('.','').replace('?','').replace(' ','').replace('_','')
        line_list = line.split('->') 
        body = line_list[0]
        head = line_list[1]
        self._body = self._parse_conjunction(body) 
        self._head = self._parse_conjunction(head) 


    def _parse_conjunction(self, conjunction):
        '''
        parse atoms (starts with alphanumeric, ends with ')')
        '''
        result = []
        atom_chars = []
        prev_char = ""
        for char in conjunction:
            if char == ',' and prev_char == ')':
                atom = ''.join(atom_chars) 
                atom_chars = []
                result.append(atom)
            else:
                atom_chars.append(char)
            prev_char = char
        if atom_chars:
            atom = ''.join(atom_chars) 
            result.append(atom)
        return result

    
    def _get_variable_list(self, atom):
        atom = atom.replace(')', '')
        variables = atom.split('(')[1]
        var_list = variables.split(',')
        return var_list


    def _get_existential_variables(self):
        body_variables = set()
        head_variables = set()
        for atom in self._body:
            variables = self._get_variable_list(atom)
            body_variables.update(variables)
        for atom in self._head:
            variables = self._get_variable_list(atom)
            head_variables.update(variables)
        existential_variables = head_variables.difference(body_variables)
        return list(existential_variables)


    def add_operator(self, operator, window_size):
        new_body = []
        for atom in self._body:
            new_atom = "[$, %d] [%s] %s" % (window_size, operator, atom)
            new_body.append(new_atom)
        self._body = new_body

    def add_event(self):
        if self.is_existential:
            self._events.append(self._existential_variables[0])

    def add_all_events(self):
        if self.is_existential:
            self._events = self._existential_variables[:]


class DependencyParser:
    def __init__(self, window_size, percent_box, percent_diamond, \
            percent_event, dir_path):
        self._window_size = window_size
        self._percent_box = percent_box
        self._percent_diamond = percent_diamond
        self._percent_event = percent_event
        self._dir_path = dir_path 
        self._st_dependencies = []
        self._t_dependencies = []

    def _parse_dependecy_file(self, file_name):
        dependencies = []
        full_path = "%s%s" % (self._dir_path, file_name)
        with open(full_path) as openfileobject:
            for line in openfileobject:
                line = line.rstrip()
                if line:    
                    dependency = Dependency(line)
                    dependencies.append(dependency)
        return dependencies
    

    def _parse_tgds(self):
        for file_name in os.listdir(self._dir_path):
            if file_name.endswith(".st-tgds.txt"): 
                new_deps = self._parse_dependecy_file(file_name)
                self._st_dependencies.extend(new_deps)
            if file_name.endswith(".t-tgds.txt"): 
                new_deps = self._parse_dependecy_file(file_name)
                self._t_dependencies.extend(new_deps)



    def _count_existential_tgds(self, dependencies):
        result = 0  
        for dependency in dependencies:
            if dependency.is_existential:
                result += 1
        return result 
    

    def _add_windows(self, dependencies):
        number_tgds = len(dependencies)
        number_box = (number_tgds * self._percent_box) / 100
        number_diamond = (number_tgds * self._percent_diamond) / 100
        for dependency in dependencies:
            if number_box > 0:
                dependency.add_operator(OPERATOR_BOX, self._window_size)
                number_box -= 1
            elif number_diamond > 0:
                dependency.add_operator(OPERATOR_DIAMOND, self._window_size)
                number_diamond -= 1


    def _add_events(self, dependencies):
        if self._percent_event == 50:
            counter = 0
            for dependency in dependencies:
                counter += 1
                if counter % 2 == 0 and dependency.is_existential:
                    dependency.add_all_events()
        else:
            number_existential_tgds = self._count_existential_tgds(dependencies)
            number_event = (number_existential_tgds * self._percent_event) / 100
            for dependency in dependencies:
                if number_event > 0 and dependency.is_existential:
                    # dependency.add_event()
                    dependency.add_all_events()
                    number_event -= 1


    def _mutate_list(self, dependencies):
        self._add_windows(dependencies)
        self._add_events(dependencies)


    def read(self):
        self._parse_tgds()


    def mutate(self):
        self._mutate_list(self._st_dependencies)
        self._mutate_list(self._t_dependencies)


    def write(self):
        for dependency in self._st_dependencies:
            print(dependency)
        for dependency in self._t_dependencies:
            print(dependency)


def validate_percentages(percent_box, percent_diamond, percent_event):
    if percent_box > 100 or percent_diamond > 100 or percent_event > 100:
        print("Percentages should not be larger than 100")
        return False
    if percent_box + percent_diamond > 100:
        print("Percentages for box and diamond should not add up to more "\
                "than 100")
        return False
    return True


def main():
    if (len(sys.argv) < 2):
        print_help()
    else:
        option = sys.argv[1]
        if option == 'S':
            if (len(sys.argv) == 4):
                timeline_size = int(sys.argv[2])
                dir_path = validate_dir(sys.argv[3])
                source_instance = parse_source(timeline_size, dir_path)
                print_source(timeline_size, source_instance)
        elif option == 'T': 
            if (len(sys.argv) == 7):
                window_size = int(sys.argv[2])
                percent_box = int(sys.argv[3])
                percent_diamond = int(sys.argv[4])
                percent_event = int(sys.argv[5])
                if validate_percentages(percent_box, percent_diamond, \
                        percent_event):
                    dir_path = validate_dir(sys.argv[6])
                    parser = DependencyParser(window_size, percent_box, \
                            percent_diamond,  percent_event, dir_path)
                    parser.read()
                    parser.mutate()
                    parser.write()
        else:
            print_help()


if __name__ == '__main__':
    main()
