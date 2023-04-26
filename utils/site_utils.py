import re
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from utils.image_utils import random_image_name, chromatic_level
from utils.level_utils import ComplexityLevel


def number_of_images(url):
    """
    Function that outputs the number of images
    on a certain website.

    Parameters
    ==========
    url
        Required, represents the link to the
        desired website.

    Returns
    =======
    num_images
        The number of images.
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


def save_print(url, image, gpu=False):
    """
    Function that save at a designated
    path the screenshot of a site's page.

    Parameters
    ==========
    url
        Required, represents the link to the
        desired website.

    image
        Required, represents the path to the
        image that contains the obtained screenshot.

    gpu
        Optional, if not provided, set to False.

    Returns
    =======
    None
    """
    # Launch Google Chrome in headless mode
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    if gpu == False:
        options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    # Navigate to the webpage
    driver.get(url)

    # Scroll to the bottom of the page to trigger the lazy loading of any images or elements
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    # Take a screenshot of the whole page
    screenshot = driver.find_element_by_tag_name('body').screenshot_as_png

    # Save the screenshot to a file
    with open(image, 'wb') as f:
        f.write(screenshot)

    # Quit the browser
    driver.quit()


def informational_scores(url):
    """
    Function that outputs the informational
    scores of a certain site.

    Parameters
    ==========
    url
        Required, represents the link to the
        desired website.

    Returns
    =======
    text_volume_score
        The amount of text on a website is one of the most basic 
        factors to consider when assessing its complexity. 
        You can measure this by analyzing the number of pages, 
        word count, or character count on the site.

    content_organization_score
        The way content is structured on a website can 
        also impact its complexity. A well-organized site 
        with clear navigation and a logical hierarchy of information 
        can make it easier for users to find what they need.

    content_format_score
        Different types of content can require different 
        levels of comprehension from users. For example, video or interactive 
        content may be more complex than simple text-based articles.

    technical_features_score
        Websites with advanced technical features, such as dynamic 
        content or interactive elements, may require more expertise 
        to build and maintain

    audience_score
        The complexity of a website may also depend on its intended 
        audience. A site aimed at a technical audience may need to 
        use more technical language and include more detailed information 
        than a site aimed at a general audience.

    References
    ==========
    [1]: https://web.eecs.umich.edu/~harshavm/papers/imc11.pdf
    [2]: https://www.jstor.org/stable/25148805
    """
    # Send a GET request to the URL and get the HTML content
    response = requests.get(url)
    html = response.content

    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html, 'html.parser')

    # Find the total number of words on the website
    total_words = len(soup.text.split())

    # Find the number of pages on the website
    num_pages = len(soup.find_all('a'))

    # Find the presence of video or interactive content
    has_video = len(soup.find_all('video')) > 0
    has_interactive = len(soup.find_all('input', type='checkbox')) > 0

    # Find the technical features used on the website
    has_dynamic = len(soup.find_all('script', type='text/javascript')) > 0

    # Determine the intended audience of the website
    has_technical = 'technical' in soup.text.lower()
    has_general = 'general' in soup.text.lower()

    # Compute the complexity score
    text_volume_score = total_words / 1000
    content_organization_score = num_pages / 10
    content_format_score = int(has_video or has_interactive)
    technical_features_score = int(has_dynamic)
    audience_score = 10 * int(has_technical) + 5 * int(has_general)

    # Return the complexity scores
    return text_volume_score, content_organization_score, content_format_score, technical_features_score, audience_score


def informational_level(url):
    """
    Function that outputs the informational
    level of a certain site, out of 100.

    Parameters
    ==========
    url
        Required, represents the link to the
        desired website.

    Returns
    =======
    complexity_level
        The informational level out of 100.
    """
    # Get the complexity scores
    text_volume_score, content_organization_score, content_format_score, technical_features_score, audience_score = informational_scores(
        url)
    text_volume_weight = 0.3
    content_organization_weight = 0.25
    content_format_weight = 0.2
    technical_features_weight = 0.15
    audience_weight = 0.1

    # Compute the complexity level
    complexity_level = (text_volume_weight * text_volume_score) + (content_organization_weight * content_organization_score) + (
        content_format_weight * content_format_score) + (technical_features_weight * technical_features_score) + (audience_weight * audience_score)

    # Return the informational level
    return int(10*complexity_level)


def complexity_level(url):
    """
    Function that outputs the complexity level
    of the site, formed by the two levels described.

    Parameters
    ==========
    url
        Required, represents the link to the
        desired site to be analyzed.

    Returns
    =======
    complexity_levels
        An ComplexityLevel object containing
        the complexity levels of the analyzed site.
    """
    # Compute chromatic level of the site
    filename = random_image_name()
    save_print(url, "./" + str(filename))
    site_chromatic_level = chromatic_level(filename)
    location = "."
    path = os.path.join(location, filename)
    os.remove(path)

    # Compute informational level of the site
    informational_level = informational_level(url)

    # Return the complexity level
    return ComplexityLevel(site_chromatic_level, informational_level)
