import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import os

OUTPUT_FOLDER = os.path.join(os.getcwd(), "data", "processed")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def generate_visualizations(df, filename="report"):
    paths = []

    try:
        # 1. Missing Values Chart
        plt.figure()
        df.isnull().sum().plot(kind='bar')
        plt.title("Missing Values")
        path1 = os.path.join(OUTPUT_FOLDER, f"{filename}_missing.png")
        plt.savefig(path1)
        plt.close()
        paths.append(path1)

        # 2. Distribution Plot (first numeric column)
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        if len(numeric_cols) > 0:
            col = numeric_cols[0]
            plt.figure()
            sns.histplot(df[col], kde=True)
            plt.title(f"Distribution of {col}")
            path2 = os.path.join(OUTPUT_FOLDER, f"{filename}_dist.png")
            plt.savefig(path2)
            plt.close()
            paths.append(path2)

        # 3. Correlation Heatmap
        if len(numeric_cols) > 1:
            plt.figure(figsize=(6, 4))
            sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm")
            plt.title("Correlation Heatmap")
            path3 = os.path.join(OUTPUT_FOLDER, f"{filename}_corr.png")
            plt.savefig(path3)
            plt.close()
            paths.append(path3)

        # Validate generated files
        valid_paths = []
        for path in paths:
            if os.path.exists(path):
                valid_paths.append(path)
            else:
                print(f"Warning: Plot not saved at {path}")

        return {
            "status": "success",
            "plots": valid_paths
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
        return {
            "status": "error",
            "message": str(e)
        }