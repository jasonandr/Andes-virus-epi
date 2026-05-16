import numpy as np
from PIL import Image

img = Image.open("/Users/jasonandrews/repos/hanta/data/vial_img_p1_4.png")
data = np.array(img.convert('L'))

x0 = 145
pixels_per_day = 6.75  # approximate

col_0 = data[:, x0]
bar_pixels = np.where(col_0 < 200)[0]
    
bars = []
current_bar = []
for y in bar_pixels:
    if not current_bar or y - current_bar[-1] == 1:
        current_bar.append(y)
    else:
        if len(current_bar) > 2:
            bars.append(int(np.mean(current_bar)))
        current_bar = [y]
if len(current_bar) > 2:
    bars.append(int(np.mean(current_bar)))
        
bars = bars[::-1]
    
for i, y in enumerate(bars):
    patient_no = i + 1
    row = data[y, :]
        
    x_exp = x0
    while x_exp > 0 and row[x_exp] < 200:
        x_exp -= 1
        
    x_white_end = x0 + 2 # skip left black border
    while x_white_end < data.shape[1] and row[x_white_end] > 100:
        x_white_end += 1
            
    x_black_end = x_white_end
    while x_black_end < data.shape[1] and row[x_black_end] < 150:
        x_black_end += 1
            
    exposure_start = (x_exp - x0) / pixels_per_day
    min_inc = (x_white_end - x0) / pixels_per_day
    prodrome_end = (x_black_end - x0) / pixels_per_day
        
    print(f"Patient {patient_no:2d}: exp={exposure_start:5.1f}, min_inc={min_inc:4.1f}, prodrome={prodrome_end:4.1f}")
