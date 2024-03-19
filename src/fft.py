from PIL import Image

import numpy as np

from src.utils import (
    normalize_image,
    denormalize_image,
    text_to_image,
    centralize,
    get_xmap,
)

PADS = (1, 1)


def embed(img: Image, text: str) -> Image:
    img = normalize_image(np.asarray(img))
    print(img.shape)
    text_img = text_to_image(text, (img.shape[1] - 2 * PADS[0], img.shape[0] // 2 - 2 * PADS[1]))
    text_img = normalize_image(np.asarray(text_img))
    
    img_fft = np.fft.fft2(img, None, (0, 1))
    
    embedding_zone = np.zeros((img.shape[0] // 2 - 2 * PADS[0], 
                               img.shape[1] - 2 * PADS[1], 
                               3))
    print(embedding_zone.shape, text_img.shape)
    
    embedding_zone[:text_img.shape[0], :text_img.shape[1]] = text_img
    
    _, low, high = centralize(img_fft)
    alpha = high - low
    
    xmap = get_xmap(embedding_zone.shape)
    
    img_fft[PADS[0] + xmap[0], PADS[1] + xmap[1]] += embedding_zone * alpha
    img_fft[-PADS[0] - xmap[0], -PADS[1] - xmap[1]] += embedding_zone * alpha
    
    img_inv = np.fft.ifft2(img_fft, None, (0, 1)).real
    
    return denormalize_image(img_inv)

    
def extract(img: Image, base_img: Image) -> Image:
    img = normalize_image(np.asarray(img))
    base_img = normalize_image(np.asarray(base_img))
    
    img_fft = np.fft.fft2(img, None, (0, 1))
    base_img_fft = np.fft.fft2(base_img, None, (0, 1))
    
    img_fft -= base_img_fft
    
    xmap = get_xmap((img.shape[0] // 2 - 2 * PADS[0], img.shape[1] - 2 * PADS[1]))
    
    embedding_zone, _, _ = centralize(img_fft[PADS[0] + xmap[0], PADS[1] + xmap[1]])
    
    return denormalize_image(embedding_zone)