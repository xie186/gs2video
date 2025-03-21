import argparse
from utils import credential
from core import GS2Video

def main():
    parser = argparse.ArgumentParser(description='Slide to video')
    parser.add_argument('-p', '--presentation_id', 
                        help='Presentation_ID', required=True)
    parser.add_argument('-f', '--fps', metavar="fps", type=int, 
                        help='Frames per second (FPS)', required=False, default=24)
    parser.add_argument('-l', '--language', type=str, 
                        help='Language in the note', required=False, default='en')
    parser.add_argument('--keep', action='store_true', 
                        help="Keep intermediate files (mp3 and png files)")
    parser.add_argument('--force', action='store_true', 
                        help='Force generate the output video even if it already exists')
    parser.add_argument('-o', '--output',
                        help='output file', default="Output_file.mp4")
    
    options = parser.parse_args()
    creds = credential()
    gs2video = GS2Video(credentials=creds, output=options.output, language=options.language, fps=options.fps, keep=options.keep, force=options.force)
    gs2video.to_video(options.presentation_id)

if __name__ == '__main__':
    main()