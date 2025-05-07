# How To use XNAT python package
https://xnat.readthedocs.io/en/latest/

(not to be confused with pyxnat)

### Preparatory steps (by Robert Malinowski):
You need to modify __init__.py from XNAT Package to to use your client-cert for the connectiont to the xnat server!

1) modify __init__.py
   - stored: ~\AppData\Roaming\Python\Python39\site-packages\xnat
   - modify:
     `def connect(server=None, user=None, password=None, verify=True, crt=None, netrc_file=None, debug=False,
            extension_types=True, loglevel=None, logger=None, detect_redirect=True,
            no_parse_model=False, default_timeout=300, auth_provider=None, jsession=None,
            cli=False)`
     
   Here I included a new Parameter "crt=None"  
   - add in Line 533 (addition by Miro: for me it was later around line 560):
          ` if crt is not None:
               requests_session.cert = crt `

    This is for https request can handle the client cert session

3) Convert your *.p12 file + Passwort to a *.pem file   -> see provided function `pfx2pem.py` (Miro edit)
4) put the pem file a cert param into the xnat.connect() function


# Notes on naming convention 
### MeMoSLAP specific (based on BIDS)

1) Behavioral Logfiles
   - store on XNAT in session 3 & 4 of each subject (session 3 = acq 1; session 4 = acq 2)
   - folder 'beh'
   - sub-2000_ses-3_task-DMTS_acq-1_run-1_beh.tsv
   - sub-2000_ses-3_task-DMTS_acq-1_run-2_beh.tsv
   - sub-2000_ses-3_task-DMTS_acq-1_run-3_beh.tsv
   - sub-2000_ses-3_task-DMTS_acq-1_run-4_beh.tsv
   - sub-2000_ses-4_task-DMTS_acq-2_run-1_beh.tsv
   - sub-2000_ses-4_task-DMTS_acq-2_run-2_beh.tsv
   - sub-2000_ses-4_task-DMTS_acq-2_run-3_beh.tsv
   - sub-2000_ses-4_task-DMTS_acq-2_run-4_beh.tsv
3) MRprotocols
   - store on XNAT in each session (base, 1, 2, 3, 4) of each subject
   - folder 'MRprotocols'
   - sub-2000_ses-base_MRprotocol.pdf
   - sub-2000_ses-1_MRprotocol.pdf
   - sub-2000_ses-2_MRprotocol.pdf
   - sub-2000_ses-3_MRprotocol.pdf
   - sub-2000_ses-4_MRprotocol.pdf
4) PANAS & TES
   - store on XNAT in each tDCS session (1, 2, 3, 4) of each subject
   - folder 'phenotype'
   - sub-2000_ses-X_panas.tsv
   - sub-2000_ses-X_tes.tsv





