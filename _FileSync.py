# Import the libraries (os and shutil)

import os
import shutil

# Make the lists of all the files in folder1 and folder2


def get_file_info(folder):
  file_info = []
  counter = 0
  for root, _, files in os.walk(folder):
    for file in files:
      counter += 1
      if counter % 100 == 0:
        print("scanned: " + str(counter))
      # Check for hidden files (indented under the loop)
      file_path = os.path.join(root, file)

      # Handle potential errors during file size retrieval
      try:
          file_size = os.path.getsize(file_path)
          if file_size > 0:  # Only process non-empty files (0kb)
              file_info.append((file, root, file_size))
      except FileNotFoundError:
          # Handle potential file not found errors (like $RECYCLE.BIN)
          pass  # Ignore the error and continue processing other files

  return file_info


# Copy the files after keeping all unique files.

def copy_unique_files(folder1, folder2):
    folder1_info = get_file_info(folder1)
    folder2_info = get_file_info(folder2)

    sublist1 = [
        (file, root, size) for file, root, size in folder1_info
        if (file, root, size) not in folder2_info
    ]

    print(sublist1)
  
    sublist2 = [
        (file, root, size) for file, root, size in folder2_info
        if (file, root, size) not in folder1_info
    ]

    print(sublist2)
  
    for file, root, _ in sublist1:
        source_path = os.path.join(root, file)
        dest_path = os.path.join(folder2, "transfer", os.path.relpath(source_path, folder1))
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)  # Create intermediate directories
        shutil.copy2(source_path, dest_path)  # Copy file with metadata
        print(dest_path)

    for file, root, _ in sublist2:
        source_path = os.path.join(root, file)
        dest_path = os.path.join(folder1, "transfer", os.path.relpath(source_path, folder2))
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)  # Create intermediate directories
        shutil.copy2(source_path, dest_path)
        print(dest_path)# Copy file with metadata

folder1 = input("Enter the first folder: ")
folder2 = input("Enter the second folder: ")

copy_unique_files(folder1, folder2)