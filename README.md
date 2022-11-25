# Bandcamp to mp4
A python script to transform an entire bandcamp library into video files.

**DISCLAIMER: Only use this on music you own, I coded this to move my bancamp tracks to youtube easily, do not use this script to download music you have not bought.**

## Usage

  ```python3 bc2mp4.py -u URL -o output [-k]```
  
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
