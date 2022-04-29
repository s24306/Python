import os
import argparse
import hashlib


def check_dir(directory):
    for root, dirs, files in os.walk(directory, topdown=True):
        for name in files:
            file_size = os.path.getsize(os.path.join(root, name))
            file_name = os.path.join(root, name)
            if specific_format is False:
                if file_size in files_dict:
                    files_dict[file_size].append(file_name)
                else:
                    files_dict[file_size] = [file_name]
            else:
                name, extension = os.path.splitext(file_name)
                if extension != '.' + specific_format:
                    continue
                else:
                    if file_size in files_dict:
                        files_dict[file_size].append(file_name)
                    else:
                        files_dict[file_size] = [file_name]


parser = argparse.ArgumentParser()
parser.add_argument('path', nargs='?', type=str, default=None)
args = parser.parse_args()
if args.path is None:
    print('Directory is not specified')
    exit()
root_dir = args.path
files_dict = {}
file_format = input('Enter file format: ')
if file_format == "":
    specific_format = False
else:
    specific_format = file_format
print('''Size sorting options:
1. Descending
2. Ascending''')

while True:
    sorting_option = input('Enter a sorting option: ')
    if (sorting_option != '1') and (sorting_option != '2'):
        print('Wrong option')
    else:
        break

check_dir(root_dir)
same_size = []
for key, value in files_dict.items():
    if len(files_dict[key]) > 1:
        same_size.append(key)
    else:
        continue

if sorting_option == '2':
    same_size = sorted(same_size, key=int)
elif sorting_option == '1':
    same_size = sorted(same_size, key=int, reverse=True)
print()
for i in same_size:
    print(str(i) + ' bytes')
    for value in files_dict[i]:
        print(value)
    print()

while True:
    check_dupes = input('Check for duplicates? ')
    if (check_dupes != 'yes') and (check_dupes != 'no'):
        print('Wrong option')
    elif check_dupes == 'no':
        exit()
    else:
        print()
        break

hash_dict = {}

for i in same_size:
    for value in files_dict[i]:
        file_hash = hashlib.md5(open(value, 'rb').read()).hexdigest()
        if file_hash in hash_dict:
            hash_dict[file_hash].append(value)
        else:
            hash_dict[file_hash] = [value]

same_hash = []
for key, value in hash_dict.items():
    if len(hash_dict[key]) > 1:
        same_hash.append(key)
    else:
        continue

counter = 1
printed_bytes = []
duplicate_files_dict = {}

for i in same_hash:
    file = hash_dict[i][0]
    for key, value in files_dict.items():
        if key in printed_bytes:
            pass
        else:
            for val2 in value:
                if val2 == file:
                    print()
                    print(str(key) + ' bytes')
                    printed_bytes.append(key)
    print('Hash: ' + str(i))
    for j in hash_dict[i]:
        print(f'{counter}. {j}')
        duplicate_files_dict[counter] = j
        counter += 1

while True:
    check_dupes = input('Delete files? ')
    if (check_dupes != 'yes') and (check_dupes != 'no'):
        print('Wrong option')
    elif check_dupes == 'no':
        exit()
    else:
        print()
        break

while True:
    try:
        files_to_del = list(map(int, input('Enter file numbers to delete: ').split()))
        if len(files_to_del) == 0:
            print('Wrong format')
            continue
        else:
            files_set = set(files_to_del)
            dict_set = set(duplicate_files_dict)
            if dict_set.intersection(files_set) != files_set:
                print('Wrong format')
            else:
                break
    except Exception:
        print('Wrong format')

freed_space = 0

for i in files_to_del:
    freed_space += os.path.getsize(duplicate_files_dict[i])
    os.remove(duplicate_files_dict[i])

print(f'Total freed up space: {freed_space} bytes')
