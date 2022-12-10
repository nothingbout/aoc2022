with open('input.txt', 'r') as file:
    lines = [line.rstrip('\r\n') for line in file.readlines()]

class File:
    def __init__(self, size, name):
        self.size = size
        self.name = name
    
    def __str__(self):
        return f'File: size = {self.size}, name = {self.name}'

class Dir:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.files = []
        self.subdirs = []

    def __str__(self):
        return f'Dir: name = {self.name}, parent = {self.parent.name if self.parent else "none"}, files: {len(self.files)}, subdirs: {len(self.subdirs)}'

    def add_subdir(self, name):
        subdir = Dir(name, self)
        self.subdirs.append(subdir)
        return subdir

    def add_file(self, file):
        self.files.append(file)
    
    def get_subdir(self, name, create_if_necessary):
        subdir = next(filter(lambda x: x.name == name, self.subdirs))
        if not subdir:
            if create_if_necessary:
                subdir = self.add_subdir(name)
        return subdir

    def get_all_subdirs_recursive(self):
        subdirs = [self]
        for subdir in self.subdirs:
            subdirs.extend(subdir.get_all_subdirs_recursive())
        return subdirs

    def get_files_size(self):
        return sum(map(lambda x: x.size, self.files))

    def get_total_size(self):
        subdirs = self.get_all_subdirs_recursive()
        return sum(map(lambda x: x.get_files_size(), subdirs))

root_dir = Dir('/', None)
current_dir = None

for line in lines:
    parts = line.split()
    if parts[0] == '$':
        cmd = parts[1]
        if cmd == 'cd':
            cd_dir = parts[2]
            if cd_dir == '/':
                current_dir = root_dir
            elif cd_dir == '..':
                current_dir = current_dir.parent
            else:
                current_dir = current_dir.get_subdir(cd_dir, False)
        elif cmd == 'ls':
            continue
    elif parts[0] == 'dir':
        current_dir.add_subdir(parts[1])
    else:
        size = int(parts[0])
        name = parts[1]
        current_dir.add_file(File(size, name))

all_dirs = root_dir.get_all_subdirs_recursive()

# for dir in all_dirs:
#     print(dir)
#     for file in dir.files:
#         print(file)

all_dir_sizes = list(map(lambda x: x.get_total_size(), all_dirs))
# print(all_dir_sizes)

root_total_size = all_dir_sizes[0]
free_space = 70000000 - root_total_size
required_space = 30000000

for size in sorted(all_dir_sizes):
    if size >= required_space - free_space:
        print(size)
        break
