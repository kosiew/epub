from ebooklib import epub
import os
from typing import Protocol
import typer

app = typer.Typer()

class EpubConverter(Protocol):
    def downgrade_epub3_to_epub2(self, input_file: str, output_file: str) -> None:
        ...

class EpubConverterImpl:
    def downgrade_epub3_to_epub2(self, input_file: str, output_file: str) -> None:
        print(f"==> Converting {input_file} to {output_file}")
        
        # Load the EPUB file
        book = epub.read_epub(input_file)

        # Ensure metadata key exists
        opf_namespace = 'http://www.idpf.org/2007/opf'
        if opf_namespace in book.metadata:
            if 'version' in book.metadata[opf_namespace]:
                print(f"==> Original EPUB version: {book.metadata[opf_namespace]['version']}")
            else:
                print("==> Version metadata not found, adding it.")
            book.metadata[opf_namespace]['version'] = ['2.0']  # Store as a list
        else:
            print("==> OPF namespace not found in metadata, creating it.")
            book.metadata[opf_namespace] = {'version': ['2.0']}

        # Save the new EPUB file
        epub.write_epub(output_file, book)

        print(f"EPUB 3 downgraded to EPUB 2 and saved as: {output_file}")


@app.command()
def convert_epub_to_v2(input_folder: str, output_folder: str) -> None:
    print(f"==> Starting conversion from {input_folder} to {output_folder}")
    converter = EpubConverterImpl()
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.epub'):
                input_file = os.path.join(root, file)
                relative_path = os.path.relpath(root, input_folder)
                output_dir = os.path.join(output_folder, relative_path)
                os.makedirs(output_dir, exist_ok=True)
                output_file = os.path.join(output_dir, f"{os.path.splitext(file)[0]}_epub2.epub")
                print(f"==> Processing file {input_file}")
                converter.downgrade_epub3_to_epub2(input_file, output_file)

if __name__ == "__main__":
    print("==> Running the application")
    app()