from pdf2image import convert_from_path
from PIL import Image
import numpy as np

# Convert PDF pages to images
pdf_file = "gif.pdf"
pages = convert_from_path(pdf_file, dpi=200)  # Adjust dpi for quality

# Define durations
hold_duration = 10  # Frames each page stays before fading
final_hold_duration = 80  # Extra-long hold for the last page
fade_steps = 15  # Number of fade transition frames

# Convert images to RGBA
images = [img.convert("RGBA") for img in pages]
frames = []

def blend_frames(img1, img2, steps):
    """Generate blended transition frames between img1 and img2."""
    transition_frames = []
    for alpha in np.linspace(0, 1, steps):
        blended = Image.blend(img1, img2, alpha)
        transition_frames.append(blended)
    return transition_frames

# Process all pages
for i in range(len(images) - 1):
    frames.extend([images[i]] * hold_duration)  # Hold current frame
    frames.extend(blend_frames(images[i], images[i + 1], fade_steps))  # Fade transition

# Add final frame with extended hold
frames.extend([images[-1]] * final_hold_duration)

# Save as GIF
frames[0].save("animated_fig.gif", save_all=True, append_images=frames[1:], duration=100, loop=0)

print("GIF saved as 'animated_fig.gif'")
