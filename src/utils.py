from PIL import ImageFont, ImageDraw, Image
import numpy as np


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CHARS_PER_ROW = 50
MONOSPACE_FONT_RATIO = 0.6


def text_to_image(text: str, shape: tuple[int, int]) -> Image:
    shape = (shape[1], shape[0])
    
    font_size = shape[0] // int(CHARS_PER_ROW * MONOSPACE_FONT_RATIO)
    n_rows = shape[1] // font_size

    if len(text) > CHARS_PER_ROW * n_rows:
        print(f"Text is to big, {len(text) - CHARS_PER_ROW * n_rows} chars will be stripped")
        text = text[:CHARS_PER_ROW * n_rows]

    font = ImageFont.truetype("static/font.ttf", font_size)

    text_img = Image.new('RGB', shape, color=BLACK)
    drawer = ImageDraw.Draw(text_img)
    
    for i in range(n_rows):
        drawer.text((0, i * font_size), 
                    text[i * CHARS_PER_ROW: (i + 1) * CHARS_PER_ROW], 
                    fill=WHITE, font=font)
    
    return text_img


def normalize_image(img: np.ndarray) -> np.ndarray:
    if img.dtype == np.uint8:
        img = img[:,:,:3] / 255.0
        
    return img[:, :, :3].astype(np.float64)


def denormalize_image(img: np.ndarray) -> np.ndarray:
    if img.dtype != np.uint8:
        # img, _, _ = centralize(img)
        img = np.clip(img, 0, 1) * 255
        
    return img[:, :, :3].astype(np.uint8)


def centralize(img: np.ndarray, side = 0.06):
    img = img.real.astype(np.float64)
    thres = img.size * side
    
    l = img.min()
    r = img.max()
    while l + 1 <= r:
        m = (l + r) / 2.
        s = np.sum(img < m)
        if s < thres:
            l = m
        else:
            r = m
    low = l            
            
    l = img.min()
    r = img.max()
    while l + 1 <= r:
        m = (l + r) / 2.
        s = np.sum(img > m)
        if s < thres:
            r = m
        else:
            l = m            
            
    high = max(low + 1, r)          
    img = (img - low) / (high - low)
    
    return img, low, high


def get_xmap(shape):
    return np.arange(shape[0]).reshape((-1, 1)), np.arange(shape[1])