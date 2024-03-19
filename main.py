import argparse
import os

from src.fft import embed, extract
from PIL import Image


parser = argparse.ArgumentParser(description='Image steganography tool for text embedding and extraction using Fast Fourier Transform (FFT)')
parser.add_argument('-i', dest='image', required=True, help='Input image file')
parser.add_argument('-b', dest='base_image', help='Base image file (for extraction only)')
parser.add_argument('-t', dest='text', help='Text to be embedded')
parser.add_argument('-E', dest='embed', action='store_true', help='Embed watermark in the image')
parser.add_argument('-X', dest='extract', action='store_true', help='Extract watermark')


def main():
    args = parser.parse_args()
    if not os.path.isfile(args.image):
        print("Image doesn't exist or isn't specified")
        return
    img = Image.open(args.image)
    
    if args.embed and args.text:
        res = embed(img, args.text)
        Image.fromarray(res).save(f"res.{img.format.lower()}")
    elif args.extract:
        if not os.path.isfile(args.base_image):
            print("Base image doesn't exist or isn't specified")
            return
        base_img = Image.open(args.base_image)
        
        res = extract(img, base_img)
        Image.fromarray(res).save(f"text.{img.format.lower()}")
        
        base_img.close()
    else:
        print("Choose either to embed text (using flags -E and -t) or extract text (-X)")
        return
    
    img.close()

    
if __name__ == "__main__":
    main()