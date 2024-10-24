import os
import shutil

# Step 1: Path choosen for the explorer (decided by user).

source_path=input("Enter the source folder path: ")
target_path=input("Enter the target folder path: ")

# Step 2: Get infos on all files in source folder.

counter = 0 

file_info_list_source = [] # empty list
for root, dirs, files in os.walk(source_path):
  for filename in files:
    counter += 1
    if counter % 1000 == 0:
      print(f"Processed {counter} source files")
    filepath = os.path.join(root, filename)
    filesize = os.path.getsize(filepath)
    file_info_list_source.append({
        "name": filename,
        "path": root,
        "size": filesize
    })

# Step 3: Get infos on all files in target folder.

counter = 0

file_info_list_target = [] # empty list
for root, dirs, files in os.walk(target_path):
  for filename in files:
    counter += 1
    if counter % 1000 == 0:
      print(f"Processed {counter} target files")
    filepath = os.path.join(root, filename)
    filesize = os.path.getsize(filepath)
    file_info_list_target.append({
        "name": filename,
        "path": root,
        "size": filesize
    })


# Step 4: Get difference between those two lists

source_subset = [{"name": info["name"], "size": info["size"]} for info in file_info_list_source]
target_subset = [{"name": info["name"], "size": info["size"]} for info in  file_info_list_target]

difference = set([tuple(item.values()) for item in source_subset]).difference(set([tuple(item.values()) for item in target_subset]))

print(difference)

difference_list_1 = []
for item in difference:
  matching_source_dict = [info for info in file_info_list_source if info["name"] == item[0] and info["size"] == item[1]][0]
  difference_list_1.append(matching_source_dict.copy()) 

print(len(difference_list_1))


# Step 5: Add difference to target path.

for i in range(len(difference_list_1)):
  
  #set ups
  name=difference_list_1[i]["name"]
  path=difference_list_1[i]["path"]
  print("Path is:")
  print(path)
  copy_source_path=os.path.join(path,name)
  print(copy_source_path)
  #building target path
  drive, sep, remaining = path.partition(':')
  target_path_new = os.path.join(os.path.join(target_path,"copy"),os.path.join(sep, remaining))
  print("new path")
  print(target_path_new)
  target=os.path.join(target_path_new, name)
  os.makedirs(target_path_new,exist_ok=True)
  shutil.copyfile(copy_source_path, target)

