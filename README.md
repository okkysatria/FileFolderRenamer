# File and Folder Renamer

A desktop application designed to rename multiple files and folders within a selected directory. The application provides functionalities to filter, sort, and batch rename items. Available as both a standalone executable and a Python script.

<div align="center">
  <img src="https://github.com/user-attachments/assets/110aa083-9e8b-4f7c-882e-a37c0823e2c0" alt="ss" width="500"/>
</div


## Requirements

- **Windows 10/11**
- **Python 3.11.x** (Required only for the Python script, not for the executable)

## Download and Installation

### Option 1: Using the Executable

1. **Download the Executable:**
   - [Download](https://github.com/okkysatria/FileFolderRenamer/releases/download/v1/FFR.exe)

2. **Run the Executable:**
   - Double-click `renamer.exe` to launch the application. Use the GUI to select a directory, scan items, and perform batch renaming.

3. **Using the GUI:**
   - **Select Directory:** Choose the directory containing items to rename.
   - **Scan Mode:** Switch between "Files" and "Folders" modes to list specific items.
   - **Sort By:** Choose how to sort items ("Name" or "Date Modified").
   - **Batch Rename:** Enter new names and click "Batch Rename" to rename items.
   - **Undo/Redo:** Use the "Undo" and "Redo" buttons to revert or reapply renaming actions.
   - **Filter Items:** Apply a filter to show items matching the specified text.
   - **Copy to Clipboard/Save to Note:** Copy the list of items to the clipboard or save it to a text file.

### Option 2: Using the Python Script

1. **Download the Repository:**
   - [Download ZIP](https://github.com/okkysatria/FileFolderRenamer/archive/refs/heads/main.zip)

2. **Extract the ZIP File:**
   - Extract the ZIP file to a location of your choice.

3. **Install Python:**
   - Ensure Python 3.11.x is installed on your computer. Download it from the [official Python website](https://www.python.org/ftp/python/3.11.1/python-3.11.1-amd64.exe).

4. **Install Dependencies:**
   - Open a command prompt or terminal, navigate to the extracted directory, and install the required libraries with:
     ```bash
     pip install -r requirements.txt
     ```

5. **Run the Script:**
   - Execute `file_renamer.py` by running:
     ```bash
     python file_renamer.py
     ```

6. **Using the Script:**
   - Follow the same instructions as for the executable to select directories, scan items, rename items, and use interactive commands.
