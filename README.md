# Image to SVG Converter

This Python program converts raster images (JPG, PNG) into Scalable Vector Graphics (SVG) format using a simple graphical user interface (GUI).

## Features

*   Converts JPG and PNG files to SVG.
*   Uses `potrace` for bitmap tracing to generate vector shapes. Images are preprocessed (converted to grayscale) using `Pillow`.
*   Simple and user-friendly interface built with Tkinter.
*   Supports selecting single or multiple input files.
*   Allows users to choose an output directory for the converted SVG files.
*   Provides progress feedback during conversion.
*   Displays clear status and error messages.
*   Runs conversion in a separate thread to keep the GUI responsive.

## Dependencies

The program requires the following dependencies to be installed:

*   **Python 3:** The core programming language.
*   **Tkinter:** Usually included with standard Python installations. If not, it might need to be installed separately (e.g., `sudo apt-get install python3-tk` on Debian/Ubuntu).
*   **Pillow:** Python Imaging Library fork for image preprocessing.
    ```bash
    pip3 install Pillow
    ```
*   **potrace:** A command-line tool for tracing bitmaps.
    ```bash
    # On Debian/Ubuntu:
    sudo apt-get update
    sudo apt-get install potrace

    # On macOS (using Homebrew):
    brew install potrace

    # On Windows:
    # Download from http://potrace.sourceforge.net/#downloading
    # Ensure the potrace.exe is in your system's PATH.
    ```

## Files

*   `image_converter_core.py`: Contains the core logic for image conversion using `potrace`.
*   `image_converter_gui.py`: Implements the Tkinter-based graphical user interface.
*   `README.md`: This file.

## How to Run

1.  **Ensure all dependencies are installed** (Python 3, Tkinter, Pillow, potrace).
2.  **Save the provided Python files** (`image_converter_core.py` and `image_converter_gui.py`) in the same directory.
3.  **Open a terminal or command prompt**, navigate to the directory where you saved the files.
4.  **Run the GUI script** using Python:
    ```bash
    python3 image_converter_gui.py
    ```
5.  **Use the application:**
    *   Click "Select Files" to choose one or more JPG/PNG images.
    *   Click "Select Directory" to choose where the output SVG files will be saved.
    *   Click "Convert to SVG" to start the conversion process.
    *   Monitor the progress bar and status messages for feedback.

## Notes

*   The current conversion process uses `potrace` on a grayscale version of the input image. This is effective for line art and shapes but will not preserve original colors directly in the SVG. For color vectorization, more complex techniques or different tools (like the initially attempted `vtracer`, if it can be made to work in your environment) would be needed.
*   Error handling is included for unsupported file types and conversion failures.

