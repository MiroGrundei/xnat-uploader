import glob
import os


logdir = 'E:/MeMoSLAP/data/logs_task_xnat'

subjects = [0, 1, 2, 3, 5, 6, 7, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 23, 24]    # subject number (in the 2000 range for Sham Arm)
sessions = [3, 4]      # session ID for XNAT [0, 1, 2, 3, 4]
runs = [1, 2, 3, 4]

# to do: 2021
for sub in subjects:
    subject_id = f'20{sub:02d}'             # only subject number e.g. 2000
    print(f'Processing {subject_id}...')

    for ses in sessions:
        n_task = ses-2  # task number in experiment is 1 or 2 for sessions 3 and 4

        for run in runs:
            logfile_name = f'{logdir}/sub-{subject_id}_ses-task/sub-{subject_id}_tDCS_TWMD_ses-{n_task:02d}_run-{run:02d}_*.tsv'
            # Find all matching .tsv files
            matching_files = glob.glob(logfile_name)
            if len(matching_files) != 1:
                raise ValueError(f'The number of matching files is not equal to 1. Found: {len(matching_files)}')
            else:
                filepath = matching_files[0]

            new_filename = f'sub-{subject_id}_ses-{ses}_task-DMTS_acq-{n_task}_run-{run}_beh.tsv'
            path_part, name_part = os.path.split(filepath)
            new_filepath = f'{path_part}/{new_filename}'
            # Rename the file
            os.rename(filepath, new_filepath)
            print(f'Renamed: {filepath} \n        -> {new_filepath}\n')