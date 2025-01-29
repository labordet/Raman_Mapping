import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")  # For embedded matplotlib in Tk
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import os
from ttkthemes import ThemedTk
from tkinter import filedialog, messagebox, StringVar
from tkinter import ttk


class SpectraAnalysisApp:
    def __init__(self, root):
        # Use ThemedTk-based root window
        self.root = root
        self.root.title("Spectra Analysis - Á. Labordet, NSI 405")
        # Start small—only enough room for file/directory selection
        self.root.geometry("600x200")
        self.root.resizable(True, True)

        # -------- THEME SELECTION (like in the second code) --------
        self.theme_frame = ttk.Frame(self.root)
        self.theme_frame.pack(side="top", fill="x", padx=5, pady=5)

        ttk.Label(self.theme_frame, text="Select Theme:").pack(side="left", padx=5)
        self.theme_var = StringVar(value="arc")  # default theme
        # List the available themes from ttkthemes
        self.themes = sorted(self.root.get_themes())
        self.theme_combo = ttk.Combobox(
            self.theme_frame,
            textvariable=self.theme_var,
            values=self.themes,
            width=15,
            state="readonly"
        )
        self.theme_combo.pack(side="left", padx=5)
        self.theme_combo.bind("<<ComboboxSelected>>", self.change_theme)

        # ========== (1) File + Directory Selection in a LabelFrame ==========
        self.file_frame = ttk.LabelFrame(self.root, text="(1) File + Directory Selection")
        self.file_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(self.file_frame, text="Select .txt File:").grid(row=0, column=0, sticky="e")
        self.file_label = ttk.Label(self.file_frame, text="No file selected", width=50)
        self.file_label.grid(row=0, column=1, sticky="w")
        ttk.Button(self.file_frame, text="Browse", command=self.select_file).grid(row=0, column=2, padx=5)

        ttk.Label(self.file_frame, text="Select Output Directory:").grid(row=1, column=0, sticky="e")
        self.dir_label = ttk.Label(self.file_frame, text="No directory selected", width=50)
        self.dir_label.grid(row=1, column=1, sticky="w")
        ttk.Button(self.file_frame, text="Browse", command=self.select_directory).grid(row=1, column=2, padx=5)

        # ========== (2) Analysis Inputs & Plot in a LabelFrame ==========
        self.analysis_frame = ttk.LabelFrame(self.root, text="(2) Analysis Inputs & Plot")
        # We'll pack() this frame only AFTER a file is chosen (in load_and_plot).

        # Region Start/End, Points/Lines
        ttk.Label(self.analysis_frame, text="Region Start:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.region_start = ttk.Entry(self.analysis_frame, width=10)
        self.region_start.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        self.region_start.insert(0, "240")  # Default

        ttk.Label(self.analysis_frame, text="Region End:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.region_end = ttk.Entry(self.analysis_frame, width=10)
        self.region_end.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        self.region_end.insert(0, "254")  # Default

        ttk.Label(self.analysis_frame, text="Points per Line:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.points_per_line = ttk.Entry(self.analysis_frame, width=10)
        self.points_per_line.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        self.points_per_line.insert(0, "110")  # Default

        ttk.Label(self.analysis_frame, text="Lines per Image:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.lines_per_image = ttk.Entry(self.analysis_frame, width=10)
        self.lines_per_image.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        self.lines_per_image.insert(0, "90")  # Default

        # Analyze button
        ttk.Button(self.analysis_frame, text="Analyze", command=self.analyze)\
            .grid(row=4, column=0, columnspan=2, pady=10)

        # (3) Plot Frame
        self.plot_frame = ttk.Frame(self.analysis_frame)
        # Place this below the "Analyze" button
        self.plot_frame.grid(row=5, column=0, columnspan=3, pady=10, sticky="nsew")

        # (4) Progress Bar
        self.progress = ttk.Progressbar(self.analysis_frame, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=6, column=0, columnspan=3, pady=10)

        # Internal data
        self.input_file = None
        self.output_dir = None
        self.x = None             # X-axis
        self.avg_spectrum = None  # Average of all columns

        # Let the lower rows/columns expand if user resizes
        self.analysis_frame.rowconfigure(5, weight=1)
        self.analysis_frame.columnconfigure(1, weight=1)

    # --- THEME SWITCHING, EXACTLY LIKE IN THE SECOND CODE ---
    def change_theme(self, event=None):
        new_theme = self.theme_var.get()
        self.root.set_theme(new_theme)

    # --- FILE AND DIRECTORY SELECTION ---
    def select_file(self):
        """User picks a .txt file; store path, load data, and show the analysis frame with average spectrum."""
        path = filedialog.askopenfilename(
            title="Select the .txt file",
            filetypes=[("Text files", "*.txt")]
        )
        if path:
            self.input_file = path
            self.file_label.config(text=os.path.basename(self.input_file))
            # Load & plot average spectrum
            self.load_and_plot()

    def select_directory(self):
        """User picks an output directory; store path."""
        path = filedialog.askdirectory(title="Select the directory to save results")
        if path:
            self.output_dir = path
            self.dir_label.config(text=self.output_dir)

    # --- LOAD + INITIAL PLOT ---
    def load_and_plot(self):
        """Load the data, compute the average, plot it, and then show the rest of the UI."""
        if not self.input_file:
            return

        # Show a quick "Plot is being generated..." message
        self.plot_wait_label = ttk.Label(self.file_frame, text="Plot is being generated, please wait...")
        self.plot_wait_label.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="w")
        self.root.update_idletasks()

        # Read data
        self.x, spectra = self.load_data(self.input_file)
        self.avg_spectrum = spectra.mean(axis=1)

        # Once data is loaded, expand the main window and show the analysis frame
        self.root.geometry("800x600")
        self.analysis_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Clear any previous plot from plot_frame
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # Create a new figure for the average spectrum
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(self.x, self.avg_spectrum, label='Average Spectrum')
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Intensity')
        ax.set_title('Average Spectrum')
        ax.legend()
        ax.grid(True)

        # Embed figure in Tk
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas, self.plot_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        # Remove the "Plot is being generated..." label
        self.plot_wait_label.destroy()

    # --- ANALYSIS ---
    def analyze(self):
        """After user sets region, points, lines, do the peak-finding, heatmaps, and save an Excel file."""
        if not self.input_file or not self.output_dir:
            messagebox.showerror("Error", "Please select both input file and output directory.")
            return

        # Validate numeric inputs
        try:
            region_start = float(self.region_start.get())
            region_end = float(self.region_end.get())
            points_per_line = int(self.points_per_line.get())
            lines_per_image = int(self.lines_per_image.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid input for region or image dimensions.")
            return

        region = [region_start, region_end]
        x, spectra = self.load_data(self.input_file)

        # Configure progress bar
        self.progress["value"] = 0
        self.progress["maximum"] = len(spectra.columns)

        # Go column by column, find top 3 peaks in the specified region
        results = []
        for i, col in enumerate(spectra.columns):
            mask = (x >= region[0]) & (x <= region[1])
            y_region = spectra[col][mask]
            top_3_indices = y_region.nlargest(3).index  # Indices of largest 3 points
            top_3_avg = y_region.loc[top_3_indices].mean()
            # Just pick the largest point’s x as “max_x”
            max_x = x[top_3_indices].iloc[0]
            results.append((max_x, top_3_avg))

            # Update progress bar
            self.progress["value"] = i + 1
            self.progress.update()

        # Generate heatmaps from the results
        self.generate_heatmaps(results, points_per_line, lines_per_image)
        # Save results to Excel
        self.save_results_to_excel(results)

        messagebox.showinfo("Success", "Analysis complete! Results saved.")

    # --- LOAD DATA ---
    def load_data(self, file_path):
        """Reads a space-delimited text file. 
           First column = X-axis; subsequent columns = spectra."""
        data = pd.read_csv(file_path, delim_whitespace=True, header=None)
        x_axis = data.iloc[:, 0]
        spectra = data.iloc[:, 1:]
        return x_axis, spectra

    # --- GENERATE HEATMAPS ---
    def generate_heatmaps(self, results, points_per_line, lines_per_image):
        """Plot and save the center and intensity heatmaps, both with 'plasma' colormap."""
        centers = [r[0] for r in results]
        intensities = [r[1] for r in results]

        center_array = np.array(centers).reshape(lines_per_image, points_per_line)
        intensity_array = np.array(intensities).reshape(lines_per_image, points_per_line)

        # ========== Center Heatmap (use plasma) ==========
        plt.figure()
        plt.imshow(center_array, cmap='plasma', aspect='auto')
        plt.colorbar(label='Peak Center (X-axis)')
        plt.title('Center Heatmap')
        plt.savefig(os.path.join(self.output_dir, 'center_heatmap.png'))
        plt.close()

        # ========== Intensity Heatmap (use plasma) ==========
        plt.figure()
        plt.imshow(intensity_array, cmap='plasma', aspect='auto')
        plt.colorbar(label='Peak Intensity')
        plt.title('Intensity Heatmap')
        plt.savefig(os.path.join(self.output_dir, 'intensity_heatmap.png'))
        plt.close()

    # --- SAVE RESULTS ---
    def save_results_to_excel(self, results):
        """Save the list of (center, intensity) to an Excel file."""
        centers = [r[0] for r in results]
        intensities = [r[1] for r in results]
        df = pd.DataFrame({"Center (X-axis)": centers, "Intensity": intensities})

        output_path = os.path.join(self.output_dir, 'results.xlsx')
        df.to_excel(output_path, index=False)


# ========== Run the app ==========
if __name__ == "__main__":
    root = ThemedTk(theme="arc")
    app = SpectraAnalysisApp(root)
    root.mainloop()
