import cv2

print("Starting camera test...")

for camera_number in [0, 1, 2]:
    print("Trying camera:", camera_number)

    camera = cv2.VideoCapture(camera_number, cv2.CAP_DSHOW)

    if camera.isOpened():
        print("Camera found:", camera_number)

        while True:
            ret, frame = camera.read()

            if not ret:
                print("Cannot read camera.")
                break

            cv2.imshow("Camera Test - Press Q", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        camera.release()
        cv2.destroyAllWindows()
        break

    camera.release()

else:
    print("No camera found!")