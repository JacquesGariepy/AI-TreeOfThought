import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # Apply a mirror effect to the image
    frame = cv2.flip(frame, 1)

    # Display the image with the mirror effect
    cv2.imshow('Cool Visual Effect', frame)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
