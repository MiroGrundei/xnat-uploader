import os

# Define the root directory where you want to start the renaming process
root_dir = 'E:/MeMoSLAP/data/MRprotocols'

# The part of the filename to find and replace everything after
search_terms = ['base', 'rest1', 'rest2', 'task1', 'task2']

# The new part of the filename to replace the found part with
new_suffixes = ['base_MRprotocol.pdf', '1_MRprotocol.pdf', '2_MRprotocol.pdf', '3_MRprotocol.pdf', '4_MRprotocol.pdf']

# Loop through all directories and subdirectories
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        # Check if the search term exists in the filename
        for term in search_terms:
            if term in filename:
                # Find the position where the search term starts
                part_index = filename.find(term)

                # Create the new filename by keeping the part before the search term and adding the new suffix
                new_filename = filename[:part_index] + new_suffixes[search_terms.index(term)]

                # Full file paths
                old_file_path = os.path.join(dirpath, filename)
                new_file_path = os.path.join(dirpath, new_filename)

                # Rename the file
                os.rename(old_file_path, new_file_path)
                print(f'Renamed: {old_file_path} \n     -> {new_file_path}')