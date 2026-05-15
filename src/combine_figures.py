import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import time
import glob

def get_latest_file(directory, prefix):
    files = glob.glob(os.path.join(directory, f"{prefix}*.png"))
    return max(files, key=os.path.getctime) if files else None

def main():
    artifacts_dir = "/Users/jasonandrews/.gemini/antigravity/brain/26e83a96-4a63-4226-94fe-627b326b4048/artifacts"
    
    img1_path = get_latest_file(artifacts_dir, "comparative_incubation_")
    img2_path = get_latest_file(artifacts_dir, "infectiousness_profile_")
    img3_path = get_latest_file(artifacts_dir, "offspring_distribution_")
    
    fig, axes = plt.subplots(3, 1, figsize=(10, 18))
    
    # Read images
    img1 = mpimg.imread(img1_path)
    img2 = mpimg.imread(img2_path)
    img3 = mpimg.imread(img3_path)
    
    # Plot images vertically
    axes[0].imshow(img1)
    axes[0].axis('off')
    
    axes[1].imshow(img2)
    axes[1].axis('off')
    
    axes[2].imshow(img3)
    axes[2].axis('off')
    
    plt.tight_layout(pad=0)
    
    timestamp = int(time.time())
    combined_plot_filename = f"combined_historical_analysis_{timestamp}.png"
    combined_plot_path = os.path.join(artifacts_dir, combined_plot_filename)
    plt.savefig(combined_plot_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved combined 3x1 plot to {combined_plot_path}")

if __name__ == "__main__":
    main()
