import re
import requests
from selenium import webdriver


def number_of_images(url):
    """
    Function that outputs the number of images
    on a certain website

    Parameters
    ==========
    url
        Required, represents the link to the
        desired website

    Returns
    =======
    num_images
        The number of images
    """
    response = requests.get(url)
    # print(response.text)
    # Find all image tags in the HTML content
    img_tags = re.findall("<img.*>", response.text)
    # print(img_tags)

    # Filter the image tags to only those with valid image file extensions
    valid_extensions = [".jpg", ".jpeg", ".png", ".gif"]
    valid_img_tags = [tag for tag in img_tags if any(
        ext in tag.lower() for ext in valid_extensions)]

    # Count the number of valid image tags
    num_images = len(valid_img_tags)

    # print(f"There are {num_images} images on {url}")
    return num_images


def save_print(url, image):
    """
    Function that save at a designated
    path the screenshot of a site's page

    Parameters
    ==========
    url
        Required, represents the link to the
        desired website

    Returns
    =======
    None
    """
    driver = webdriver.Chrome()
    driver.get(url)
    driver.get_screenshot_as_file(image)
