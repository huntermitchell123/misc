### Code that returns image most similar to your input image from list of scraped google images
### Written by Hunter Mitchell - 4/7/20 

### Note: Must have chromedriver executable set up in existing path, along with Pillow, Selenium, and Skimage

### SSIM Testing imports
from skimage.measure import compare_ssim
from PIL import Image
import argparse
import imutils
import cv2

### Webscraping imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image

import json
import os
import io
import requests
import urllib
import argparse
import time
import hashlib


### FILL OUT CHROMEDRIVER PATH HERE ###
DRIVER_PATH = '/Users/huntermitchell/Desktop/chromedriver 2'
wd = webdriver.Chrome(executable_path=DRIVER_PATH)
#######################################

### ENTER STUFF HERE ###
own_path = '/Users/huntermitchell/Downloads/hunter.jpeg'
search_term = 'cat'
number_of_images = 20
########################


### Function for calculating SSIM between two images. Adaptd from https://github.com/mostafaGwely/Structural-Similarity-Index-SSIM-
def compareImages(path1,path2):
    imageA = cv2.imread(path1)
    imageB = cv2.imread(path2)
    (score, diff) = compare_ssim(imageA, imageB, full=True, multichannel=True)
    diff = (diff * 255).astype("uint8")
    print("SSIM: {}".format(score))
    return score

### Function to resize image to 200 x 200 pixels, since images must be the same size to compare
def resizeImage(path):
    temp_pic = Image.open(path,mode='r')
    temp_pic = temp_pic.resize((200,200))
    temp_pic.save(path)


### Functions to scrape images from web. Adapted from https://towardsdatascience.com/image-scraping-with-python-a96feda8af2d

### Function to get the image urls based on search
def fetch_image_urls(query:str, max_links_to_fetch:int, wd:webdriver, sleep_between_interactions:int=1):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)    
    
    # build the google query
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    # load the page
    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    results_start = 0
    while image_count < max_links_to_fetch:
        scroll_to_end(wd)

        # get all image thumbnail results
        thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
        number_results = len(thumbnail_results)
        
        print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")
        
        for img in thumbnail_results[results_start:number_results]:
            # try to click every thumbnail such that we can get the real image behind it
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue

            # extract image urls    
            actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))

            image_count = len(image_urls)

            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!")
                break
        else:
            print("Found:", len(image_urls), "image links, looking for more ...")
            time.sleep(30)
            return
            load_more_button = wd.find_element_by_css_selector(".mye4qd")
            if load_more_button:
                wd.execute_script("document.querySelector('.mye4qd').click();")

        # move the result startpoint further down
        results_start = len(thumbnail_results)

    return image_urls


### Function to download images into folder
def persist_image(count,path_list,folder_path:str,url:str):
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        image_file = io.BytesIO(image_content)

        image = Image.open(image_file).convert('RGB')

        file_path = os.path.join(folder_path,hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
        print(f"SUCCESS - saved {url} - as {file_path}")
        path_list[count] = file_path 
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")


### Function that loops through and puts all downloaded images in folder
def search_and_download(path_list,search_term:str,driver_path:str,target_path='./scraped_images',number_images=5):
    target_folder = os.path.join(target_path,'_'.join(search_term.lower().split(' ')))

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    with webdriver.Chrome(executable_path=driver_path) as wd:
        res = fetch_image_urls(search_term, number_images, wd=wd, sleep_between_interactions=0.5)
        
    count = 0
    for elem in res:
        persist_image(count,path_list,target_folder,elem)
        count = count + 1




# resize input image and create empty file paths list
resizeImage(own_path)
file_paths = ['']*number_of_images



search_and_download(file_paths,search_term=search_term,driver_path=DRIVER_PATH,number_images=number_of_images)


### Goes through each path, calculates similarity and keeps top one
top_image_score = 0
top_path = ''
for path in file_paths:
    resizeImage(path)
    temp = compareImages(own_path,path)
    if (temp > top_image_score):
        top_image_score = temp
        top_path = path


# delete all the other ones
for path in file_paths:
    if path != top_path:
        os.remove(path)


# prints and shows original image and most similar image
print('Top image path: ',top_path,' with score of: ',top_image_score)
final_image = Image.open(top_path,mode='r')
final_image.show()
own_image = Image.open(own_path,mode='r')
own_image.show()

wd.quit()
