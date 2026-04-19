import pandas as pd
from models.visualization import generate_visualizations

def process_csv(file_path):
    try:
        # Load dataset with encoding handling
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, encoding='latin1')

        original_shape = df.shape

        # Cleaning
        df = df.drop_duplicates()
        df = df.fillna(df.mean(numeric_only=True))

        df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

        # Summary
        summary = {
            "rows": df.shape[0],
            "columns": df.shape[1],
            "original_rows": original_shape[0],
            "duplicates_removed": original_shape[0] - df.shape[0]
        }

        # Generate visual reports
        visuals = generate_visualizations(df)

        return {
            "status": "success",
            "data_preview": df.head().to_dict(),
            "summary": summary,
            "visualizations": visuals.get("plots", []),
            "message": "CSV processed with visual reports"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }