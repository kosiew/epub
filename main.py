import os
from typing import Protocol
import typer
import subprocess
import time

app = typer.Typer()
DEFAULT_OUTPUT_FOLDER = "/Users/kosiew/Downloads/epub_v2"
EPUB_TO_GENERATE_FOLDER = "/Users/kosiew/Downloads/epub v2 to generate"

class EpubConverter(Protocol):
    def downgrade_epub3_to_epub2(self, input_file: str, output_file: str) -> None: ...


class EpubConverterImpl:
    EBOOK_CONVERT = "/Applications/calibre.app/Contents/MacOS/ebook-convert"

    def downgrade_epub3_to_epub2(self, input_file: str, output_file: str) -> None:
        print(f"==> Converting {input_file} to {output_file}")

        command = [
            EpubConverterImpl.EBOOK_CONVERT,
            input_file,
            output_file,
            "--epub-version",
            "2",
        ]

        try:
            subprocess.run(command, check=True)
            print(f"Converted '{input_file}' to EPUB v2 -> '{output_file}'")
        except subprocess.CalledProcessError as e:
            print(f"Failed to convert '{input_file}': {e}")
        except FileNotFoundError:
            print(
                "Error: 'ebook-convert' not found. Ensure Calibre is installed and in your PATH."
            )

def walk_epub_files(input_folder: str, output_folder: str):
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith((".epub", ".mobi")):
                input_file = os.path.join(root, file)
                relative_path = os.path.relpath(root, input_folder)
                output_dir = os.path.join(output_folder, relative_path)
                yield input_file, file, output_dir

@app.command()
def copy_files(input_folder: str, output_folder: str = EPUB_TO_GENERATE_FOLDER, hours: int = 2) -> None:
    print(f"==> Copying files from {input_folder} to {output_folder} modified in the last {hours} hours")
    current_time = time.time()
    copied_count = 0
    for input_file, file, output_dir in walk_epub_files(input_folder, output_folder):
        file_mod_time = os.path.getmtime(input_file)
        if (current_time - file_mod_time) <= hours * 3600:
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, file)
            print(f"==> Copying file {input_file} to {output_file}")
            try:
                subprocess.run(["cp", input_file, output_file], check=True)
                print(f"Copied '{input_file}' to '{output_file}'")
                copied_count += 1
            except subprocess.CalledProcessError as e:
                print(f"Failed to copy '{input_file}': {e}")
    print(f"==> Copied {copied_count} files")

@app.command()
def convert_to_epub_v2(
    input_folder: str, output_folder: str = DEFAULT_OUTPUT_FOLDER
) -> None:
    print(f"==> Starting conversion from {input_folder} to {output_folder}")
    converter = EpubConverterImpl()
    processed_count = 0
    for input_file, file, output_dir in walk_epub_files(input_folder, output_folder):
        os.makedirs(output_dir, exist_ok=True)
        base_name, _ = os.path.splitext(file)
        output_file = os.path.join(output_dir, f"{base_name}_epub2.epub")
        print(f"==> Processing file {input_file}")
        converter.downgrade_epub3_to_epub2(input_file, output_file)
        processed_count += 1
    print(f"==> Processed {processed_count} files")

@app.command()
def copy_and_convert(
    input_folder: str,
    copy_output_folder: str = EPUB_TO_GENERATE_FOLDER,
    convert_output_folder: str = DEFAULT_OUTPUT_FOLDER,
    hours: int = 2
) -> None:
    copy_files(input_folder, copy_output_folder, hours)
    convert_to_epub_v2(copy_output_folder, convert_output_folder)

if __name__ == "__main__":
    print("==> Running the application")
    app()
