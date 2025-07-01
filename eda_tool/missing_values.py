import seaborn as sns
import matplotlib.pyplot as plt

def plot_missing_values(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(df.isnull(), cbar=False, yticklabels=False, cmap='viridis', ax=ax)
    ax.set_title("Missing Values Heatmap")
    return fig
