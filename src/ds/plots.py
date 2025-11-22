import matplotlib.pyplot as plt
import plotly.io as pio
import seaborn as sns


def set_style():
    """
    Sets a professional plotting style for Matplotlib and Seaborn.
    Also sets the default Plotly template.
    """
    # Seaborn / Matplotlib style
    sns.set_theme(style="whitegrid", context="notebook")
    plt.rcParams["figure.figsize"] = (10, 6)
    plt.rcParams["axes.titlesize"] = 16
    plt.rcParams["axes.labelsize"] = 12

    # Plotly default template
    pio.templates.default = "plotly_white"


def save_fig(fig, filename: str, tight_layout: bool = True):
    """
    Helper to save matplotlib figures easily.
    """
    if tight_layout:
        plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches="tight")
