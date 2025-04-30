# Core image conversion logic using potrace
import subprocess
import os
import logging
from PIL import Image
import tempfile
from typing import Tuple, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ConversionConfig:
    """Configuration for image conversion process."""
    def __init__(self):
        self.turdsize = 2  # Suppress speckles of this size
        self.alphamax = 1.34  # Corner threshold parameter
        self.opttolerance = 0.2  # Curve optimization tolerance
        self.optimize = True  # Whether to optimize the output SVG

def convert_image_to_svg_potrace(
    input_path: str,
    output_path: str,
    config: Optional[ConversionConfig] = None
) -> Tuple[bool, Optional[str]]:
    """Converts a raster image (JPG, PNG) to SVG using potrace CLI.

    Args:
        input_path (str): Path to the input image file.
        output_path (str): Path where the SVG file should be saved.
        config (ConversionConfig, optional): Configuration for the conversion process.

    Returns:
        Tuple[bool, Optional[str]]: (success, error_message)
            - success: True if conversion was successful, False otherwise
            - error_message: Error message if conversion failed, None otherwise
    """
    if config is None:
        config = ConversionConfig()

    temp_bmp_file = None
    try:
        logger.info(f"Starting conversion of {input_path} to {output_path}")
        
        # Validate input file
        if not os.path.exists(input_path):
            return False, f"Input file not found: {input_path}"
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        # Preprocess image
        try:
            img = Image.open(input_path)
            if img.mode != 'L':
                img = img.convert("L")
            logger.info(f"Image loaded successfully: {img.size[0]}x{img.size[1]} pixels")
        except Exception as e:
            return False, f"Failed to process input image: {str(e)}"

        # Create temporary BMP file
        with tempfile.NamedTemporaryFile(suffix=".bmp", delete=False) as temp_file:
            temp_bmp_file = temp_file.name
            img.save(temp_bmp_file)
            logger.info("Temporary BMP file created successfully")

        # Construct potrace command with configuration
        command = [
            "potrace",
            temp_bmp_file,
            "-s",  # Output SVG
            "-o", output_path,
            "--turdsize", str(config.turdsize),
            "--alphamax", str(config.alphamax),
            "--opttolerance", str(config.opttolerance)
        ]
        
        if config.optimize:
            command.append("--optimize")

        logger.info(f"Executing potrace command: {' '.join(command)}")
        
        # Execute potrace command
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )

        # Verify output
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            logger.info(f"Conversion successful. Output file size: {file_size} bytes")
            return True, None
        else:
            error_message = f"potrace command executed but output file not found. Stderr: {result.stderr}"
            logger.error(error_message)
            return False, error_message

    except subprocess.CalledProcessError as e:
        error_message = f"potrace failed: {e.stderr}"
        logger.error(error_message)
        return False, error_message
    except FileNotFoundError:
        error_message = "potrace command not found. Make sure it is installed and in PATH."
        logger.error(error_message)
        return False, error_message
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        logger.error(error_message)
        return False, error_message
    finally:
        # Clean up temporary file
        if temp_bmp_file and os.path.exists(temp_bmp_file):
            try:
                os.remove(temp_bmp_file)
                logger.info("Temporary file cleaned up successfully")
            except Exception as e:
                logger.warning(f"Failed to clean up temporary file: {str(e)}")

# Update the main GUI script to import this new function name
# (Need to modify image_converter_gui.py later)

