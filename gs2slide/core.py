import os
import sys
import hashlib
import logging
import urllib.request
from googleapiclient.discovery import build
from gtts import gTTS
from moviepy import *
import logging

logging.basicConfig(level=logging.INFO)

class GS2Video:
    def __init__(self, credentials, output, language='en', fps=24, keep=False, force=False):
        self.credentials = credentials
        self.output = os.path.abspath(output)
        self.language = language
        self.fps = fps
        self.keep = keep
        self.force = force
        self.tem_files = []
        self.clip_list = []
        self.service = build('slides', 'v1', credentials=self.credentials)
        # Ensure the cache directory exists
        if not os.path.exists('cache'):
            os.makedirs('cache')
            
    def generate_hash(self, content):
        if isinstance(content, str):
            content = content.encode('utf-8')
        return hashlib.md5(content).hexdigest()
    
    def rmtem(self):
        for f in self.tem_files:
            logging.info(f)
            if os.path.isfile(f):
                os.remove(f)
    
    def to_video(self, presentation_id):
        if os.path.isfile(self.output) and not self.force:
            logging.info("Output video file already exists: " + self.output)
            return
        
        presentation = self.service.presentations().get(presentationId=presentation_id).execute()
        slides = presentation.get('slides')
        print('The presentation contains {} slides:'.format(len(slides)))
        video_hash = hashlib.md5()
        for i, slide in enumerate(slides):
            logging.info('- Slide #{} contains {} elements.'.format(i + 1, len(slide.get('pageElements')))) 
            text = slide['slideProperties']['notesPage']['pageElements'][1]['shape']['text']['textElements'][1]['textRun']['content']
            text_hash = self.generate_hash(text)
            video_hash.update(text_hash.encode('utf-8'))
            tem_audio = f"cache/{text_hash}.mp3"
            
            if not os.path.isfile(tem_audio):
                v = gTTS(text=text, lang=self.language, slow=False) 
                v.save(tem_audio) 
            tem_audiocontent = AudioFileClip(tem_audio)
            print(tem_audiocontent)
            self.tem_files.append(tem_audio)
            
            img_info = self.service.presentations().pages().getThumbnail(
                presentationId=presentation_id,
                pageObjectId=slide.get('objectId'), 
                thumbnailProperties_thumbnailSize="LARGE"
                ).execute()
            img_url = img_info["contentUrl"]
            
            with urllib.request.urlopen(img_url) as response:
                img_content = response.read()
            img_hash = self.generate_hash(img_content)
            video_hash.update(img_hash.encode('utf-8'))
            tem_png = f"cache/{img_hash}.png"
            if i == 0:
                print(img_hash)
            
            if not os.path.isfile(tem_png):
                with open(tem_png, 'wb') as f:
                    f.write(img_content)
            self.tem_files.append(tem_png)
            
            print(tem_audiocontent.duration)
            clip = ImageClip(tem_png).with_duration(tem_audiocontent.duration).with_audio(tem_audiocontent)
            self.clip_list.append(clip)
        
        video_hash = video_hash.hexdigest()
        video_file = os.path.join('cache', f"{video_hash}.mp4")
        if not os.path.isfile(video_file) or self.force:
            concat_clip = concatenate_videoclips(self.clip_list, method="compose")
            logging.info("Write video file: ") 
            concat_clip.write_videofile(video_file, fps=self.fps)
            
        if os.path.isfile(self.output): 
            os.remove(self.output)
        os.symlink(video_file, self.output)
            
        if not self.keep:
            self.rmtem()