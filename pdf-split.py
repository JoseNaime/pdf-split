import sys
import os
import fitz  # PyMuPDF

def extract_name_from_file_path(file_path):
    """ Extracts and returns the file name without extension from a file path. """
    return os.path.splitext(os.path.basename(file_path))[0]

def ensure_folder_exists(folder_path):
    """ Ensures the output folder exists, creates it if it doesn't. """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def split_pdf_to_files(doc, output_base):
    """ Splits the PDF into individual files. """
    for page_num in range(len(doc)):
        with fitz.open() as new_pdf:
            new_pdf.insert_pdf(doc, from_page=page_num, to_page=page_num)
            output_filename = f"{output_base}-Page-{page_num + 1}.pdf"
            new_pdf.save(output_filename)
            print(f"Saved: {output_filename}")

def convert_pdf_to_png(doc, output_base):
    """ Converts PDF pages to PNG format. """
    for page_number in range(len(doc)):
        page = doc.load_page(page_number)
        pix = page.get_pixmap()
        output_file = f"{output_base}-Page-{page_number + 1}.png"
        pix.save(output_file)

def process_pdf(input_file_path, output_folder):
    """ Processes the PDF to split and convert to PNG. """
    output_filename_base = f"{output_folder}/{extract_name_from_file_path(input_file_path)}"

    with fitz.open(input_file_path) as doc:
        if len(doc) == 0:
            raise Exception("No pages found in the document")

        split_pdf_to_files(doc, output_filename_base)
        convert_pdf_to_png(doc, output_filename_base)

def main():
    """ Main function to handle command-line arguments and run processes. """
    try:
        if len(sys.argv) < 3:
            raise Exception("Usage: pdfSplitter <input_file_path> <output_folder_path>")

        input_file_path = sys.argv[1]
        output_folder = sys.argv[2]
        ensure_folder_exists(output_folder)

        process_pdf(input_file_path, output_folder)

    except Exception as e:
        print(f"Caught an error: {e}")

if __name__ == "__main__":
    main()
