# XNAT Data Uploader

A small command-line utility for uploading imaging archives and related files
to [XNAT](https://www.xnat.org/). It supports:

- importing ZIP archives into the XNAT prearchive;
- uploading files to an experiment resource;
- uploading files to a project resource;
- checking an upload with `--dry-run` before connecting.

This repository grew out of scripts used to upload MRI, behavioral, protocol,
and questionnaire data for a research project. The command-line interface
keeps those workflows reusable without storing project IDs, local paths, or
credentials in source code.

## Installation

Python 3.9 or newer is recommended.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

On macOS or Linux, activate the environment with
`source .venv/bin/activate`.

## Connection settings

Set the server and user as environment variables:

```bash
set XNAT_SERVER=https://xnat.example.org
set XNAT_USER=my-user
```

Use `export` instead of `set` on macOS or Linux. The tool prompts for the
password, so it does not appear in shell history. Alternatively, set
`XNAT_PASSWORD` for unattended use.

Credentials and certificates should never be committed to the repository.

## Examples

Check an MRI import without connecting:

```bash
python xnat_upload.py --dry-run scan scans\sub-1001_ses-01.zip ^
  --project DEMO --subject 1001 --experiment 1001_01
```

Import the archive:

```bash
python xnat_upload.py scan scans\sub-1001_ses-01.zip ^
  --project DEMO --subject 1001 --experiment 1001_01
```

Upload a behavioral file to an experiment resource:

```bash
python xnat_upload.py resource data\sub-1001_task-test_beh.tsv ^
  --project DEMO --subject 1001 --experiment 1001_01 --resource beh
```

Upload a codebook to a project-level resource:

```bash
python xnat_upload.py project-resource data\data_dictionary.json ^
  --project DEMO --resource documentation
```

The examples use Windows Command Prompt line continuation (`^`). Commands can
also be entered on a single line.

## Notes

- Scan imports must be ZIP files.
- Existing prearchive sessions are skipped unless `--allow-existing` is used.
- Resource uploads use the local filename by default. Use `--remote-name` to
  choose another name on XNAT.
- `--insecure` disables TLS verification and should only be used for a known
  internal test server.

This utility uses the `xnat` Python package, not `pyxnat`. See the
[xnatpy documentation](https://xnat.readthedocs.io/) for package details.
The standard xnatpy connection does not currently expose a client-certificate
argument; servers that require mutual TLS need server-specific configuration.
