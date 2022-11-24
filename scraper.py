import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller

def getAllTracksURL(pageURL):
    print("Getting all tracks URL")
    page = requests.get(pageURL)
    soup = BeautifulSoup(page.content, 'html.parser')
    trackURLs = []
    gridItems = soup.find_all('li', class_='music-grid-item')
    for item in gridItems:
        track = item.find('a')['href']
        if "track" in track:
            trackURLs.append(pageURL.strip("/") + item.find('a')['href'])
    return trackURLs

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
        #wait for audio to load
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
    

def mainExport(pageURL, output):
    print("Starting export")
    trackURLs = getAllTracksURL(pageURL)
    for trackURL in trackURLs:
        videoTitle, image, audio = getTrackInfo(trackURL)
        downloadTrackData(videoTitle, image, audio, output)
