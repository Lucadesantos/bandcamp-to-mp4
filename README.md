# Bandcamp to mp4
A python script to transform an entire bandcamp library into video files.

**DISCLAIMER: Only use this on music you own, I coded this to move my bancamp tracks to youtube easily, do not use this script to download music you have not bought.**

## Usage
  
```bc2mp4.py [-h] (-u URL | -t TRACK | -a ALBUM) -o OUTPUT [-k]```

required arguments:

  - -u URL, --url URL           URL to the Bandcamp page
  - OR
  - -t TRACK, --track TRACK     Convert a track
  - OR
  - -a ALBUM, --album ALBUM     Convert an album
  - -o OUTPUT, --output OUTPUT  Output directory
 
optional arguments:

  - -h, --help                  show this help message and exit
  
  - -k, --keep                  Keep the audio and image source files

## Required libraries

- selenium
- bs4
- moviepy
- argparse
- chromedriver_autoinstaller
- requests
