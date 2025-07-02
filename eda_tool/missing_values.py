import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


def plot_missing_values(df):
    """
    Returns a matplotlib figure showing a heatmap of missing values in the DataFrame.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(df.isnull(), cbar=False, yticklabels=False, cmap='viridis', ax=ax)
    ax.set_title("Missing Values Heatmap")
    return fig


def handle_missing_values_ui(df):
    """
    Streamlit-based UI to handle missing values column-wise.
    Returns the cleaned DataFrame.
    """
    st.markdown("### 🧹 Handle Missing Data")

    null_counts = df.isnull().sum()
    null_counts = null_counts[null_counts > 0]

    if null_counts.empty:
        st.success("✅ No missing values in the dataset.")
        return df

    st.write("🔢 **Missing Value Count per Column:**")
    st.dataframe(null_counts)

    cleaned_df = df.copy()

    for col in null_counts.index:
        st.markdown(f"---\n#### Column: `{col}`")
        col_type = "numerical" if pd.api.types.is_numeric_dtype(df[col]) else "categorical"

        method = st.radio(
            f"Choose how to handle missing values in `{col}`:",
            options=["Drop Rows", "Replace with Mean", "Replace with Median", "Replace with Mode"],
            key=f"missing_{col}"
        )

        if method == "Drop Rows":
            cleaned_df = cleaned_df.dropna(subset=[col])
        elif method == "Replace with Mean":
            if col_type == "numerical":
                cleaned_df[col] = cleaned_df[col].fillna(cleaned_df[col].mean())
            else:
                st.warning("⚠️ Mean replacement only valid for numerical columns.")
        elif method == "Replace with Median":
            if col_type == "numerical":
                cleaned_df[col] = cleaned_df[col].fillna(cleaned_df[col].median())
            else:
                st.warning("⚠️ Median replacement only valid for numerical columns.")
        elif method == "Replace with Mode":
            cleaned_df[col] = cleaned_df[col].fillna(cleaned_df[col].mode()[0])

    return cleaned_df
