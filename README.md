# Bandcamp to mp4
A python script to transform an entire bandcamp library into video files.

## Usage

  python3 bc2mp4.py -u URL -o output [-k]
  
- -u (--URL): Bandcamp site URL
- -o (--output): Output directory
- -k (--keep): Keep source files (default = False)

## Required libraries

- selenium
- bs4
- moviepy
- argparse
- chromedriver_autoinstaller
- requests
