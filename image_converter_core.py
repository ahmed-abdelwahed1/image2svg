# Core image conversion logic using potrace
import subprocess
import os
from PIL import Image
import tempfile

def convert_image_to_svg_potrace(input_path, output_path):
    """Converts a raster image (JPG, PNG) to SVG using potrace CLI.

    Args:
        input_path (str): Path to the input image file.
        output_path (str): Path where the SVG file should be saved.

    Returns:
        bool: True if conversion was successful, False otherwise.
        str: Error message if conversion failed, None otherwise.
    """
    temp_bmp_file = None
    try:
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        # 1. Preprocess image using Pillow and save as temporary BMP
        # potrace works best with black and white images. We can threshold.
        # For simplicity here, let's convert to grayscale first.
        # A more advanced approach might involve color quantization and multiple potrace runs.
        img = Image.open(input_path).convert("L") # Convert to grayscale

        # Create a temporary file for the BMP intermediate
        with tempfile.NamedTemporaryFile(suffix=".bmp", delete=False) as temp_file:
            temp_bmp_file = temp_file.name
            img.save(temp_bmp_file)

        # 2. Construct the potrace command
        # Using -s for SVG output. Other options can be added.
        command = [
            "potrace",
            temp_bmp_file,
            "-s", # Output SVG
            "-o", output_path,
            # Add other potrace options here if needed, e.g.:
            # "--turdsize", "2", # Suppress speckles of this size
            # "--alphamax", "1.34" # Corner threshold parameter
        ]

        # 3. Execute the potrace command
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        # Check if the output file was created
        if os.path.exists(output_path):
            return True, None
        else:
            error_message = f"potrace command executed but output file not found. Stderr: {result.stderr}"
            return False, error_message

    except subprocess.CalledProcessError as e:
        error_message = f"potrace failed: {e.stderr}"
        return False, error_message
    except FileNotFoundError:
        error_message = "potrace command not found. Make sure it is installed and in PATH."
        return False, error_message
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        return False, error_message
    finally:
        # Clean up the temporary BMP file
        if temp_bmp_file and os.path.exists(temp_bmp_file):
            os.remove(temp_bmp_file)

# Update the main GUI script to import this new function name
# (Need to modify image_converter_gui.py later)

