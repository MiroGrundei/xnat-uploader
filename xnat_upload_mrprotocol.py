import import2xnat as impx
import glob


# upload MR protocol of each session

xnat_session = impx.start_xnat_session()
project = '002'

# MR protocol data is stored under 'MRprotocol'
resource_name = 'MRprotocol'

data_dir = 'E:/MeMoSLAP/data/MRprotocols/'

subjects = [0, 1, 2, 3, 5, 6, 7, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 23, 24]     # subject number (in the 2000 range for Sham Arm)
sessions = [0, 1, 2, 3, 4]      # session ID for XNAT [0, 1, 2, 3, 4]

for sub in subjects:
    subject_id = f'20{sub:02d}'             # only subject number e.g. 2000

    for ses in sessions:
        # MRI Session (Note: sub-2001_ses-base = 2001_base, sub-2001_ses-task2 = 2001_4)
        if ses == 0:
            experiment_id = f'{subject_id}_base'
            file_name = f'{data_dir}/sub-{subject_id}/sub-{subject_id}_ses-base_MRprotocol'
        else:
            experiment_id = f'{subject_id}_{ses}'
            file_name = f'{data_dir}/sub-{subject_id}/sub-{subject_id}_ses-{ses}_MRprotocol'

        # Find all matching .tsv files
        matching_files = glob.glob(file_name + '.pdf')
        if len(matching_files) != 1:
            raise ValueError(f'The number of matching files is not equal to 1. Found: {len(matching_files)}')
        else:
            filepath = matching_files[0]

        # upload to MRprotocol resources
        impx.upload_resource_files(xnat_session, project, subject_id, experiment_id, resource_name, filepath)