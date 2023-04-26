import cv2
import re
import numpy as np
import names


def random_image_name(extension=".png"):
    """
    Function that outputs a random name
    for an image file.

    Parameters
    ==========
    extension
        Optional, represents the type of
        the image file.

    Returns
    =======
    filename
        The name of desired file.
    """
    filename = re.sub(" ", "__", names.get_full_name())
    return str(filename) + extension


def chromatic_score(image):
    """
    Function that outputs a float number associated
    to the image's chromatic score.

    Parameters
    ==========
    image
        Required, represents the path to the image
        file to be analyzed.

    Returns
    =======
    colorfulness
        The chromatic score, which according to
        the cited article is between 0 and around
        109 (for simplity and safety we will consider
        the maximum to be 120).

    References
    ==========
    [1]: https://infoscience.epfl.ch/record/33994
    """
    # Load input image
    image = cv2.imread(image)
    (B, G, R) = cv2.split(image)

    # Compute rg = R - G
    rg = np.absolute(R - G)

    # Compute yb = 0.5 * (R + G) - B
    yb = np.absolute(0.5 * (R + G) - B)

    # Compute the mean and standard deviation of both `rg` and `yb`
    rgMean, rgStd = np.mean(rg), np.std(rg)
    ybMean, ybStd = np.mean(yb), np.std(yb)

    # Combine the mean and standard deviations
    stdRoot = np.sqrt((rgStd ** 2) + (ybStd ** 2))
    meanRoot = np.sqrt((rgMean ** 2) + (ybMean ** 2))

    # Derive the "colorfulness" metric and return it
    return stdRoot + (0.3 * meanRoot)


def chromatic_level(image):
    """
    Function that outputs a positive number smaller 
    than 100 representing the chromatic level of an image.

    Parameters
    ==========
    image
        Required, represents the path to the image
        file to be analyzed.

    Returns
    =======
    level
        The chromatic level on a scale from 0 to 100.
    """
    # Compute the score between 0 and 120
    score = chromatic_score(image)

    return int(score/1.2)


def most_correlated(input_image, candidate_images):
    """
    Function that outputs in order of correlation
    the candidate images in respect to the input
    image.

    Parameters
    ==========
    input_image
        Required, represents the path to the image
        file that is used as a fixed point in searching
        the image that fits the best with it.

    candidate_images
        Required, represents the array of candidate
        images that are to be ordered based on the
        correlation with the input image.

    Returns
    =======
    ordered_images
        The ordered images based on correlation.
    """
    # Load input image
    input_image = cv2.imread(input_image)

    # Convert to LAB color space
    lab_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2LAB)

    # Calculate color histogram of input image
    hist = cv2.calcHist([lab_image], [1, 2], None, [
                        128, 128], [0, 128, 0, 128])

    # Calculate color histogram of each candidate image
    candidate_hists = []
    for candidate_image in candidate_images:
        candidate_image = cv2.imread(candidate_image)
        candidate_lab_image = cv2.cvtColor(candidate_image, cv2.COLOR_BGR2LAB)
        candidate_hist = cv2.calcHist([candidate_lab_image], [1, 2], None, [
                                      128, 128], [0, 128, 0, 128])
        candidate_hists.append(candidate_hist)

    # Compare histograms using correlation distance
    # (which should be higher for better correlation, so therefore the minus)
    distances = []
    for candidate_hist in candidate_hists:
        distance = cv2.compareHist(hist, candidate_hist, cv2.HISTCMP_CORREL)
        distances.append(-distance)

    # Sort candidate images based on distance
    sorted_candidates = [candidate_images[i] for i in np.argsort(distances)]

    # Select the most similar image
    most_similar_images = sorted_candidates

    # Return the best images in order
    return most_similar_images
