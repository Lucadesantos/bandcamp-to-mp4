import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import os

def getAllTracksURL(pageURL):
    print("Getting all tracks URL")
    page = requests.get(pageURL)
    soup = BeautifulSoup(page.content, 'html.parser')
    trackURLs, albumsURLs = [], []
    
    gridItems = soup.find_all('li', class_='music-grid-item')
    for item in gridItems:
        track = item.find('a')['href']
        if "track" in track:
            trackURLs.append(pageURL.strip("/") + item.find('a')['href'])
        elif "album" in track: 
            albumsURLs.append(pageURL.strip("/") + item.find('a')['href'])
    return trackURLs, albumsURLs

def getTrackInfo(trackURL):
    print("Getting track info for: " + trackURL)
    try:
        chromedriver_autoinstaller.install() 
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-logging")
        options.add_argument("--log-level=3")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        driver.get(trackURL)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        title = soup.find('h2', class_='trackTitle').text.strip()
        artist = soup.find('h3', class_='albumTitle').text.strip()

        artist = artist.split("\n")[-1].strip()
        
        videoTitle = artist + " - " + title
        image = soup.find('a', class_='popupImage').find('img')['src']
        #click on play button
        driver.find_element_by_class_name('playbutton').click()
        driver.find_element_by_class_name('playbutton').click()
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        audios = soup.find_all('audio')
        for audio in audios:
            if audio['src'] != "":
                audio = audio['src']
                break
        driver.close()
        driver.quit()
        return videoTitle, image, audio
    except Exception as e:
        print(e)
        driver.close()
        driver.quit()
        exit()

def downloadTrackData(videoTitle, image, audio, path):
    print("Downloading track elements for: " + videoTitle)
    with open(path + "/" + videoTitle + ".jpg", "wb") as f:
        f.write(requests.get(image).content)
    with open(path + "/" + videoTitle + ".wav", "wb") as f:
        f.write(requests.get(audio).content)

def downloadAlbumData(albumTitle, image, tracks, output):
    # if directory output + "/" + videoTitle + " doesn't exist, create it
    if not os.path.exists(output + "/" + albumTitle):
        os.makedirs(output + "/" + albumTitle)
    with open(output + "/" + albumTitle + ".jpg", "wb") as f:
        f.write(requests.get(image).content)

    pos = 1
    for track in tracks:
        with open(output + "/" + albumTitle + "/" + str(pos) + " " + track['title'] + ".wav", "wb") as f:
            f.write(requests.get(track['audio']).content)
        pos += 1

def getAlbumTracks(URL, output):
    print("Getting album info for: " + URL)
    tracks = []
    titles = []
    try:
        chromedriver_autoinstaller.install() 
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-logging")
        options.add_argument("--log-level=3")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        driver.get(URL)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        title = soup.find('h2', class_='trackTitle').text.strip()
        artist = soup.find('h3').text.strip()

        artist = artist.split("\n")[-1].strip()
        
        videoTitle = artist + " - " + title
        image = soup.find('a', class_='popupImage').find('img')['src']
        playButtons = driver.find_elements_by_class_name('play-col')
        for playButton in playButtons:
            playButton.click()
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            audios = soup.find_all('audio')
            for audio in audios:
                if audio['src'] != "":
                    tracks.append(audio['src'])
                    break
            title = soup.find_all('span', class_='track-title')
        for t in title:
            titles.append(t.text.strip())
        print("Tracks in album: ", titles)
        for i in range(len(tracks)):
            tracks[i] = {"title": titles[i], "audio": tracks[i]}

        driver.find_element_by_class_name('playbutton').click()
        driver.close()
        driver.quit()
        return videoTitle, image, tracks
    except Exception as e:
        print(e)
        driver.close()
        driver.quit()
        exit()

def mainExport(pageURL, output):
    print("Starting export")
    trackURLs, albumsURLs = getAllTracksURL(pageURL)
    for trackURL in trackURLs:
        videoTitle, image, audio = getTrackInfo(trackURL)
        downloadTrackData(videoTitle, image, audio, output)
    for albumURL in albumsURLs:
        albumTitle, image, tracks = getAlbumTracks(albumURL, output)
        downloadAlbumData(albumTitle, image, tracks, output)


