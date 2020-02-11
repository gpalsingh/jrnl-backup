# jrnl-backup

A python script to backup your jrnl.sh journals

## Setting up Google Drive credentials
This script uses [Google Drive API v3](https://developers.google.com/drive/api/v3/reference).
Check the [Quickstart Tutorial](https://developers.google.com/drive/api/v3/quickstart/go#step_1_turn_on_the) to create the credentials JSON file.
Set the environment `GDRIVE_JRNLBACKUP_CREDENTIALS_JSON` to the absolute path of the credentials file on the system
**Note:** You will be asked to authenticate the app on the first run

## Usage
```console
$ jrnl-backup
```
or
```console
$ jrnlbackup
```