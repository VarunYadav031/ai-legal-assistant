import pandas as pd

def extract_table_insights(file):

    df = pd.read_excel(file)

    insights = {
        "columns": list(df.columns),
        "rows": len(df),
        "summary": df.describe(include='all').to_string()
    }

    return insights