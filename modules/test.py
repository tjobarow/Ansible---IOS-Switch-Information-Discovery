import csv, json

def parseCSV(path: str):
    inventory_dict = {}
    with open(path,'r') as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=',')
        line_index = 0
        for row in csv_reader:
            if line_index == 0:
                line_index = line_index + 1
                continue
            host_entry = {
                'host_ip':row[0],
                'ansible_user':row[1],
                'ansible_password':row[2],
                'ansible_become_password':row[3]
            }
            print(host_entry)
            if row[4] in inventory_dict:
                inventory_dict[row[4]].append(host_entry.copy())
            else:
                inventory_dict.update({row[4]:[]})
                inventory_dict[row[4]].append(host_entry.copy())
    return inventory_dict

if __name__ == "__main__":
    path = '/Users/tobarows/Coding_Projects/Ansible/ansible-ios-switch-information-discovery/modules/inventory.csv'
    print(json.dumps(parseCSV(path),indent=4))
