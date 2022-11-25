import argparse
from moviepy.editor import AudioFileClip, ImageClip, VideoClip, concatenate_audioclips
import scraper
import os 


def createVideoTrack(audio, image, fileSaveName):
    print("Creating video for: " + fileSaveName)
    audio_clip = AudioFileClip(audio)
    image_clip = ImageClip(image)
    image_clip.duration = audio_clip.duration
    image_clip.fps = 24
    image_clip = image_clip.set_audio(audio_clip)
    image_clip.write_videofile(fileSaveName)

def createVideoAlbum(tracksDir, image, video):
    print("Creating video for: " + video)
    tracks = os.listdir(tracksDir)
    tracks.sort()
    clips = []
    for track in tracks:
        audio_clip = AudioFileClip(tracksDir + "/" + track)
        clips.append(audio_clip)
    audio_clip = concatenate_audioclips(clips)
    image_clip = ImageClip(image)
    image_clip.duration = audio_clip.duration
    image_clip.fps = 24
    image_clip = image_clip.set_audio(audio_clip)
    image_clip.write_videofile(video)


def convertAll(output, keep):
    
    allTitlesRaw = os.listdir(output)
    allTitlesFormatted = []
    for title in allTitlesRaw:
        allTitlesFormatted.append(title.split(".")[0])
    for title in set(allTitlesFormatted):
        # check if track is not already converted
        if not os.path.exists(output + "/" + title + ".mp4"):
            if os.path.isdir(output + "/" + title):
                image = output + "/" + title + ".jpg"
                tracksDir = output + "/" + title
                video = output + "/" + title + ".mp4"
                createVideoAlbum(tracksDir, image, video)
                if not keep:
                    os.remove(image)
                    # delete tracks
                    for track in os.listdir(tracksDir):
                        os.remove(tracksDir + "/" + track)
                    os.rmdir(tracksDir)
            else:
                image = output + "/" + title + ".jpg"
                audio = output + "/" + title + ".wav"
                video = output + "/" + title + ".mp4"
                createVideoTrack(audio, image, video)
                if not keep:
                    os.remove(image)
                    os.remove(audio)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-u", "--url", help="URL to the bandcamp page", required=False)
    group.add_argument("-t", "--track", help="Convert a track", required=False)
    group.add_argument("-a", "--album", help="Convert an album", required=False)
    parser.add_argument("-o", "--output", help="Output directory", required=True)
    parser.add_argument("-k", "--keep", help="Keep the audio and image files", required=False, action="store_true")
    args = parser.parse_args()
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    if args.track:
        if not "track" in args.track:
            print("Invalid track URL")
            exit()
        scraper.downloadTrack(args.track, args.output)
        convertAll(args.output, args.keep)
    elif args.album:
        if not "album" in args.album:
            print("Invalid album URL")
            exit()
        scraper.downloadAlbum(args.album, args.output)
        convertAll(args.output, args.keep)
    else:
        scraper.mainExport(args.url, args.output)
        convertAll(args.output, args.keep)

