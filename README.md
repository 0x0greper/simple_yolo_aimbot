# Simple YOLO Aimbot PoC for AssaultCube 1.2

![Logo](logo.png)

This is a proof-of-concept aimbot for **AssaultCube 1.2**, specifically designed to work on systems with NVIDIA GPUs. The project also includes additional scripts to help you train your own YOLO model. Have fun, and enjoy exploring the possibilities! 😎🎮

# Installation:
1. Install Python:
Ensure you have Python 3.11.9 installed. This version has been tested for compatibility with the aimbot.

2. Clone the Repository:
Download the project files using Git:

```git clone https://github.com/0x0greper/simple_yolo_aimbot.git```

3. Ensure NVIDIA Drivers Are Installed:
Verify that your NVIDIA GPU drivers are up to date.

4. Install CUDA Toolkit 12.4:
This aimbot is designed to work with CUDA 12.4. Download and install it from the official NVIDIA CUDA 12.4 archive. Be sure you grab the correct version. ```https://developer.nvidia.com/cuda-12-4-0-download-archive```

```nvcc --version```
Use this command to confirm the correct CUDA version is installed.

5. Install Required Libraries:
Once CUDA is set up, install the dependencies listed in requirements.txt by running:

```pip install -r requirements.txt```

6. Install the Correct Version of PyTorch:
Uninstall any previously installed versions of PyTorch to avoid conflicts:

```pip uninstall torch torchvision torchaudio```

Then, install the compatible PyTorch version for CUDA 12.4:

```pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118```

7. Verify PyTorch Installation:
Check if the correct version of PyTorch has been installed and confirm that your GPU is detected:


```import torch```
```print(torch.__version__)```
```print(torch.cuda.is_available())```

You should see output that confirms PyTorch is usingthe correct version and that it is using CUDA.

8. Download and Install AssaultCube 1.2:
Get the correct version of AssaultCube 1.2 from the official release page.

```https://github.com/assaultcube/AC/releases/tag/v1.2.0.0```

10. Set Up AssaultCube:
Run AssaultCube.
Go to the video settings and disable fullscreen mode.
Resize the game window so it’s about half the size of your monitor. This is necessary to view the AI-generated overlay on a secondary window.

#Usage:
**Detection Mode:**
To run the real-time detection of in-game objects, execute the detect.py script while AssaultCube is running. A secondary window will appear, displaying a mirror of the game with AI-generated bounding boxes overlaying detected objects.

**Aimbot Mode:**
To activate the aimbot, run aimbot.py while AssaultCube is running. A secondary window will display the AI’s object detection overlay. While playing, simply press the "q" key repeatedly to lock your crosshairs onto the enemy’s head. Enjoy your headshots! 😉

