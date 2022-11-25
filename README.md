# Bandcamp to mp4
A python script to transform an entire bandcamp library into video files.

**DISCLAIMER: Only use this on music you own, I coded this to move my bancamp tracks to youtube easily, do not use this script to download music you have not bought.**

## Usage
  
```bc2mp4.py [-h] (-u URL | -t TRACK | -a ALBUM) -o OUTPUT [-k]```

required arguments (one of the three):

  - -u URL, --url URL           URL to the Bandcamp page
  - -t TRACK, --track TRACK     Convert a track
  - -a ALBUM, --album ALBUM     Convert an album
  
optional arguments:

  - -h, --help                  show this help message and exit
  - -o OUTPUT, --output OUTPUT  Output directory
  - -k, --keep                  Keep the audio and image source files

## Required libraries

- selenium
- bs4
- moviepy
- argparse
- chromedriver_autoinstaller
- requests
