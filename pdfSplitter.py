from pdf2image import convert_from_path
import sys
import os


def extractNameFromFilePath(filePath):
    split_path = filePath.split("/")
    name = split_path[-1]
    name_without_ext = name.split(".")[0]
    return name_without_ext


def removeEndSlashFromPath(filePath):
    if filePath.endswith("/"):
        return filePath[:-1]
    return filePath


# Read first argument
try:

    if sys.argv[1] == "--help" or sys.argv[1] == "-h":
        print("Usage: pdfSplitter <input_file_path> <output_folder_path>")

    if len(sys.argv) < 2:
        raise Exception("No file path provided")

    filepath = removeEndSlashFromPath(sys.argv[1])
    output_folder = removeEndSlashFromPath(sys.argv[2])

    # check if output_folder exists, if not, create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Convert PDF to list of images
    images = convert_from_path(filepath)

    if len(images) == 0:
        raise Exception("File not found or not pages")

    # Save each page as an image
    for i, image in enumerate(images):
        image.save(f'{output_folder}/{extractNameFromFilePath(filepath)}-Page-{i + 1}.png', 'PNG')

except Exception as e:
    print(f"Caught an error: {e}")
