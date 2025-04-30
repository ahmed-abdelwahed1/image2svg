# Image to SVG Converter

A professional desktop application for converting raster images (JPG, PNG) to SVG format using the powerful potrace algorithm.

## Features

- Convert multiple images to SVG format in batch
- Modern and intuitive user interface
- Support for JPG and PNG input formats
- SVG optimization options
- Progress tracking and detailed error reporting
- Professional logging system

## Requirements

- Python 3.6 or higher
- potrace (must be installed and available in system PATH)
- Required Python packages:
  - Pillow (PIL)
  - tkinter (usually comes with Python)

## Installation

1. Ensure you have Python 3.6+ installed on your system
2. Install potrace:
   - Windows: Download and install from [potrace website](http://potrace.sourceforge.net/)
   - Linux: `sudo apt-get install potrace`
   - macOS: `brew install potrace`

3. Install required Python packages:

   ```bash
   pip install Pillow
   ```

4. Clone or download this repository

## Usage

1. Run the application:

   ```bash
   python image_converter_gui.py
   ```

2. Using the application:
   - Click "Select Files" to choose input images (JPG/PNG)
   - Click "Select Directory" to choose output location
   - (Optional) Configure conversion options
   - Click "Convert to SVG" to start the conversion

## Conversion Options

- **Optimize SVG output**: When enabled, the generated SVG files will be optimized for size and performance

## Error Handling

The application provides detailed error messages for:

- Invalid file formats
- Conversion failures
- System errors
- Missing dependencies

All errors are logged for debugging purposes.

## Logging

The application maintains detailed logs of all operations. Logs include:

- File selection
- Conversion progress
- Success/failure status
- Error details
- Configuration changes

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [potrace](http://potrace.sourceforge.net/) for the vectorization algorithm
- [Pillow](https://python-pillow.org/) for image processing
- [tkinter](https://docs.python.org/3/library/tkinter.html) for the GUI framework
