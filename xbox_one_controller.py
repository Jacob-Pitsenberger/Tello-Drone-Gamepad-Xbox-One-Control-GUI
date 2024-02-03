"""
Author: Jacob Pitsenberger
date: 1/30/24
Description:
    This module contains the XboxController class used for receiving inputs from an Xbox one game controller,
    normalizing the values returned from the joystick input and filtering any low values from these to exclude
    noise.
"""
import time
from inputs import get_gamepad
import math
import threading


class XboxController(object):
    # Max values for normalizing
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):
        """Initialize all input values to zero then create and start a thread to call the method
           for monitoring the controller for inputs."""

        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def read(self):
        """Return the current input values from the controller as a list."""
        return [
            self.LeftJoystickX,
            self.LeftJoystickY,
            self.RightJoystickX,
            self.RightJoystickY,
            self.LeftTrigger,
            self.RightTrigger,
            self.LeftBumper,
            self.RightBumper,
            self.A,
            self.X,
            self.Y,
            self.B,
            self.LeftThumb,
            self.RightThumb,
            self.Back,
            self.Start,
            self.LeftDPad,
            self.RightDPad,
            self.UpDPad,
            self.DownDPad
        ]

    @staticmethod
    def _normalize(value):
        """This static method is used to normalize the read joystick inputs such that can hold values in the
           range [-100, 100]"""
        # Normalize a value from the range [0, max_value] to [-100, 100]
        return int((value / XboxController.MAX_JOY_VAL) * 100)

    @staticmethod
    def _filter_noise(value):
        """This static method is in essence a debouncing method similar to those used for buttons in electronics
           Through experimentation, noise from joystick was found to be in the range of 0-15 so filter out these
           values by returning any less than the maximum of 15 as zero."""
        if abs(value) <= 15:
            filtered_value = 0
        else:
            filtered_value = value
        return filtered_value

    def _monitor_controller(self):
        """Execute an infinite loop that checks the controller (gamepad) for events and updates the XboxController
           classes input values to the event state for each respective button/input sensors event code."""
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    print(f"To get max values for normalizing, print the left joystick y before normalizing giving:\nvalue = {event.state}")
                    self.LeftJoystickY = self._filter_noise(self._normalize(event.state))
                elif event.code == 'ABS_X':
                    self.LeftJoystickX = self._filter_noise(self._normalize(event.state))
                elif event.code == 'ABS_RY':
                    self.RightJoystickY = self._filter_noise(self._normalize(event.state))
                elif event.code == 'ABS_RX':
                    self.RightJoystickX = self._filter_noise(self._normalize(event.state))
                elif event.code == 'ABS_Z':
                    self.LeftTrigger = self._filter_noise(self._normalize(event.state))
                elif event.code == 'ABS_RZ':
                    self.RightTrigger = self._filter_noise(self._normalize(event.state))
                elif event.code == 'BTN_START':
                    self.Start = event.state
                elif event.code == 'BTN_TL':
                    self.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    self.RightBumper = event.state
                elif event.code == 'BTN_SOUTH':
                    self.A = event.state
                elif event.code == 'BTN_NORTH':
                    self.Y = event.state
                elif event.code == 'BTN_WEST':
                    self.X = event.state
                elif event.code == 'BTN_EAST':
                    self.B = event.state
                elif event.code == 'BTN_THUMBL':
                    self.LeftThumb = event.state
                elif event.code == 'BTN_THUMBR':
                    self.RightThumb = event.state
                elif event.code == 'BTN_SELECT':
                    self.Back = event.state
                elif event.code == 'BTN_START':
                    self.Start = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY1':
                    self.LeftDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY2':
                    self.RightDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY3':
                    self.UpDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY4':
                    self.DownDPad = event.state


if __name__ == '__main__':
    """Main method for analyzing the class and debugging its usage."""
    # Initialize class
    joy = XboxController()
    # Run a loop to read input from the controller until the program is terminated.
    while True:
        # Get a list of controller values in real-time by calling read()
        controller_values = joy.read()
        """
        # Access the start button from the list returned from read()
        start_button = controller_values[14]
            
        ### HERE IS HOW I FOUND THE PERFECT DELAY TO USE WHEN THE START BUTTON IS PRESSED ###
        print(f"start button before sleeping")
        if start_button:
            print(start_button)
            time.sleep(0.15)
        print("after sleeping")

        # Access controller values by their index in the list returned from read().
        left_joy_x = controller_values[0]
        left_joy_y = controller_values[1]
        right_joy_x = controller_values[2]
        right_joy_y = controller_values[3]
        # print(f"Left y = {left_joy_y}, Left x = {left_joy_x}")
        # print(f"Right y = {right_joy_y}, Right x = {right_joy_x}")

        """
