from image_converter_core import convert_image_to_svg_potrace
import os

input_file = "/home/ubuntu/test_input.png"
output_file = "/home/ubuntu/test_output.svg"

print(f"Attempting to convert {input_file} to {output_file}...")
success, error = convert_image_to_svg_potrace(input_file, output_file)

if success:
    print(f"Successfully converted {input_file} to {output_file}")
    # Optionally, print the first few lines of the SVG file
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            print("\n--- Start of SVG content ---")
            for i, line in enumerate(f):
                if i >= 5:
                    break
                print(line.strip())
            print("--- End of SVG preview ---")
else:
    print(f"Conversion failed: {error}")

