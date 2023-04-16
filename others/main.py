import cv2

cap = cv2.VideoCapture(0)
xml_data = cv2.CascadeClassifier('models/haarcascade_eye.xml')

while True:
    ret, frame = cap.read()
    detecting = xml_data.detectMultiScale(frame, minSize=(30, 30))
    amountDetecting = len(detecting)

    print(amountDetecting)
    if amountDetecting != 0:
        for (a, b, width, height) in detecting:
            cv2.rectangle(frame, (a, b),
                          (a + height, b + width),
                          (0, 275, 0), 9)
    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cv2.release()
cv2.destroyAllWindows()