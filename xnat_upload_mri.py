import import2xnat as impx


### Upload MRI data

xnat_session = impx.start_xnat_session()

project = '002'                # project ID, 3digits e.g. 002, 008 ...
data_base_path = '//campus.fu-berlin.de/daten/ERZWISS/CCNB-MRT/DICOM/MeMoSLAP_P2'   # path to data storage (e.g. CCNB)

# Needed:
# 22: base
subjects = [22]     # subject number (in the 2000 range for Sham Arm)
sessions = [0]      # session ID for XNAT [0, 1, 2, 3, 4]
data_sessions = ['base', 'rest1', 'rest2', 'task1', 'task2']    # session ID as stored at CCNB

for sub in subjects:
    subject_id = f'20{sub:02d}'             # only subject number e.g. 2000

    for ses in sessions:
        # MRI Session (Note: sub-2001_ses-base = 2001_base, sub-2001_ses-task2 = 2001_4)
        if ses == 0:
            experiment_id = f'{subject_id}_base'
        else:
            experiment_id = f'{subject_id}_{ses}'
        # subject ID as stored at CCNB, e.g. sub-2011, sub-2000, ...
        data_subID = f'sub-{subject_id}'
        # session ID as stored at CCNB, e.g. rest1, rest2, task1, task2
        data_sesID = data_sessions[ses]
        # Full data path to DICOM Session
        data = f'{data_base_path}/{data_subID}/{data_subID}_ses-{data_sesID}'

        result = impx.check_zipfile(data)
        if result == "not_zip":
            # make zipfile if not zipped (which it is on the CCNB Dicom server
            # shutil.make_archive(experiment_id, 'zip', data)
        elif result == "no_file":
            raise FileExistsError(f'File {data} does not exist!')

        # upload to prearchive
        impx.upload_to_prearchive(xnat_session, project, subject_id, experiment_id, data + '.zip')

