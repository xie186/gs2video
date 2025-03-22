import os
import sys
import hashlib
import logging
import urllib.request
from googleapiclient.discovery import build
from gtts import gTTS
from moviepy import *
import soundfile as sf
from kokoro_onnx import Kokoro
from misaki import en, espeak
import logging

logging.basicConfig(level=logging.INFO)

# Misaki G2P with espeak-ng fallback
fallback = espeak.EspeakFallback(british=False)
g2p = en.G2P(trf=False, british=False, fallback=fallback)
# Kokoro
kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")

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

    def process_slide(self, slide, video_hash, index, presentation_id):
        logging.info('- Slide #{} contains {} elements.'.format(index + 1, len(slide.get('pageElements')))) 
        text = slide['slideProperties']['notesPage']['pageElements'][1]['shape']['text']['textElements'][1]['textRun']['content']
        #for element in slide['slideProperties']['notesPage']['pageElements'][1]['shape']['text']['textElements']:
        #    print(element.keys())
        #    print(f'Element {element}:{element[1]['textRun']['content']}')
        text_hash = self.generate_hash(text)
        video_hash.update(text_hash.encode('utf-8'))
        
        tem_audio = self.process_audio_kokoro(text, text_hash, index)
        tem_png = self.process_image(slide, video_hash, index, presentation_id)
        
        tem_audiocontent = AudioFileClip(tem_audio)
        print(tem_audiocontent.duration)
        clip = ImageClip(tem_png).with_duration(tem_audiocontent.duration).with_audio(tem_audiocontent)
        self.clip_list.append(clip)

    def process_audio(self, text, text_hash, index):
        tem_audio = os.path.join(self.cache_dir, f"slide-{index}_{text_hash}.mp3")
        if not os.path.isfile(tem_audio):
            v = gTTS(text=text, lang=self.language, slow=False) 
            v.save(tem_audio) 
        tem_audiocontent = AudioFileClip(tem_audio)
        #print(tem_audiocontent)
        self.tem_files.append(tem_audio)
        return tem_audio

    def process_image(self, slide, video_hash, index, presentation_id):
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
        tem_png = os.path.join(self.cache_dir, f"slide-{index}_{img_hash}.png")
        
        if not os.path.isfile(tem_png):
            with open(tem_png, 'wb') as f:
                f.write(img_content)
        self.tem_files.append(tem_png)
        return tem_png
    
    def process_audio_kokoro(self, text, text_hash, index):
        print(f'Slide-{index} text: {text}')
        tem_audio = os.path.join(self.cache_dir, f"slide-{index}_{text_hash}.wav")
        if not os.path.isfile(tem_audio):
            phonemes, _ = g2p(text)
            samples, sample_rate = kokoro.create(phonemes, 'af_heart', is_phonemes=True)
            sf.write(tem_audio, samples, sample_rate)
        tem_audiocontent = AudioFileClip(tem_audio)
        print(tem_audiocontent)
        self.tem_files.append(tem_audio)
        return tem_audio