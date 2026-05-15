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
    
    img1_path = get_latest_file(artifacts_dir, "actual_epuyen_mle_")
    img2_path = get_latest_file(artifacts_dir, "infectiousness_profile_")
    img3_path = get_latest_file(artifacts_dir, "offspring_distribution_")
    img4_path = get_latest_file(artifacts_dir, "parameter_distributions_")
    
    fig, axes = plt.subplots(2, 2, figsize=(20, 12))
    
    # Read images
    img1 = mpimg.imread(img1_path)
    img2 = mpimg.imread(img2_path)
    img3 = mpimg.imread(img3_path)
    img4 = mpimg.imread(img4_path)
    
    # Plot images
    axes[0, 0].imshow(img4) # Parameter distributions
    axes[0, 0].axis('off')
    axes[0, 0].set_title("A. Foundational Parameter Distributions", fontsize=16, fontweight='bold', pad=10)
    
    axes[0, 1].imshow(img1) # Lauer MLE
    axes[0, 1].axis('off')
    axes[0, 1].set_title("B. Interval-Censored MLE of Incubation (Epuyén)", fontsize=16, fontweight='bold', pad=10)
    
    axes[1, 0].imshow(img2) # Infectiousness Profile
    axes[1, 0].axis('off')
    axes[1, 0].set_title("C. Infectiousness Profile (El Bolsón)", fontsize=16, fontweight='bold', pad=10)
    
    axes[1, 1].imshow(img3) # Offspring distribution
    axes[1, 1].axis('off')
    axes[1, 1].set_title("D. Offspring Distribution & Heterogeneity", fontsize=16, fontweight='bold', pad=10)
    
    plt.tight_layout()
    
    timestamp = int(time.time())
    combined_plot_filename = f"combined_historical_analysis_{timestamp}.png"
    combined_plot_path = os.path.join(artifacts_dir, combined_plot_filename)
    plt.savefig(combined_plot_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved combined plot to {combined_plot_path}")

if __name__ == "__main__":
    main()
