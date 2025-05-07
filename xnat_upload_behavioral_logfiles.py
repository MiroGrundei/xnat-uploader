import import2xnat as impx
import glob


# upload behavioral logfile of task MRI session

xnat_session = impx.start_xnat_session()
project = '002'

# behavioral data is stored under 'beh'
resource_name = 'beh'

logdir = 'E:/MeMoSLAP/data/logs_task_xnat'

subjects = [0, 1, 2, 3, 5, 6, 7, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 23, 24]     # subject number (in the 2000 range for Sham Arm)
sessions = [3, 4]      # session ID for XNAT [0, 1, 2, 3, 4]
runs = [1, 2, 3, 4]

# to do: 2021
for sub in subjects:
    subject_id = f'20{sub:02d}'             # only subject number e.g. 2000
    print(f'Processing {subject_id}...')

    for ses in sessions:
        experiment_id = f'{subject_id}_{ses}'

        for run in runs:
            logfile_name = f'{logdir}/sub-{subject_id}_ses-task/sub-{subject_id}_ses-{ses}_task-DMTS_acq-{ses-2}_run-{run}_beh.tsv'
            # Find all matching .tsv files
            matching_files = glob.glob(logfile_name)
            if len(matching_files) != 1:
                raise ValueError(f'The number of matching files is not equal to 1. Found: {len(matching_files)}')
            else:
                filepath = matching_files[0]

            # upload to behavioral resources
            impx.upload_resource_files(xnat_session, project, subject_id, experiment_id, resource_name, filepath)