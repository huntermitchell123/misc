"""
Hunter Mitchell
12/29/20

Description: Scrapes images from Google based on a search input, compares each image to an input image on your machine,
saves the image that is the most structurally similar, and then shows both of them

Packages Required: Pillow, scikit-image, opencv-python, selenium, webdriver-manager
Note: Must have chromedriver compatible with your chrome version downloaded -> https://chromedriver.chromium.org/downloads
"""


### SSIM Testing imports
from skimage.measure import compare_ssim
from PIL import Image
import cv2

### Webscraping imports
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

### Other imports
import os
import io
import requests
import time
import hashlib



#-------------------------------#
# FILL OUT SPECIFICATIONS HERE  #
#-------------------------------#
DRIVER_PATH = '/Users/huntermitchell/Documents/PYTHON_FILES/chromedriver' # chromedriver executable path
MY_IMAGE_PATH = '/Users/huntermitchell/Desktop/HunterPix/bandanaCut.jpg' # path to image you want to compare (Note: This image will be resized)
SEARCH_TERM = 'actor' # google search term you want to find images based on
NUMBER_OF_IMAGES = 100 # how many images to get
TARGET_PATH = '/Users/huntermitchell/Documents/PYTHON_FILES/compareYourself' # location to store final image




def compareImages(path1,path2):
    """
    Calculates structural similarity between two images. Adapted from
    https://github.com/mostafaGwely/Structural-Similarity-Index-SSIM-

    Parameters:
    path1,path2: filepaths of image locations to compare
    
    Return:
    score between 0 and 1 representing how similar the images are
    """
    img1 = cv2.imread(path1)
    img2 = cv2.imread(path2)

    (score, diff) = compare_ssim(img1, img2, full=True, multichannel=True)
    diff = (diff * 255).astype("uint8")
    print("SSIM: {}".format(score))
    return score




def resizeImage(path):
    """
    Resizes image to 200x200 pixels

    Parameters:
    path: filepath to image location
    """
    temp_pic = Image.open(path,mode='r')
    temp_pic = temp_pic.resize((200,200))
    temp_pic.save(path)



def fetch_image_urls(query:str, max_links_to_fetch:int, wd:webdriver, sleep_between_interactions:float=0.5):
    """
    Gets list of image urls to download
    Adapted from https://towardsdatascience.com/image-scraping-with-python-a96feda8af2d

    Parameters:
    query: search term string
    max_links_to_fetch: number of links to get
    wd: webdriver object
    sleep_between_interactions: time to wait between getting urls (default 0.5)

    Returns: list of image urls
    """
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



def persist_image(count,path_list,folder_path:str,url:str):
    """
    Downloads images from image url list into a folder
    Also adapted from https://towardsdatascience.com/image-scraping-with-python-a96feda8af2d 

    Parameters:
    count: which image number it is on
    path_list: list of paths where images will go
    folder_path: Local path of folder that images will be stored in
    url: URL of image to download
    """
    try:
        img = requests.get(url, timeout=5.0)

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        image_file = io.BytesIO(img.content)

        image = Image.open(image_file).convert('RGB')

        file_path = os.path.join(folder_path,hashlib.sha1(img.content).hexdigest()[:10] + '.jpg')
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
        print(f"SUCCESS - saved {url} - as {file_path}")
        path_list[count] = file_path
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")



def main():

    wd = webdriver.Chrome(executable_path=DRIVER_PATH)

    # resize input image and create empty file paths list
    resizeImage(MY_IMAGE_PATH)
    file_paths = ['']*NUMBER_OF_IMAGES

    os.chdir(TARGET_PATH)

    target_folder = os.path.join('./scraped_images','_'.join(SEARCH_TERM.lower().split(' ')))

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    
    # get list of image urls to download
    res = fetch_image_urls(SEARCH_TERM, NUMBER_OF_IMAGES, wd=wd, sleep_between_interactions=0.25)
    
    
    # download each of them
    count = 0
    for elem in res:
        persist_image(count,file_paths,target_folder,elem)
        count += 1


    # go through each image, calculates structural similarity and keeps top one
    top_image_score = 0.0
    top_path = ''
    for path in file_paths:
        if path != '':
            resizeImage(path)
            temp = compareImages(MY_IMAGE_PATH,path)
            if (temp > top_image_score):
                top_image_score = temp
                top_path = path


    # delete all the other images
    for path in file_paths:
        if path != top_path:
            os.remove(path)


    # prints and shows original image and most similar image
    print(f"Top image path: {top_path} with score of: {top_image_score}")
    final_image = Image.open(top_path,mode='r')
    final_image.show()
    my_image = Image.open(MY_IMAGE_PATH,mode='r')
    my_image.show()


    wd.quit()



if __name__=="__main__":
    main()
