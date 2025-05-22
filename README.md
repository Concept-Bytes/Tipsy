# Tipsy the AI Cocktail Maker Project

This project is a multi-part cocktail maker system designed to run on a Raspberry Pi. It integrates three separate modules:

1. **Streamlit App (app.py):**  
   Allows users to configure pump settings, generate cocktail recipes (using an OpenAI API), and view a recipe book with cocktail images and details.

2. **Pygame Interface (interface.py):**  
   Provides a full-screen, swipeable interface for cocktail selection. The interface displays a background image (`tipsy.png`), overlays the selected cocktail logo, and includes extra interactive logos (`single.png` and `double.png`) to select drink mode (single or double). It features various animations such as text zoom and logo pop effects, and displays pouring/loading overlays.

3. **Pump Controller (controller.py):**  
   Reads the selected cocktail and pump configuration (from `cocktails.json` and `pump_config.json`), then controls 12 pumps via the Raspberry Pi GPIO (using L91105 motor drivers) to mix the drink. The controller uses a mapping of ingredients to pump pins.

4. **Main Launcher (main.py) (optional):**  
   A helper script to launch both the Streamlit app and Pygame interface concurrently.

---

## Features

- **Cocktail Recipe Generation:**  
  Generates cocktail recipes (via OpenAI API) based on pump configuration and bartender requests.

- **Swipe & Mode Selection Interface:**  
  Use touch/mouse swipe gestures to navigate cocktail logos. Tap the extra logos (`single.png` and `double.png`) to select drink mode, triggering animations and overlays.

- **Pump Control:**  
  Uses Raspberry Pi GPIO and L91105 motor drivers to run pumps based on the selected cocktail’s ingredients.

- **Configurable Pump Setup:**  
  Pump-to-ingredient mapping is stored in `pump_config.json`.

- **Persistent API Key:**  
  The Streamlit app prompts for an OpenAI API key (if not found in a `.env` file) and saves it for future use.

---

## Hardware Requirements

- **Raspberry Pi (any recent model)**  
- **L91105 Motor Drivers** for each pump  
- **12 Pumps** connected to the L91105 boards, with the following GPIO pin configuration:

  | Pump    | IA Pin | IB Pin |
  |---------|--------|--------|
  | Pump 1  | GPIO17 | GPIO4  |
  | Pump 2  | GPIO22 | GPIO27 |
  | Pump 3  | GPIO10 | GPIO9  |
  | Pump 4  | GPIO5  | GPIO11 |
  | Pump 5  | GPIO13 | GPIO6  |
  | Pump 6  | GPIO26 | GPIO19 |
  | Pump 7  | GPIO20 | GPIO21 |
  | Pump 8  | GPIO12 | GPIO16 |
  | Pump 9  | GPIO8  | GPIO7  |
  | Pump 10 | GPIO24 | GPIO25 |
  | Pump 11 | GPIO18 | GPIO23 |
  | Pump 12 | GPIO14 | GPIO15 |

- **Touchscreen or Mouse** for interacting with the Pygame interface

### PCB Files

The project includes custom PCB designs for the pump controller circuitry. These files are located in the `/PCB Board Production` folder and contain everything needed for fabrication:
- **Gerber Files:** All layers required for manufacturing the PCB.
- **Bill of Materials (BOM):** A complete list of components.
- **Component Position Files:** Placement and assembly details.

You can send these files directly to a PCB manufacturer (such as JLCPCB) to have the custom boards produced.

---

## Software Dependencies

- **Python 3.x**
- **Streamlit**  
  `pip install streamlit`
- **Pygame**  
  `pip install pygame`
- **RPi.GPIO** (or similar, for Raspberry Pi GPIO control)  
  `pip install RPi.GPIO`
- **python-dotenv**  
  `pip install python-dotenv`
- **Requests**  
  `pip install requests`
- **OpenAI Python Library**  
  `pip install openai`
- **Pydantic**  
  `pip install pydantic`
  Requires `numpy<2.0`; on Raspberry Pi 4 (64‑bit) only supported on OS kernel versions ≤6.6.51. Avoid mass‑upgrading numpy or other system software without verifying compatibility.

 
 > **Note on ONNX Runtime Compatibility:** This project uses `rembg` for background removal (via ONNX Runtime). ONNX Runtime requires `numpy<2.0`, and on Raspberry Pi 4 (64‑bit) only supports OS kernel versions ≤6.6.51. Avoid mass‑upgrading numpy, the OS kernel, or other system packages without verifying compatibility.

---

## Installation & Setup

1. **Clone the Repository:**  
   ```bash
   git clone https://github.com/Concept-Bytes/Tipsy
   cd Tipsy
   ```

2. **Install Dependencies:**  
   ```bash
   pip install -r requirements.txt
   ```
   *(Alternatively, install the packages listed above individually.)*

3. **Configure GPIO & Hardware:**  
   Wire your pumps to the Raspberry Pi as per the pin mapping provided above. Ensure your L91105 drivers and pumps are correctly connected.

4. **Set Up API Key:**  
   When running the Streamlit app (app.py), you will be prompted to enter your OpenAI API key. This key will be saved to a `.env` file for future use.

5. **Prepare JSON Files:**  
   - Edit `pump_config.json` to map pumps to your desired ingredients.  
   - Generate cocktail recipes via the Streamlit interface (app.py) to create/update `cocktails.json`.

6. **Place Image Assets:**  
   - Ensure `tipsy.png` is in the project root.  
   - Place your cocktail logo images in the `drink_logos` folder.  
   - Ensure `single.png`, `double.png`, `pouring.png`, and `loading.png` are in the project root (or adjust paths accordingly).

7. **PCB Board Production Files:** 
   Check the `/PCB Board Production` folder for Gerber files, BOM, and component placement files required for PCB manufacturing. Send these files to your chosen PCB manufacturer (e.g., JLCPCB).
   ![PCB Screenshot](./board.jpg)
---

## Running the Project

### Option 1: Launch Separately
- **Streamlit App:**  
  ```bash
  streamlit run app.py
  ```
- **Pygame Interface:**  
  ```bash
  python interface.py
  ```
- **Controller:**  
  After selecting a cocktail and mode, run the controller on the Raspberry Pi:  
  ```bash
  python controller.py
  ```

### Option 2: Launch Together Using Main Launcher
- **Main Launcher (main.py):**  
  ```bash
  python main.py
  ```
  This script launches both the Streamlit app and the Pygame interface concurrently. (You can run the controller separately when ready.)

---

## Controller Operation

The `controller.py` script will:
1. Read `pump_config.json` and `cocktails.json`.
2. Determine which cocktail is selected by reading `selected_cocktail.txt`.
3. Determine the drink mode (single or double) by reading `selected_mode.txt`.
4. Activate the appropriate pumps via GPIO for the required duration based on the cocktail recipe.  
*Adjust the conversion factor (seconds per ounce) in `controller.py` to suit your pump flow rate.*

---

## Configuration Options

Several settings can be configured via environment variables, or in a .env file.
* OPENAI_API_KEY: Your API key for OpenAI. This is set when you first run the streamlit app.
* DEBUG: Set to 'true' to enable debug logging and disable motor control
* OZ_COEFFICIENT: The number of seconds required for your pumps to pour 1oz of liquid.
* INVERT_PUMP_PINS: Set to 'true' to invert the direction of your pumps.
* PUMP_CONCURRENCY: The number of pumps that should run simultaneously.
* FULL_SCREEN: Set to 'false' to disable full screen mode for the PyGame interface. Useful for debugging.
* SHOW_RELOAD_COCKTAILS_BUTTON: Set to 'true' to show a reload button for manually reloading the list of cocktails
* RELOAD_COCKTAILS_TIMEOUT: Set to a number of milliseconds to automatically reload the list of cocktails that often.
* RETRACTION_TIME: Set to a number of seconds to reverse the motors at the end of a pour. This should help prevent buildup on the ends of the tubing.
* USE_GPT_TRANSPARENCY: Set to 'true' to enable native image transparency in OpenAI. This should produce more consistent image results. This uses the `gpt-image-1` model. Your organization must be verified to use the model `gpt-image-1`. Please go to: https://platform.openai.com/settings/organization/general and click on Verify Organization. If you just verified, it can take up to 15 minutes for access to propagate.
* COCKTAIL_IMAGE_SCALE: The size (as a decimal, ie. 0.75 for 75%) you want to scale the cocktail images to, relative to the screen size. Defaults to 1.0, or full screen.

---

## Troubleshooting

- **GPIO Issues:**  
  Ensure that your wiring matches the pin mappings in `controller.py` and that your Raspberry Pi user has permissions to access GPIO.

- **Image Loading Errors:**  
  Verify that all image files (`tipsy.png`, `pouring.png`, `loading.png`, logos, etc.) are present and paths are correct.

- **API Key Issues:**  
  If the API key prompt appears on every run, ensure the `.env` file is being written to and that you have appropriate write permissions.

- **Dependency Errors:**  
  Check that all Python dependencies are installed correctly. Use `pip freeze` to verify.

---

## License

*Include your project license here (e.g., MIT License).*

---

## Acknowledgments

*Mention any libraries, tutorials, or contributors that helped build this project.*
