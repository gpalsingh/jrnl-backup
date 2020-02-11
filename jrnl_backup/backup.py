import os
import appdirs
import subprocess
import pickle
import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive']
userDataDirectory = appdirs.user_data_dir('jrnl_backup')
backupFileName = 'backup.txt'

def getFilePath(fileName):
  return os.path.join(userDataDirectory, fileName)

def getGdriveCredentialsLocation():
  return os.environ.get('GDRIVE_JRNLBACKUP_CREDENTIALS_JSON')

def getRemoteBackupFileName():
  return 'journal-encrypted-{}.txt'.format(time.strftime("%m/%d/%Y-%H:%M:%S"))

# Create encrypted backup file
def createBackup():
  print('Creating local backup')
  # Create backup folder if it doesn't exist
  if os.path.exists(userDataDirectory) == False:
    os.makedirs(userDataDirectory)
  backupCommand = 'jrnl --encrypt {}'.format(backupFileName)
  streamFile = getFilePath('backup.log')
  with open(streamFile, 'w+') as fakeStream:
    subprocess.Popen(
      backupCommand,
      cwd=userDataDirectory,
      stdout=fakeStream,
      stderr=fakeStream
    )
  print('Finished creating local backup')

# login into gdrive
def uploadBackup():
  print('Starting upload')
  creds = None
  # The file token.pickle stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  pickleFileName = 'token.pickle'
  pickleFilePath = getFilePath(pickleFileName)
  if os.path.exists(pickleFilePath):
    with open(pickleFilePath, 'rb') as token:
      creds = pickle.load(token)

  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      credentialsLocation = getGdriveCredentialsLocation()
      flow = InstalledAppFlow.from_client_secrets_file(
        credentialsLocation, SCOPES)
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(pickleFilePath, 'wb') as token:
      pickle.dump(creds, token)
  else:
    print("Using saved credentials")

  service = build('drive', 'v3', credentials=creds)

  # Check if the backup folder exists on drive
  folderName = 'jrnl_backup'
  results = service.files().list(
      q="mimeType='application/vnd.google-apps.folder' and name='{}'".format(folderName)
    ).execute()
  items = results.get('files', [])

  if not items:
    print('Backup folder not found on drive. Attempting to create one')
    file_metadata = {
      'name': folderName,
      'mimeType': 'application/vnd.google-apps.folder'
    }
    item = service.files().create(body=file_metadata).execute()
    items = [item]

  # Upload the file to drive
  folderInfo = items[0]
  folder_id = folderInfo['id']
  file_metadata = {
      'name': getRemoteBackupFileName(),
      'parents': [folder_id]
  }

  media = MediaFileUpload(getFilePath(backupFileName),
                        mimetype='text/plain',
                        resumable=True)
  file = service.files().create(body=file_metadata,
                              media_body=media).execute()
  print('Uploaded file: {}'.format(file['name']))

def main():
  # Get backup folder location
  createBackup()
  uploadBackup()

if __name__ == "__main__":
  main()