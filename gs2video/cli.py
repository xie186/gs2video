import argparse
from utils import credential
from core import GS2Video

def parse_rgb(value):
    try:
        r, g, b = map(int, value.split(','))
        return (r, g, b)
    except:
        raise argparse.ArgumentTypeError("RGB values must be three integers separated by commas")

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
    parser.add_argument('--duration', type=int, 
                        help='Duration of each slide in seconds', 
                        default=0.5, required=False)
    parser.add_argument('--bg_color', type=parse_rgb, 
                        help='Background color during transitions (RGB values as comma-separated integers)', 
                        required=False, default=(0, 0, 0))
    parser.add_argument('-o', '--output',
                        help='output file', default="Output_file.mp4")
    
    options = parser.parse_args()
    creds = credential()
    gs2video = GS2Video(credentials=creds, 
                        output=options.output, 
                        language=options.language, 
                        fps=options.fps, 
                        keep=options.keep, 
                        force=options.force, 
                        bg_color=options.bg_color)
    gs2video.to_video(options.presentation_id)

if __name__ == '__main__':
    main()