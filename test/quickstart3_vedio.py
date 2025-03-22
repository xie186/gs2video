import urllib.request
import json   

import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/presentations.readonly']
# The ID of a sample presentation.
PRESENTATION_ID = '1-aTBNXcSIqlMRzn-FHnRmRPbGlh5eY8MgZNaBwo15IM'
creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
   creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
   if creds and creds.expired and creds.refresh_token:
       creds.refresh(Request())
   else:
       flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
       creds = flow.run_local_server(port=0)
   # Save the credentials for the next run
   with open('token.json', 'w') as token:
       token.write(creds.to_json())

service = build('slides', 'v1', credentials=creds)

presentation = service.presentations().get(presentationId=PRESENTATION_ID).execute()
slides = presentation.get('slides')
print('The presentation contains {} slides:'.format(len(slides)))
## 
for i, slide in enumerate(slides):
    print('- Slide #{} contains {} elements.'.format(i + 1, len(slide.get('pageElements'))))
    text = slide['slideProperties']['notesPage']['pageElements'][1]['shape']['text']['textElements'][1]['textRun']['content']
    
    img_info = service.presentations().pages().getThumbnail(presentationId=PRESENTATION_ID, 
          pageObjectId=slide.get('objectId'), thumbnailProperties_thumbnailSize="LARGE").execute()
    urllib.request.urlretrieve(img_info["contentUrl"], "test"+str(i)+".png")





