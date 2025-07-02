import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_pie_chart(df, column):
    """
    Generates a pie chart for a categorical column.
    Returns a matplotlib figure.
    """
    fig, ax = plt.subplots(figsize=(6, 6))
    counts = df[column].value_counts(dropna=False)
    ax.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90)
    ax.set_title(f"Pie Chart of {column}")
    ax.axis('equal')  # Equal aspect ratio ensures the pie is circular.
    return fig

# Helper function to get categorical and numerical columns
def get_col_types(df):
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    return cat_cols, num_cols


def plot_histograms(df):
    cat_cols, num_cols = get_col_types(df)
    df_numeric = df[num_cols]

    fig, axs = plt.subplots(len(num_cols), 1, figsize=(10, 4 * len(num_cols)))
    if len(num_cols) == 1:
        axs = [axs]

    for i, col in enumerate(num_cols):
        sns.histplot(df[col].dropna(), kde=True, ax=axs[i])
        axs[i].set_title(f"Histogram of {col}")
    plt.tight_layout()
    return fig


def plot_correlation_matrix(df):
    _, num_cols = get_col_types(df)
    corr = df[num_cols].corr()

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
    ax.set_title("Correlation Matrix")
    return fig


def plot_countplots(df):
    cat_cols, _ = get_col_types(df)
    figs = []
    for col in cat_cols:
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.countplot(data=df, x=col, ax=ax)
        ax.set_title(f"Count Plot of {col}")
        ax.tick_params(axis='x', rotation=45)
        figs.append(fig)
    return figs


def plot_boxplots(df):
    _, num_cols = get_col_types(df)
    figs = []
    for col in num_cols:
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.boxplot(data=df, x=col, ax=ax)
        ax.set_title(f"Box Plot of {col}")
        figs.append(fig)
    return figs


def plot_violinplots(df):
    _, num_cols = get_col_types(df)
    figs = []
    for col in num_cols:
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.violinplot(data=df, x=col, ax=ax)
        ax.set_title(f"Violin Plot of {col}")
        figs.append(fig)
    return figs


def plot_pairplot(df):
    _, num_cols = get_col_types(df)
    pairplot_df = df[num_cols].dropna()
    fig = sns.pairplot(pairplot_df)
    return fig.figure


def plot_kde(df):
    _, num_cols = get_col_types(df)
    figs = []
    for col in num_cols:
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.kdeplot(df[col].dropna(), shade=True, ax=ax)
        ax.set_title(f"KDE Plot of {col}")
        figs.append(fig)
    return figs
