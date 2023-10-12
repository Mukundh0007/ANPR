import cv2
import imutils
import pytesseract

#download the haarcascade for number plate detection
haarcascade = "path/to/haarcascade_russian_plate_number.xml"
#realtime detection and OCR
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # width
cap.set(4, 480)  # height
min_area = 500
count = 0

while True:
    success, img = cap.read()

    plate_cascade = cv2.CascadeClassifier(haarcascade)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

    for (x, y, w, h) in plates:
        area = w * h

        if area > min_area:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
            cv2.putText(img, "Number Plate", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)

            img_roi = img[y: y + h, x:x + w]
            cv2.imshow("ROI", img_roi)
            new_image = cv2.convertScaleAbs(img_roi, alpha=1.5, beta=20)
            # cv2.imshow("",new_image)
            try:
                _, thresholded = cv2.threshold(new_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                thresholded = imutils.resize(thresholded, width=500)
                result = pytesseract.image_to_string(thresholded, config='--psm 7 digits ', lang='eng')
            except:
                result = pytesseract.image_to_string(img_roi, config='--psm 7 digits ', lang='eng')
            print(result)

    cv2.imshow("Result", img)

    if cv2.waitKey(1) & 0xFF == ord('s'):
        # cv2.imwrite("plates/scaned_img_" + str(count) + ".jpg", img_roi)
        cv2.rectangle(img, (0, 200), (640, 300), (0, 255, 0), cv2.FILLED)
        # cv2.putText(img, "Plate Saved", (150, 265), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255), 2)
        # cv2.imshow("Results", img)
        cv2.waitKey(100)
        count += 1

print(x)
