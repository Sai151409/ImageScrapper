import os
import time
import requests
from selenium import webdriver


def fetch_img_links(search_string : str, max_fetch_links : int, wd : webdriver, sleep_between_interactions : float = 1):
    def scroll_to_end(wd):
        wd.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(sleep_between_interactions)

    search_url = search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    wd.get(search_url.format(q=search_string))

    image_urls = set()
    image_count = 0
    results_start = 0
    while image_count < max_fetch_links:
        scroll_to_end(wd)
        thumbnails_result = wd.find_elements_by_css_selector('img.Q4LuWd')
        number_result = len(thumbnails_result)

        print(f'Found {number_result} images. Extracting images from {results_start} : {number_result}]')

        for img in thumbnails_result[results_start:number_result]:
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except:
                continue
            actual_images = wd.find_elements_by_css_selector('img.n3VNCb')

            for actual_image in actual_images:
                if actual_image.get_attribute('src') and "https" in actual_image.get_attribute("src"):
                    image_urls.add(actual_image.get_attribute('src'))

            image_count = len(image_urls)

            if image_count >= max_fetch_links:
                print(f'Found {image_count} image links and done...')
                break
        else:
            print(f'Found {image_count} image urls. Looking for more.....')
            time.sleep(sleep_between_interactions)
            load_more_button = wd.find_elements_by_css_selector('.mye4qd')

            if load_more_button:
                wd.execute_script("document.querySelector('.mye4qd').click();")

        results_start = len(thumbnails_result)

    return image_urls


def persist_images(folder_path : str, url : str, counter):
    try:
        image_content = requests.get(url).content
    except Exception as e:
        print(f'Error has occured for {url} - {e}')

    try:
        f = open(os.path.join(folder_path, 'jpg_'+str(counter)+'.jpg'), 'wb')
        f.write(image_content)
        f.close()
        print(f'Successfully Downloaded {url}')
    except Exception as e:
        print(f'Error has occured {url} - {e}')


def search_and_download(search_term : str, driver_path = str, target_path = "./images", number_images : int = 10):
    target_folder= os.path.join(target_path, "_".join(search_term.lower().split(' ')))

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    with webdriver.Chrome(executable_path=driver_path) as wd:
        res = fetch_img_links(search_string=search_term, max_fetch_links=number_images, wd=wd, sleep_between_interactions=0.5)

    counter = 0
    for ele in res:
        persist_images(folder_path=target_folder, url=ele, counter=counter)
        counter += 1


term = 'Jr NTR'
path = r'C:\Users\Asus\PycharmProjects\ImageScrapper1\chromedriver.exe'
number = 1


search_and_download(search_term=term, driver_path=path, number_images=number)
