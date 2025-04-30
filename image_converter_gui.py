import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading
import logging
from image_converter_core import convert_image_to_svg_potrace, ConversionConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to SVG Converter")
        self.root.geometry("600x500")
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure("Custom.TButton", padding=6)
        self.style.configure("Custom.TLabel", padding=2)
        self.style.configure("Custom.TFrame", background="#f0f0f0")
        self.style.configure("Custom.TCheckbutton", padding=2)
        
        # Set theme colors
        self.bg_color = "#f0f0f0"
        self.accent_color = "#2196F3"
        self.text_color = "#333333"
        
        self.root.configure(bg=self.bg_color)
        
        self.input_files = []
        self.output_dir = ""
        self.conversion_config = ConversionConfig()

        # Main container with padding
        self.main_container = ttk.Frame(root, style="Custom.TFrame", padding="20")
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Title
        self.title_label = ttk.Label(
            self.main_container,
            text="Image to SVG Converter",
            font=("Helvetica", 16, "bold"),
            foreground=self.text_color
        )
        self.title_label.pack(pady=(0, 20))

        # Input Files Section
        self.input_frame = ttk.Frame(self.main_container, style="Custom.TFrame")
        self.input_frame.pack(fill=tk.X, pady=(0, 15))

        self.input_label = ttk.Label(
            self.input_frame,
            text="Input Files",
            font=("Helvetica", 10, "bold"),
            foreground=self.text_color
        )
        self.input_label.pack(side=tk.LEFT)

        self.select_files_button = ttk.Button(
            self.input_frame,
            text="Select Files",
            command=self.select_input_files,
            style="Custom.TButton"
        )
        self.select_files_button.pack(side=tk.RIGHT)

        # File list with custom styling
        self.file_listbox = tk.Listbox(
            self.main_container,
            selectmode=tk.EXTENDED,
            height=5,
            font=("Helvetica", 9),
            bg="white",
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground="#cccccc"
        )
        self.file_listbox.pack(fill=tk.X, pady=(0, 15))

        # Output Directory Section
        self.output_frame = ttk.Frame(self.main_container, style="Custom.TFrame")
        self.output_frame.pack(fill=tk.X, pady=(0, 15))

        self.output_label = ttk.Label(
            self.output_frame,
            text="Output Directory",
            font=("Helvetica", 10, "bold"),
            foreground=self.text_color
        )
        self.output_label.pack(side=tk.LEFT)

        self.select_output_button = ttk.Button(
            self.output_frame,
            text="Select Directory",
            command=self.select_output_directory,
            style="Custom.TButton"
        )
        self.select_output_button.pack(side=tk.RIGHT)

        self.output_path_label = ttk.Label(
            self.main_container,
            text="No directory selected",
            font=("Helvetica", 9),
            foreground="#666666",
            background="white",
            padding=5
        )
        self.output_path_label.pack(fill=tk.X, pady=(0, 20))

        # Conversion Options Section
        self.options_frame = ttk.LabelFrame(
            self.main_container,
            text="Conversion Options",
            padding="10",
            style="Custom.TFrame"
        )
        self.options_frame.pack(fill=tk.X, pady=(0, 15))

        # Optimize SVG checkbox
        self.optimize_var = tk.BooleanVar(value=True)
        self.optimize_check = ttk.Checkbutton(
            self.options_frame,
            text="Optimize SVG output",
            variable=self.optimize_var,
            style="Custom.TCheckbutton",
            command=self.update_config
        )
        self.optimize_check.pack(anchor=tk.W, pady=2)

        # Progress Section
        self.progress_frame = ttk.Frame(self.main_container, style="Custom.TFrame")
        self.progress_frame.pack(fill=tk.X, pady=(0, 15))

        self.progress_label = ttk.Label(
            self.progress_frame,
            text="Progress",
            font=("Helvetica", 10, "bold"),
            foreground=self.text_color
        )
        self.progress_label.pack(side=tk.LEFT)

        self.progress_bar = ttk.Progressbar(
            self.main_container,
            orient="horizontal",
            length=400,
            mode="determinate",
            style="Custom.Horizontal.TProgressbar"
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 15))

        # Status Label
        self.status_label = ttk.Label(
            self.main_container,
            text="Ready",
            font=("Helvetica", 9),
            foreground="#666666",
            background="white",
            padding=5
        )
        self.status_label.pack(fill=tk.X, pady=(0, 20))

        # Convert Button
        self.convert_button = ttk.Button(
            self.main_container,
            text="Convert to SVG",
            command=self.start_conversion_thread,
            state=tk.DISABLED,
            style="Custom.TButton"
        )
        self.convert_button.pack(pady=(0, 10))

    def update_config(self):
        """Update conversion configuration based on UI settings."""
        self.conversion_config.optimize = self.optimize_var.get()
        logger.info(f"Updated conversion config: optimize={self.conversion_config.optimize}")

    def select_input_files(self):
        files = filedialog.askopenfilenames(
            title="Select Input Images",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png"), ("All Files", "*.*")]
        )
        if files:
            self.input_files = list(files)
            self.file_listbox.delete(0, tk.END)
            for f in self.input_files:
                self.file_listbox.insert(tk.END, os.path.basename(f))
            self.update_convert_button_state()
            self.status_label.config(text=f"{len(self.input_files)} file(s) selected.")
            logger.info(f"Selected {len(self.input_files)} input files")

    def select_output_directory(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir = directory
            self.output_path_label.config(text=self.output_dir)
            self.update_convert_button_state()
            self.status_label.config(text=f"Output directory set to: {self.output_dir}")
            logger.info(f"Selected output directory: {self.output_dir}")

    def update_convert_button_state(self):
        if self.input_files and self.output_dir:
            self.convert_button.config(state=tk.NORMAL)
        else:
            self.convert_button.config(state=tk.DISABLED)

    def start_conversion_thread(self):
        self.convert_button.config(state=tk.DISABLED)
        self.select_files_button.config(state=tk.DISABLED)
        self.select_output_button.config(state=tk.DISABLED)
        self.progress_bar["value"] = 0
        self.progress_bar["maximum"] = len(self.input_files)
        self.status_label.config(text="Starting conversion...")
        logger.info("Starting conversion process")

        conversion_thread = threading.Thread(target=self.run_conversion, daemon=True)
        conversion_thread.start()

    def run_conversion(self):
        successful_conversions = 0
        failed_conversions = 0

        for i, input_file in enumerate(self.input_files):
            base_name = os.path.splitext(os.path.basename(input_file))[0]
            output_file = os.path.join(self.output_dir, f"{base_name}.svg")
            self.status_label.config(text=f"Converting {os.path.basename(input_file)}...")
            logger.info(f"Converting file {i+1}/{len(self.input_files)}: {input_file}")

            try:
                ext = os.path.splitext(input_file)[1].lower()
                if ext not in [".jpg", ".jpeg", ".png"]:
                    messagebox.showerror(
                        "Invalid File Format",
                        f"The file '{os.path.basename(input_file)}' is not supported.\n\n"
                        "Please select a JPG or PNG image file.",
                        icon="error"
                    )
                    failed_conversions += 1
                    self.progress_bar["value"] = i + 1
                    continue

                success, error_msg = convert_image_to_svg_potrace(
                    input_file,
                    output_file,
                    self.conversion_config
                )

                if success:
                    successful_conversions += 1
                    self.status_label.config(text=f"Successfully converted {os.path.basename(input_file)}")
                    logger.info(f"Successfully converted: {input_file}")
                else:
                    failed_conversions += 1
                    self.status_label.config(text=f"Failed to convert {os.path.basename(input_file)}")
                    messagebox.showerror(
                        "Conversion Failed",
                        f"Unable to convert '{os.path.basename(input_file)}'.\n\n"
                        f"Error: {error_msg}\n\n"
                        "Please ensure the image is valid and try again.",
                        icon="error"
                    )
                    logger.error(f"Conversion failed for {input_file}: {error_msg}")

            except Exception as e:
                failed_conversions += 1
                self.status_label.config(text=f"Error converting {os.path.basename(input_file)}")
                messagebox.showerror(
                    "Unexpected Error",
                    f"An unexpected error occurred while converting '{os.path.basename(input_file)}'.\n\n"
                    f"Error: {str(e)}\n\n"
                    "Please try again or contact support if the problem persists.",
                    icon="error"
                )
                logger.error(f"Unexpected error during conversion of {input_file}: {str(e)}")

            self.progress_bar["value"] = i + 1
            self.root.update_idletasks()

        self.convert_button.config(state=tk.NORMAL)
        self.select_files_button.config(state=tk.NORMAL)
        self.select_output_button.config(state=tk.NORMAL)

        final_message = f"Conversion complete. {successful_conversions} succeeded, {failed_conversions} failed."
        self.status_label.config(text=final_message)
        logger.info(final_message)
        
        if successful_conversions > 0:
            messagebox.showinfo(
                "Conversion Complete",
                f"Successfully converted {successful_conversions} file(s) to SVG format.\n\n"
                f"Files have been saved to:\n{self.output_dir}",
                icon="info"
            )
        elif failed_conversions == len(self.input_files):
            messagebox.showerror(
                "Conversion Failed",
                "No files were converted successfully.\n\n"
                "Please check your input files and try again.",
                icon="error"
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageConverterApp(root)
    root.mainloop()