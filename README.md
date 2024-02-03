# Tello Drone Gamepad (Xbox One) Control GUI

## Overview

This project provides a Python-based [interface](GUI.py) for controlling and capturing video from a Tello drone. 
It uses the `djitellopy` library to establish a connection with the drone, `opencv-python` and `Pillow` for video processing/display, 
and the `inputs` library to capture input from a [game controller](xbox_one_controller.py).

### Notes
This project was created using [this](https://github.com/Jacob-Pitsenberger/Tkinter-Tello-Drone-Controller/blob/master/tkinter_keyboard_controller.py) 
repository module as a template for the [GUI](GUI.py) and adjusting it to work with a 
[XboxController](xbox_one_controller.py) class adapted from this [source](https://stackoverflow.com/questions/46506850/how-can-i-get-input-from-an-xbox-one-controller-in-python) 
found through performing a Google search on how to receive input from an xbox controller using python.

Please note that this class required some adjustments to work with my xbox one controller such that the 
key event were correctly defined for the proper button they represent in code.

Also note that while this code works as it is intended to, I did have to change some joystick assignments.
For example, the left and right joysticks x and y values were opposite so left joystick x was actually y
and etcetera until I changed them here. If you find issues try experimenting with this module and your
controller until you are sure that the correct buttons and event keys are outputting the correct values
for the button/event key we define them as here.

## Installation

To run this project, you need to have Python installed on your machine. 
This project was developed with Python 3.10, but it should work with any Python version above 3.6.

### Setting Up a Virtual Environment (Optional)

It's recommended to set up a virtual environment to avoid any conflicts with other Python packages you might have installed. You can create a virtual environment using the following command:

```bash
python -m venv venv
```

Activate the virtual environment with:

- On Windows:

```bash
.\venv\Scripts\activate
```

- On macOS and Linux:

```bash
source venv/bin/activate
```

### Installing Dependencies

Once your virtual environment is activated, you can install the required dependencies by running:

```bash
pip install -r requirements.txt
```

The [requirements.txt](requirements.txt) file includes the following libraries:

- opencv-python~=4.9.0.80: For video capture and image processing.
- djitellopy~=2.4.0: Python interface for the Tello drone.
- Pillow~=8.4.0: For image processing tasks.
- inputs~=0.5: For capturing input from game controllers.

## Usage

After installing all dependencies, you can run the [main script](GUI.py) to start controlling your Tello drone. 
Ensure your Tello drone is powered on and connected to your computer's Wi-Fi network.

```bash
python GUI.py
```

Make sure you have a compatible game controller connected to your computer. The script maps specific controller buttons and joysticks to drone movements and actions.

## Future Enhancements:

- Add different functionalities and enable them to be executed through use of other controller buttons.

## Contributing

Feel free to fork this project and contribute. 
If you find a bug or have a feature request, please open an issue.

## Author
[Jacob Pitsenberger](https://github.com/Jacob-Pitsenberger)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.