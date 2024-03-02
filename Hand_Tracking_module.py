import cv2  # Importing the OpenCV library
import mediapipe as mp  # Importing the Mediapipe library
import time  # Importing the time module

class HandDetector:  # Defining a class for hand detection
    def __init__(self, mode=False, max_hands=2, detection_con=50, track_con=50):
        # Constructor method to initialize the hand detection parameters
        self.mode = mode  # Setting the mode for hand detection
        self.max_hands = max_hands  # Setting the maximum number of hands to detect
        self.detection_con = detection_con  # Setting the detection confidence threshold
        self.track_con = track_con  # Setting the tracking confidence threshold

        # Initializing the Mediapipe Hands module
        self.mp_hands = mp.solutions.hands
        # Creating an instance of the Hands class with specified parameters
        self.hands = self.mp_hands.Hands(self.mode, self.max_hands, self.detection_con, self.track_con)
        # Initializing the drawing utilities from Mediapipe
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):  # Method to find hands in an image
        # Converting the image to RGB format for Mediapipe processing
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Processing the image to detect hands
        results = self.hands.process(img_rgb)
        # Checking if hands are detected
        if results.multi_hand_landmarks:
            for hand_lms in results.multi_hand_landmarks:
                if draw:
                    # Drawing landmarks on the image if draw parameter is True
                    self.mp_draw.draw_landmarks(img, hand_lms, self.mp_hands.HAND_CONNECTIONS)

    def main(self):  # Main method to capture video and detect hands
        p_time = 0  # Initializing previous time variable for FPS calculation
        cap = cv2.VideoCapture(0)  # Capturing video from the default camera
        # detector = HandDetector()
        while True:  # Running an infinite loop for video capture
            success, img = cap.read()  # Reading a frame from the camera

            if not success:  # Checking if frame reading was successful
                print("Error: Failed to read frame from camera")  # Printing error message
                break  # Exiting the loop if frame reading failed

            self.find_hands(img)  # Calling the find_hands method to detect hands in the image

            c_time = time.time()  # Getting the current time for FPS calculation
            fps = 1 / (c_time - p_time)  # Calculating frames per second
            p_time = c_time  # Updating previous time for next iteration

            # Displaying the FPS on the image
            cv2.putText(img, f"FPS: {int(fps)}", (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

            # Displaying the image with detected hands
            cv2.imshow("Image", img)

            key = cv2.waitKey(1)  # Waiting for a key press

            if key == ord('q'):  # Checking if 'q' key is pressed
                break  # Exiting the loop if 'q' key is pressed

        cap.release()  # Releasing the camera resource
        cv2.destroyAllWindows()  # Closing all OpenCV windows

if __name__ == "__main__":  # Checking if the script is executed directly
    hd = HandDetector()  # Creating an instance of the HandDetector class
    hd.main()  # Calling the main method to start hand detection
