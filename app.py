import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from eda_tool.data_loader import load_data
from eda_tool.eda_summary import dataset_summary
from eda_tool.missing_values import plot_missing_values
from eda_tool.visualization import (
    plot_histograms, plot_correlation_matrix, plot_countplots, 
    plot_boxplots, plot_violinplots, plot_pairplot, plot_kde
)

# Streamlit Page Config
st.set_page_config(page_title="EDA Made Easy", layout="wide")

# App Title
st.title("📊 EDA MADE EASY")
st.markdown("#### _By Stark")
st.markdown("---")

# Sidebar for File Upload
st.sidebar.header("📂 Upload Your Dataset")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    df = load_data(uploaded_file)

    if df is not None:
        st.sidebar.success("✅ Dataset Loaded Successfully!")
        
        # Sidebar Navigation
        st.sidebar.header("🔎 Explore Sections")
        section = st.sidebar.radio(
            "Select Analysis Section",
            (
                "Dataset Overview",
                "Missing Values",
                "Visualizations"
            )
        )

        if section == "Dataset Overview":
            st.header("📑 Dataset Overview")
            st.write("Use the expanders below to explore your dataset details:")

            with st.expander("🔢 Dataset Shape"):
                st.write(f"Shape: {df.shape}")

            with st.expander("📝 Column Names"):
                st.write(f"Columns: {list(df.columns)}")

            with st.expander("📉 Data Types"):
                st.write(df.dtypes)

            with st.expander("📈 Summary Statistics"):
                st.write(df.describe())

        elif section == "Missing Values":
            st.header("🚨 Missing Values Analysis")
            with st.expander("🔎 Show Missing Value Count"):
                st.write(df.isnull().sum())
            with st.expander("🗺️ Missing Values Heatmap"):
                st.pyplot(plot_missing_values(df))

        elif section == "Visualizations":
            st.header("📊 Data Visualizations")

            # Multi-select for visualizations
            viz_options = st.multiselect(
                "Select Visualizations to Display:",
                [
                    "Histograms",
                    "Correlation Matrix",
                    "Count Plots",
                    "Box Plots",
                    "Violin Plots",
                    "Pair Plot",
                    "KDE Plots"
                ]
            )

            if "Histograms" in viz_options:
                st.subheader("📊 Feature Distributions (Histogram)")
                st.pyplot(plot_histograms(df))

            if "Correlation Matrix" in viz_options:
                st.subheader("🔗 Correlation Matrix")
                st.pyplot(plot_correlation_matrix(df))

            if "Count Plots" in viz_options:
                st.subheader("🧮 Count Plots (Categorical Features)")
                for fig in plot_countplots(df):
                    st.pyplot(fig)

            if "Box Plots" in viz_options:
                st.subheader("📦 Box Plots for Outlier Detection")
                for fig in plot_boxplots(df):
                    st.pyplot(fig)

            if "Violin Plots" in viz_options:
                st.subheader("🎻 Violin Plots")
                for fig in plot_violinplots(df):
                    st.pyplot(fig)

            if "Pair Plot" in viz_options:
                st.subheader("🔄 Pair Plot (Feature Relationships)")
                st.pyplot(plot_pairplot(df))

            if "KDE Plots" in viz_options:
                st.subheader("🌊 KDE (Density) Plots")
                for fig in plot_kde(df):
                    st.pyplot(fig)

    else:
        st.error("❌ Error while loading the dataset.")
else:
    st.info("📥 Please upload a CSV file to get started.")
