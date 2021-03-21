#!/usr/bin/env python
#-*-- coding: utf-8 -*-
import argparse
import urllib.request
import json
import logging

import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from gtts import gTTS
from moviepy.editor import *

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/presentations.readonly']

def credential():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
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
    return creds

def rmtem(temlist):
    for f in temlist:
        logging.info(f)
        if os.path.isfile(f): # this makes the code more robust
            os.remove(f)

def to_video(tem_service, options):
    present_id = options.presentation_id
    output = options.output
    tem_files = []
    clip_list = []
    presentation = tem_service.presentations().get(presentationId=present_id).execute()
    slides = presentation.get('slides')
    print('The presentation contains {} slides:'.format(len(slides)))
    for i, slide in enumerate(slides):
        logging.info('- Slide #{} contains {} elements.'.format(i + 1, len(slide.get('pageElements')))) 
        text = slide['slideProperties']['notesPage']['pageElements'][1]['shape']['text']['textElements'][1]['textRun']['content']
        tem_audio = output + "."+str(i)+".mp3"
        v =gTTS(text=text, lang=options.language, slow=False) 
        v.save(tem_audio) 
        tem_audiocontent = AudioFileClip(tem_audio)
        tem_files.append(tem_audio)
        
        img_info = service.presentations().pages().getThumbnail(presentationId=present_id,
            pageObjectId=slide.get('objectId'), thumbnailProperties_thumbnailSize="LARGE").execute()
        tem_png = output + "."+str(i)+".png"
        urllib.request.urlretrieve(img_info["contentUrl"], tem_png)
        tem_files.append(tem_png)
        # Import the audio(Insert to location of your audio instead of audioClip.mp3)
        # Import the Image and set its duration same as the audio (Insert the location of your photo instead of photo.jpg)
        clip = ImageClip(tem_png).set_duration(tem_audiocontent.duration)
        # Set the audio of the clip
        clip = clip.set_audio(tem_audiocontent)
        clip_list.append(clip)
    concat_clip = concatenate_videoclips(clip_list, method="compose")
    logging.info("Write video file: ") 
    concat_clip.write_videofile(output, fps=options.fps)
    if(not options.keep):
        rmtem(tem_files)
        
if __name__ == '__main__':
    ## description - Text to display before the argument help (default: none)
    parser = argparse.ArgumentParser(description='Slide to vedio') #add_help=False)                             
    parser.add_argument('-p', '--presentation_id', \
                      # metavar - A name for the argument in usage messages.
                      help='Presentation_ID', required=True)
    parser.add_argument('-f', '--fps', metavar = "fps", type=int, \
                      help='Frames per second (FPS)', required=False, default = 24)
    parser.add_argument('-l', '--language', type=str, \
                      help='Language in the note', required=False, default = 'en')
    parser.add_argument('--keep', action='store_true', help = "Keep intermediate files (mp3 and png files)")
    parser.add_argument('-o', '--output', help='output file', default = "Output_file.mp4") 
    
    options = parser.parse_args()
    dict_cmd = vars(options) 
    # The ID of a sample presentation. PRESENTATION_ID = '1-aTBNXcSIqlMRzn-FHnRmRPbGlh5eY8MgZNaBwo15IM'
    creds = credential()
    service = build('slides', 'v1', credentials=creds) 
    to_video(service, options)
    
