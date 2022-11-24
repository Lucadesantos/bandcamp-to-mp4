import argparse
from moviepy.editor import AudioFileClip, ImageClip, VideoClip
import scraper
import os 


def createVideo(audio, image, fileSaveName):
    print("Creating video for: " + fileSaveName)
    audio_clip = AudioFileClip(audio)
    image_clip = ImageClip(image)
    image_clip.duration = audio_clip.duration
    image_clip.fps = 24
    image_clip = image_clip.set_audio(audio_clip)
    image_clip.write_videofile(fileSaveName)


def mainLinkToVideos(link, output, keep):
    
    scraper.mainExport(link, output)
    allTitlesRaw = os.listdir(output)
    allTitlesFormatted = []
    for title in allTitlesRaw:
        allTitlesFormatted.append(title.split(".")[0])
    for title in set(allTitlesFormatted):
        
        image = output + "/" + title + ".jpg"
        audio = output + "/" + title + ".wav"
        video = output + "/" + title + ".mp4"
        createVideo(audio, image, video)
        if not keep:
            os.remove(image)
            os.remove(audio)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="URL to the bandcamp page")
    parser.add_argument("-o", "--output", help="Output directory")
    parser.add_argument("-k", "--keep", help="Keep the audio and image files", required=False, action="store_true")
    args = parser.parse_args()
    mainLinkToVideos(args.url, args.output, args.keep)
