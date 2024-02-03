"""
Author: Jacob Pitsenberger
date: 1/30/24
Description:
    This Module initializes the GameControllerGUI class and calls its run application method.
    This allows for the Tello drone to be controlled using an xbox one game controller with
    current capabilities allow for the joysticks (left and right) to be used for controlling
    the drones movement by sending RC control commands and for the takeoff/land command to be
    sent to the drone by pressing the controllers start button.
"""

import time
import cv2
import threading
from djitellopy import tello
from tkinter import *
from PIL import Image, ImageTk
from xbox_one_controller import XboxController


class GameControllerGUI:
    def __init__(self):

        ### **** NEW **** ###
        self.xbox_controller = XboxController()  # Initialize the xbox controller object
        ### ************* ###

        # Prepare our GUI window
        self.root = Tk()  # Initialize the Tkinter window
        self.root.title("Tello Drone Control GUI with Xbox Game Controller")  # Add a title to the window
        self.root.minsize(800, 600)  # Set the minimum gui size

        # Initialize the video stream capture label
        self.cap_lbl = Label(self.root)

        # Prepare our drone object
        self.drone = tello.Tello()  # Initialize the drone
        self.drone.connect()  # Connect to the drone
        self.drone.streamon()  # Turn on the drones video stream

        # Initialize variables involving drone functionalities
        self.frame = self.drone.get_frame_read()  # variable to get the video frames from the drone

        ### **** NEW **** ###
        # this is to store the joystick rc values as they are updated in realtime.
        self.rc_controls = [0, 0, 0, 0]  # the initial movement velocity values for lr, fb, ud, and yaw motions
        ### ************* ###

    def takeoff_land(self):
        """Set the command for the takeoff/land button depending on the drones flying state"""
        if self.drone.is_flying:
            threading.Thread(target=lambda: self.drone.land()).start()
        else:
            threading.Thread(target=lambda: self.drone.takeoff()).start()

    ### **** NEW METHOD **** ###
    def update_joystick(self):
        """Method to update joystick values."""
        try:
            # Read current joystick values using the XboxController class
            joystick_values = self.xbox_controller.read()

            # Extract individual joystick values for easier reference
            left_joystick_x = joystick_values[0]
            left_joystick_y = joystick_values[1]
            right_joystick_x = joystick_values[2]
            right_joystick_y = joystick_values[3]
            start_button = joystick_values[14]

            # Check if the start button is pressed
            if start_button:
                self.takeoff_land()  # Call the takeoff/land method if the start button is pressed
                time.sleep(0.15)  # sleep long enough to register button as not pressed so no false send of land command.

            # Map joystick values to specific RC control channels
            self.rc_controls[0] = right_joystick_x  # lr RC value
            self.rc_controls[1] = right_joystick_y  # fb RC value
            self.rc_controls[2] = left_joystick_y  # ud RC value
            self.rc_controls[3] = left_joystick_x  # yaw RC value

            # If rc control values aren't zero then send them to the drone using the send_rc_control(lr, fb, ud, yv) command.
            if self.rc_controls != [0, 0, 0, 0]:
                self.drone.send_rc_control(self.rc_controls[0], self.rc_controls[1], self.rc_controls[2], self.rc_controls[3])

            # and if not zero then send the equivalent command for the drone to hover in place
            else:
                self.drone.send_rc_control(0, 0, 0, 0)
            # Call the update_joystick method again after a delay (50 milliseconds)
            self.root.after(50, self.update_joystick)

        # Handle exceptions that may occur during joystick update
        except Exception as joystickUpdateException:
            print(f"Exception occurred when updating joystick values.\nJoystickUpdateException: {joystickUpdateException}")
    ### ************* ###

    def run_app(self):
        """Method to run the application."""
        try:
            # Pack the video stream label to the GUI window
            self.cap_lbl.pack(anchor="center")

            # Call the video_stream method to start displaying video
            self.video_stream()

            ### **** NEW **** ###
            # Call the update_joystick method to start the joystick control
            self.update_joystick()
            ### ************* ###

            # Start the tkinter main loop
            self.root.mainloop()
        except Exception as runAppException:
            print(f"Exception occurred when running the application.\nrunAppException: {runAppException}")
        finally:
            # When the root window is exited out of ensure to clean up any resources.
            self.cleanup()

    def video_stream(self):
        """Method to display video stream."""
        try:
            # Define the height and width to resize the current frame to
            h = 480
            w = 720

            # Read a frame from our drone
            frame = self.frame.frame

            frame = cv2.resize(frame, (w, h))

            # Convert the current frame to the rgb colorspace
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

            # Convert this to a Pillow Image object
            img = Image.fromarray(cv2image)

            # Convert this then to a Tkinter compatible PhotoImage object
            imgtk = ImageTk.PhotoImage(image=img)

            # Place the image label at the center of the window
            self.cap_lbl.pack(anchor="center", pady=15)

            # Set it to the photo image
            self.cap_lbl.imgtk = imgtk

            # Configure the photo image as the displayed image
            self.cap_lbl.configure(image=imgtk)

            # Update the video stream label with the current frame
            # by recursively calling the method itself with a delay.
            self.cap_lbl.after(5, self.video_stream)
        except Exception as videoStreamException:
            print(f"Exception occurred when updating the video stream.\nvideoStreamException: {videoStreamException}")

    def cleanup(self) -> None:
        """Method for cleaning up resources."""
        try:
            # Release any resources
            print("Cleaning up resources...")
            self.drone.end()
            self.root.quit()  # Quit the Tkinter main loop
            exit()
        except Exception as e:
            print(f"Error performing cleanup: {e}")


if __name__ == "__main__":
    # Initialize the GUI
    gui = GameControllerGUI()

    # Call the run_app method to run tkinter mainloop
    gui.run_app()

