import import2xnat as impx
import glob


# upload tes questionnaires of each session

xnat_session = impx.start_xnat_session()
project = '002'

# PANAS, TES, Strategy/Focus data is stored under 'phenotype'
resource_name = 'Neuropsych'

quests = ['bdi_II', 'digit_span', 'dmeq', 'handedness', 'lueden_activity', 'mwt', 'quest', 'raven', 'rey_figure', 'rwt',
          'stroop', 'tmt', 'vlmt']

for quest in quests:
    file_name = f'E:/MeMoSLAP/data/assessments/Neuropsych/{quest}'

    # Find all matching .tsv files
    matching_files = glob.glob(f'{file_name}_p{int(project)}.tsv')

    if len(matching_files) != 1:
        raise ValueError(f'The number of matching files is not equal to 1. Found: {len(matching_files)}')
    else:
        filepath = matching_files[0]

    # upload to phenotype resources: .tsv
    impx.upload_resource_to_main(xnat_session, project, resource_name, f'{filepath[:-4]}.tsv')
    # upload to phenotype resources: .json
    impx.upload_resource_to_main(xnat_session, project, resource_name, f'{filepath[:-4]}.json')