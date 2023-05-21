import os
import argparse
import rawpy
import rawpy.enhance
import traceback
import os
from PIL import Image
from multiprocessing import Pool

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

# converts image to webp (currently hardcoded)
def convert_image(image_path, output_dir, quality):
    try:
        base_name = os.path.basename(image_path)
        output_path = os.path.join(output_dir, os.path.splitext(base_name)[0] + '.webp')
        output_path = output_dir + '/' + image_path + '.webp'

        ensure_dir(output_path)

        if image_path.lower().endswith(('.nef', '.cr2', '.dng', '.raw')):
            with rawpy.imread(image_path) as raw:
                # correct bad pixels would need to be run on all raw files:
                #bad_pixels = rawpy.enhance.find_bad_pixels([image_path1, image_path2, ...])
                #rawpy.enhance.repair_bad_pixels(raw, bad_pixels, method='median')
                rgb = raw.postprocess()
                image = Image.fromarray(rgb)
                image.save(output_path, 'WEBP', quality=quality, lossless=False, method=6)
        else:
            image = Image.open(image_path)
            image.save(output_path, 'WEBP', quality=quality, lossless=False, mathod=6)

        print(f"Converted {image_path} to {output_path}")
    except Exception as e:
        print(f"Error converting {image_path}: {e}")
        traceback.print_exc()

# call convert_image in parallel over all files
def convert_images_in_folder(folder_path, output_dir, quality):
    os.makedirs(output_dir, exist_ok=True)
    image_paths = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            image_paths.append(file_path)

    with Pool() as pool:
        pool.starmap(convert_image, [(path, output_dir, quality) for path in image_paths])

def main():
    parser = argparse.ArgumentParser(description='Convert images to WebP format.')
    parser.add_argument('input_folder', help='Path to the input folder containing the images')
    parser.add_argument('output_folder', help='Path to the output folder to save the WebP files')
    parser.add_argument('-q', '--quality', type=int, default=86, help='Compression quality (0-100)')

    args = parser.parse_args()

    convert_images_in_folder(args.input_folder, args.output_folder, args.quality)

if __name__ == '__main__':
    main()
