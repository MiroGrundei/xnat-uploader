import xnat
import os
import zipfile
import time


def start_xnat_session():
    # Start XNAT session
    user = ''  # XNAT user
    password = ''  # XNAT password
    pem_certificate = 'C:/Users/nnu04/Documents/MeMoSLAP/XNAT/GRUNDEI.pem'  # Certificate in .pem format
    xnat_session = xnat.connect('https://neuro.med.uni-greifswald.de/xnat', user=user, password=password, cert=pem_certificate)
    return xnat_session


def end_xnat_session(xnat_session):
    print('Ending session.')
    print("Sleep.....")
    time.sleep(50)
    print("Disconnect.....")
    xnat_session.disconnect()
    print("Ended.")


def upload_to_prearchive(xnat_session, project, subject_id, experiment_id, data_path):

    print(f'Upload file: {data_path}')

    rtn = xnat_session.prearchive.find(project, subject_id, experiment_id)
    print(f'Feedback from pre-archive: {rtn}')

    if rtn:
        print('Session already uploaded!')
    else:
        print(f'Starting upload as {experiment_id}')
        try:
            response = xnat_session.services.import_(data_path, project=project, subject=subject_id, experiment=experiment_id)
        except Exception as e:
            error_message = str(e)
            if "504 Gateway Time-out" in error_message:
                print('Gateway time-out (expected)')
                pass
            else:
                print(f'An unexpected error occurred: {e}')


def check_zipfile(filepath):
    # Check if the file exists
    if os.path.exists(filepath):
        # File exists, now check if it is a ZIP file
        if zipfile.is_zipfile(filepath):
            return "valid_zip"
        else:
            return "not_zip"
    else:
        return "no_file"


def upload_resource_files(xnat_session, project, subject_id, experiment_id, resource_name, filepath, filename_xnat=None):

    # access the project experiment
    experiment = xnat_session.projects[project].subjects[subject_id].experiments[experiment_id]

    # access resources
    resource_list = experiment.resources

    # check if the resource exists
    if resource_name not in resource_list:
        print(f'Resource "{resource_name}" does not exist in {subject_id}. Will be created.')
        # create
        xnat_session.classes.ResourceCatalog(parent=experiment, label=resource_name)

    # If filename_xnat is not provided, use the same path as filepath
    if filename_xnat is None:
        filename_xnat = filepath

    file_path_temp, file_name = os.path.split(filename_xnat)
    experiment.resources[resource_name].upload(path=filepath, remotepath=file_name)

    print(f'Uploaded {filepath} as {file_name} to {resource_name} of project {project} | subject {subject_id} | session {experiment_id}.')



def upload_resource_to_main(xnat_session, project, resource_name, filepath):

    # access the project
    experiment = xnat_session.projects[project]

    # access resources
    resource_list = experiment.resources

    # check if the resource exists
    if resource_name not in resource_list:
        print(f'Resource "{resource_name}" does not exist. Will be created.')
        # create
        xnat_session.classes.ResourceCatalog(parent=experiment, label=resource_name)

    file_path, file_name = os.path.split(filepath)
    experiment.resources[resource_name].upload(path=filepath, remotepath=file_name)

    print(f'Uploaded {filepath} to {resource_name} of project {project}.')
