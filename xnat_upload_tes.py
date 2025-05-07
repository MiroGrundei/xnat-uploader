import import2xnat as impx
import glob


# upload tes questionnaires of each session

xnat_session = impx.start_xnat_session()
project = '002'

# PANAS, TES, Strategy/Focus data is stored under 'phenotype'
resource_name = 'phenotype'

quest = 'TES'
quest_dir = 'E:/MeMoSLAP/data/assessments/' + quest

subjects = [0, 1, 2, 3, 5, 6, 7, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 23, 24]    # subject number (in the 2000 range for Sham Arm)
sessions = [1, 2, 3, 4]     # session ID for XNAT [0, 1, 2, 3, 4]

for sub in subjects:
    subject_id = f'20{sub:02d}'             # only subject number e.g. 2000
    print(f'Processing {subject_id}...')

    for ses in sessions:
        experiment_id = f'{subject_id}_{ses}'

        file_name = f'{quest_dir}/sub-{subject_id}_ses-{ses}_{quest.lower()}'
        # Find all matching .tsv files
        matching_files = glob.glob(file_name + '.tsv')
        if len(matching_files) != 1:
            raise ValueError(f'The number of matching files is not equal to 1. Found: {len(matching_files)}')
        else:
            filepath = matching_files[0]

        # upload to phenotype resources: .tsv
        impx.upload_resource_files(xnat_session, project, subject_id, experiment_id, resource_name, f'{filepath[:-4]}.tsv')
        # upload to phenotype resources: .json
        impx.upload_resource_files(xnat_session, project, subject_id, experiment_id, resource_name, f'{filepath[:-4]}.json')