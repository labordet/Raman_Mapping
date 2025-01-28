# Spectra Analysis App – Quick-Start Guide

A simple desktop application (Windows .exe) that loads a space-delimited text file containing spectral data (exported from WITec), plots the average spectrum, then generates heatmaps of peak centers and intensities, along with an Excel results file.

---

## Table of Contents

1. [Purpose](#purpose)
2. [Preparing Data in WITec](#preparing-data-in-witec)
3. [Launching the App](#launching-the-app)
4. [Selecting the Input `.txt` File](#selecting-the-input-txt-file)
5. [Selecting the Output Directory](#selecting-the-output-directory)
6. [Specifying Parameters](#specifying-parameters)
7. [Running the Analysis](#running-the-analysis)
8. [Reviewing the Outputs](#reviewing-the-outputs)
9. [Troubleshooting & Tips](#troubleshooting--tips)
10. [Adding Images to Your GitHub README](#adding-images-to-your-github-readme)

---

## Purpose

This application:
- Loads a space- or tab-delimited text file containing spectral data (exported from WITec).
- Plots the **average spectrum**.
- Generates **heatmaps** of peak centers and intensities.
- Exports an **Excel** results file containing the peak centers and intensities for each spectrum in the map.

---

## Preparing Data in WITec

1. **Locate Your Raman Mapping Data** in the WITec Project.
2. **Right-Click** on the mapping data entry.
3. Select **Export → Table**.
4. In the **Export Filter File Info** dialog:
   - Set your x-axis units (e.g., rel. 1/cm or nm—whatever you prefer).
   - Choose **Export into one file**, give it a filename (e.g., `Export File.txt`).
   - Click **OK** to finalize the export.
5. Confirm the resulting `.txt` is space/tab-delimited, with:
   - **First column**: x-axis values (wavenumbers, wavelength, etc.)
   - **Subsequent columns**: intensities for each spectrum in the map
6. **Note the Points per Line and Lines per Image** used in your WITec scan.  
   - You can find these in the **Info** text object (the green “T” icon) under the mapping data in the project tree.
   - You’ll need these values to generate correct heatmaps in this app.

---

## Launching the App

1. **Double-click** the `.exe` file (on Windows).
2. A small window appears with two fields:
   - **Select .txt File**
   - **Select Output Directory**

---

## Selecting the Input `.txt` File

1. Click **Browse** next to **Select .txt File**.
2. Navigate to the `.txt` file you exported from WITec.  
   **Data Format Reminder**:
   - First column = x-axis (e.g., wavenumber or wavelength)
   - All subsequent columns = intensities for each spectrum
3. Click **Open**.  
   The program will show a message: “Plot is being generated, please wait…”  
   When loading completes, the window resizes to display the **average spectrum** plus additional fields (Region Start/End, Points per Line, etc.).

---

## Selecting the Output Directory

1. Click **Browse** next to **Select Output Directory**.
2. Choose any folder where you want the **heatmaps (`.png`)** and **Excel results (`.xlsx`)** saved.

---

## Specifying Parameters

Below the average spectrum, four fields appear:

1. **Region Start** – Lower bound of your region of interest (e.g., 240).
2. **Region End** – Upper bound of your region of interest (e.g., 254).
3. **Points per Line** – Number of spectra points in each horizontal line of your map (matches WITec’s “Points per Line”).
4. **Lines per Image** – Number of horizontal lines that make up the 2D map (matches WITec’s “Lines per Image”).

> **Tip:** If unsure, check your WITec scan setup or the exported file’s metadata. These must match exactly for correct heatmaps.

---

## Running the Analysis

Click **Analyze**:

1. The software reads each column of the input data within the specified **Region Start–End**.
2. For each column (each spectrum), it:
   - Finds the **top 3** highest intensities in that region.
   - Calculates:
     - **Peak Center** = the x-axis position of the highest among those top 3 peaks
     - **Average Intensity** of those top 3 peak values
3. A progress bar shows analysis progress.

When complete, you’ll see a popup: **“Analysis complete! Results saved.”**

---

## Reviewing the Outputs

1. **Average Spectrum**  
   Displayed in the main window with a Matplotlib toolbar for zoom/pan/save.
2. **Center Heatmap** (`center_heatmap.png`)  
   Visualizes the peak center position across your scanned 2D area.
3. **Intensity Heatmap** (`intensity_heatmap.png`)  
   Visualizes the peak intensity across your scanned area.
4. **results.xlsx**  
   A spreadsheet listing each column’s:
   - **Center (X-axis)**
   - **Intensity**

---

## Troubleshooting & Tips

- **Export Format**: Ensure the `.txt` is space/tab-delimited, with the first column as your x-axis.
- **Long Load Times**: Large `.txt` files can take a while. You’ll see “Plot is being generated…” until it finishes.
- **Points/Lines Mix-up**: If heatmaps look incorrect or you get a reshape error, verify the **Points per Line** and **Lines per Image** match WITec’s settings.
- **Missing File/Directory**: The app prompts you to select a file and output folder if forgotten.
- **Invalid Inputs**: If Region Start/End or Points/Lines are not numeric, the app will ask you to correct them.

---

## Adding Images to Your GitHub README

You can include the output heatmaps (e.g., `center_heatmap.png`, `intensity_heatmap.png`) in your GitHub README by placing them in your repository and referencing them like so:

```markdown
![Center Heatmap](path/to/center_heatmap.png)
![Intensity Heatmap](path/to/intensity_heatmap.png)
