import os
from typing import Protocol
import typer
import subprocess

app = typer.Typer()
DEFAULT_OUTPUT_FOLDER = "/Users/kosiew/Downloads/epub_v2"


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


@app.command()
def convert_epub_to_v2(
    input_folder: str, output_folder: str = DEFAULT_OUTPUT_FOLDER
) -> None:
    print(f"==> Starting conversion from {input_folder} to {output_folder}")
    converter = EpubConverterImpl()
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".epub"):
                input_file = os.path.join(root, file)
                relative_path = os.path.relpath(root, input_folder)
                output_dir = os.path.join(output_folder, relative_path)
                os.makedirs(output_dir, exist_ok=True)
                output_file = os.path.join(
                    output_dir, f"{os.path.splitext(file)[0]}_epub2.epub"
                )
                print(f"==> Processing file {input_file}")
                converter.downgrade_epub3_to_epub2(input_file, output_file)


if __name__ == "__main__":
    print("==> Running the application")
    app()
