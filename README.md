# README - Fishing Bot

## Overview

The **Fishing Bot** automates the fishing process in wow combining screen capture, audio detection, and automated mouse movements.

## Components

### `main.py`

This is the main script that initializes and controls the bot.

- **Functions:**
  - Initializes the `MainAgent`, the central controller.
  - Creates instances of `ScreenAgent`, `AudioAgent`, and `FishingAgent`.
  - Starts the `ScreenAgent` for continuous screen capture.
  - Handles user input to start fishing or quit the program.
  - Manages the proper start and stop of all agents.

### `audio_agent.py` (AudioAgent)

Handles audio detection to determine when a fish bites.

- **Functions:**
  - Loads the reference audio sample (`bitesound.wav`) representing a fish bite.
  - Opens an audio stream to listen for incoming audio signals.
  - Compares incoming audio in real-time with the reference sample.
  - Notifies the `FishingAgent` when a bite is detected.

### `screen_agent.py` (ScreenAgent)

Captures and provides screen images for processing.

- **Functions:**
  - Continuously captures screenshots of the primary monitor.
  - Provides current screen images to other agents.
  - Assists the `FishingAgent` in visual detection of objects (e.g., the bobber).

### `fishing_agent.py` (FishingAgent)

Controls the fishing process.

- **Functions:**
  - Casts the fishing line by simulating a key press (`cast_lure()`).
  - Searches the screen for the bobber using image processing (`find_lure()`).
  - Moves the mouse cursor to the bobber (`move_to_lure()`).
  - Uses the `AudioAgent` to detect when a fish bites (`listen_for_bite()`).
  - Reels in the line once a bite is detected.

## Requirements

- **Python 3.x**
- **Dependencies:** Install required packages:

  ```bash
  pip install -r requirements.txt
  ```

- **Additional Requirements:**
  - A working microphone or access to the game's audio output.
  - Appropriate screen resolution and game graphics settings for image processing.

## Installation and Execution

1. **Clone or download the repository.**
2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the program:**

   ```bash
   python main.py
   ```

4. **Follow the terminal instructions:**
   - Press `F` to start fishing.
   - Press `Q` to quit the program.

## Notes

- **Audio Settings:** Make sure the correct recording device is selected and volume levels are appropriate.
- **Image Processing:** Bobber detection success may vary based on lighting and screen resolution.
- **Troubleshooting:**
  - If imports fail, check for `__init__.py` files and correct module paths.
  - Avoid blocking operations in the `__init__` methods of the agents.

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

## Contact

For questions or suggestions, contact the development team.



# fishersfritze
# fishersfritze
