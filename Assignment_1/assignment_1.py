import os, glob, argparse

# Arguments passed at command line
parser = argparse.ArgumentParser()
parser.add_argument("--input_path", type=str, default='./input_folder/', help="path to the input folder where all the files are kept")
parser.add_argument("--output_path", type=str, default='./output_folder/', help="path to the input folder where all the files are kept")
args = parser.parse_args()

# Make the necessary global variables
text_files_extensions = ['.txt', '.doc', '.docx', '.pdf']
image_files_extensions = ['.jpg', '.jpeg', '.bmp', '.png', '.tiff']
IMAGES_FOLDER = 'images'
TEXTS_FOLDER = 'texts'
# Make the necessary output folders
os.makedirs(os.path.join(args.output_path, IMAGES_FOLDER), exist_ok=True)
os.makedirs(os.path.join(args.output_path, TEXTS_FOLDER), exist_ok=True)

for file_path in glob.glob(os.path.join(args.input_path, "*")): # Iterate through all the files
    if any([file_path.endswith(ext) for ext in text_files_extensions]): # If extension ends with text file extensions given above
        os.replace(file_path, os.path.join(args.output_path, TEXTS_FOLDER, os.path.basename(file_path))) # File move
    elif any([file_path.endswith(ext) for ext in image_files_extensions]): # If extension ends with image file extensions given above
        os.replace(file_path, os.path.join(args.output_path, IMAGES_FOLDER, os.path.basename(file_path))) # File move
    else: # Extension is neither from text nor from image
        try:
            raise Exception(f"{file_path} is neither text file nor image file")
        except Exception as e:
            print(e)

# Note: I have seggregated based on extension. We could have used the seggregation based on mime type as well.
# https://stackoverflow.com/questions/43580/how-to-find-the-mime-type-of-a-file-in-python
# The above link helps to find the mimetype