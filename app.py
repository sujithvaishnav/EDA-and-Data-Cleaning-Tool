import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from eda_tool.data_loader import load_data
from eda_tool.missing_values import plot_missing_values,handle_missing_values_ui
from eda_tool.visualization import (
    plot_histograms, plot_correlation_matrix, plot_countplots,
    plot_boxplots, plot_violinplots, plot_pairplot, plot_kde
)

# Set page config
st.set_page_config(page_title="Clean Sight", layout="wide")
st.title("📊 Tool for Basic Data Cleaning and EDA")
st.markdown("#### _By Sujith Vaishnav")
st.markdown("---")

# File Upload
st.sidebar.header("📂 Upload Your Dataset")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

# Plot choices based on data type
PLOT_OPTIONS = {
    "categorical": ["Count Plot", "Pie Plot"],
    "numerical": ["Histogram", "Box Plot", "Violin Plot", "KDE Plot"]
}

if uploaded_file:
    df = load_data(uploaded_file)

    if df is not None:
        st.sidebar.success("✅ Dataset Loaded Successfully!")
        
        # Sidebar Navigation
        section = st.sidebar.radio(
            "Select Analysis Section",
            ("Dataset Overview", "Missing Values", "Interactive Visualizations")
        )

        if section == "Dataset Overview":
            st.header("📑 Dataset Overview")
            with st.expander("🔢 Dataset Shape"):
                st.write(f"Shape: {df.shape}")
            with st.expander("📝 Column Names"):
                st.write(list(df.columns))
            with st.expander("📉 Data Types"):
                st.write(df.dtypes)
            with st.expander("📈 Summary Statistics"):
                st.write(df.describe())

        elif section == "Missing Values":
            st.header("🚨 Missing Values Analysis")

            with st.expander("🗺️ Missing Values Heatmap"):
                st.pyplot(plot_missing_values(df))

            # Handle nulls
            modified_df = handle_missing_values_ui(df)

            # Option to use or download cleaned data
            use_cleaned = st.checkbox("✅ Use this cleaned data for further analysis")

            st.download_button(
                label="📥 Download Cleaned CSV",
                data=modified_df.to_csv(index=False).encode("utf-8"),
                file_name="cleaned_data.csv",
                mime="text/csv"
            )

            if use_cleaned:
                df = modified_df



        elif section == "Interactive Visualizations":
            st.header("🎨 Interactive Column-wise Visualizations")

            col_selected = st.selectbox("📌 Select a column", df.columns)

            # Detect data type
            if df[col_selected].dtype in ['object', 'category']:
                col_type = "categorical"
            elif pd.api.types.is_numeric_dtype(df[col_selected]):
                col_type = "numerical"
            else:
                col_type = None
                st.warning("❗ Unsupported column type.")

            if col_type:
                plot_selected = st.selectbox("📊 Select plot type", PLOT_OPTIONS[col_type])

                # Plot logic based on type
                fig, ax = plt.subplots(figsize=(8, 4))

                if col_type == "categorical":
                    if plot_selected == "Count Plot":
                        sns.countplot(data=df, x=col_selected, ax=ax)
                        ax.set_title(f"Count Plot of {col_selected}")
                        ax.tick_params(axis='x', rotation=45)
                    elif plot_selected == "Pie Plot":
                        from eda_tool.visualization import plot_pie_chart
                        pie_fig = plot_pie_chart(df, col_selected)
                        st.pyplot(pie_fig)

                elif col_type == "numerical":
                    if plot_selected == "Histogram":
                        sns.histplot(df[col_selected].dropna(), kde=True, ax=ax)
                        ax.set_title(f"Histogram of {col_selected}")
                    elif plot_selected == "Box Plot":
                        sns.boxplot(x=df[col_selected], ax=ax)
                        ax.set_title(f"Box Plot of {col_selected}")
                    elif plot_selected == "Violin Plot":
                        sns.violinplot(x=df[col_selected], ax=ax)
                        ax.set_title(f"Violin Plot of {col_selected}")
                    elif plot_selected == "KDE Plot":
                        sns.kdeplot(df[col_selected].dropna(), shade=True, ax=ax)
                        ax.set_title(f"KDE Plot of {col_selected}")

                st.pyplot(fig)

    else:
        st.error("❌ Error loading the dataset.")
else:
    st.info("📥 Please upload a CSV file to get started.")
