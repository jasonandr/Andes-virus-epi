import numpy as np
from PIL import Image

img = Image.open("/Users/jasonandrews/repos/hanta/data/vial_img_p1_4.png")
data = np.array(img.convert('L'))  # grayscale

# Find rows corresponding to bars
# Bars are mostly black/grey/white with horizontal black outlines.
# Let's average horizontally
row_means = np.mean(data, axis=1)

# we can find the y-coordinates of the bars
# Let's print out the profile
for y in range(data.shape[0]):
    pass

# A simpler way: we know there are 20 bars.
# Let's crop x corresponding to the plot area.
# x-axis has a line at the bottom.
# y-axis has a line on the left.
