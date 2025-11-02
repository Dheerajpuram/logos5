import pandas as pd
from prophet import Prophet
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import uuid

def detect_plotting_intent(query: str) -> bool:
    """Detects if the user's query contains keywords related to plotting or forecasting."""
    plotting_keywords = ["forecast", "plot", "graph", "predict", "project", "trend"]
    return any(keyword in query.lower() for keyword in plotting_keywords)

def generate_forecast_plot(df: pd.DataFrame, file_name: str) -> dict:
    """Generates a forecast plot from a DataFrame and returns the image path and summary."""
    try:
        df.columns = df.columns.str.strip()
        df['ds'] = pd.to_datetime(df['ds'])
    except Exception as e:
        return {"error": f"Failed to format data for forecasting: {e}"}

    try:
        model = Prophet()
        model.fit(df)
        future = model.make_future_dataframe(periods=365)
        forecast = model.predict(future)
    except Exception as e:
        return {"error": f"Failed to generate forecast: {e}"}

    try:
        # Create a new figure for the plot
        fig = model.plot(forecast, figsize=(12, 6))
        ax = fig.gca()
        ax.set_title(f"Forecast for {file_name}", fontsize=14, fontweight='bold')
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Value", fontsize=12)
        plt.tight_layout()

        plot_filename = f"forecast_{uuid.uuid4()}.png"
        # Save plots to a temporary directory outside the frontend
        temp_plot_dir = os.path.join("/Users/dheeraj/Desktop/finalmp", "temp_plots")
        plot_path_for_backend = os.path.join(temp_plot_dir, plot_filename)
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(plot_path_for_backend), exist_ok=True)
        
        # Save the figure with high DPI
        plt.savefig(plot_path_for_backend, dpi=100, bbox_inches='tight')
        plt.close(fig)
        
        # Verify the file was created
        if not os.path.exists(plot_path_for_backend):
            return {"error": "Failed to save plot image file."}

        # The frontend will fetch this image from a new backend endpoint
        plot_path_for_frontend = f"/api/plots/{plot_filename}"

        summary = f"Forecast generated for the next 365 days. The model predicts a value of {forecast['yhat'].iloc[-1]:.2f} on {forecast['ds'].iloc[-1].strftime('%Y-%m-%d')}."

        return {"answer": summary, "image_path": plot_path_for_frontend}
    except Exception as e:
        # Make sure to close any open figures on error
        plt.close('all')
        return {"error": f"Failed to generate or save plot: {e}"}
