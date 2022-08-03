import csv

all_common_names_dict = {}
with open('data/common_names.csv') as f:
    next(f)  # Skip the header
    reader = csv.reader(f, skipinitialspace=True)
    all_common_names_dict = dict(reader)

ebirdcodes = open("data/ebirdcodes.csv",'r').read().splitlines()

filtered_dict = {ebird_code:common_name for (ebird_code, common_name) in all_common_names_dict.items() if ebird_code in ebirdcodes}
print(filtered_dict)
#
# filtered_list = dict(ChainMap(*filtered_list))
#
# print(filtered_list)
#
# header = filtered_list[0].keys()
# with open('data/filtered_common_names.csv', 'w') as file:
#     csv_writer = csv.DictWriter(file, header)
#     csv_writer.writeheader()
#     csv_writer.writerows(filtered_list)

