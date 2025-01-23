# EPUB Converter

This project provides a tool to convert EPUB v3 files to EPUB v2 format using Calibre's `ebook-convert` utility.

## Requirements

- Python 3.12 or higher
- Calibre installed and `ebook-convert` available in your PATH

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Set up the virtual environment and install dependencies:
    ```sh
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

## Usage

To convert EPUB v3 files to EPUB v2, run the following command:
```sh
python main.py <input_folder> [output_folder]