import cv2

# image processing utility functions
# install by running - pip install imutils
import imutils


def detect_image_difference(path1, path2):
    original = cv2.imread(path1)
    new = cv2.imread(path2)
    # resize the images to make them smaller. Bigger image may take a significantly
    # more computing power and time
    original = imutils.resize(original, height=600)
    new = imutils.resize(new, height=600)
    diff = original.copy()
    cv2.absdiff(original, new, diff)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # increasing the size of differences so we can capture them all
    for i in range(0, 3):
        dilated = cv2.dilate(gray.copy(), None, iterations=i + 1)
    (T, thresh) = cv2.threshold(dilated, 3, 255, cv2.THRESH_BINARY)

    # now we need to find contours in the binarised image
    cnts = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    for c in cnts:
        # fit a bounding box to the contour
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(new, (x, y), (x + w, y + h), (0, 255, 0), 2)
    similarity_score = 1 - (cv2.countNonZero(gray) / (gray.shape[0] * gray.shape[1]))

    # Print similarity score
    print("Similarity Score:", similarity_score)

    # uncomment below 2 lines if you want to
    # view the image press any key to continue
    # write the identified changes to disk
    cv2.imwrite("changes.png", new)
    return new, similarity_score
