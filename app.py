from flask import Flask, render_template, request
import plotly.express as px
import pandas as pd
import json
import plotly

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    # Get the selected chart type from the dropdown menu (default to "box")
    chart_type = request.form.get("chart_type", "box")

    # Load coffee export data
    df = pd.read_csv("coffee_exports.csv")

    # Ensure numeric columns are properly formatted
    df['Export_Value_USD'] = df['Export_Value_USD'].astype(float)
    df['Export_Tons'] = df['Export_Tons'].astype(float)

    # Create visualization based on chart type
    if chart_type == "bar":
        # Aggregate data for bar chart (sum export values by country and region)
        aggregated_df = df.groupby(['Country', 'Region'], as_index=False).sum()
        fig = px.bar(
            aggregated_df,
            x="Country",
            y="Export_Value_USD",
            color="Region",
            title="Coffee Export Values by Country (USD)"
        )
    elif chart_type == "scatter":
        # Scatter plot showing export tons vs export values
        fig = px.scatter(
            df,
            x="Export_Tons",
            y="Export_Value_USD",
            color="Region",
            size="Export_Tons",
            hover_name="Country",
            title="Coffee Exports: Volume vs Value"
        )
    else:
        # Box plot showing export value distribution by region
        fig = px.box(
            df,
            x="Region",
            y="Export_Value_USD",
            color="Region",
            title="Regional Coffee Export Value Distribution"
        )

    # Apply dark theme formatting
    fig.update_layout(
        plot_bgcolor='#1a1c23',
        paper_bgcolor='#1a1c23',
        font_color='#ffffff',
        autosize=True,
        margin=dict(t=50, l=50, r=50, b=50),
        height=600
    )

    # Format axes for better readability
    fig.update_xaxes(showgrid=False, color='#cccccc', categoryorder="total descending")
    fig.update_yaxes(showgrid=False, color='#cccccc', tickprefix="$", tickformat=",.0f")

    # Convert Plotly figure to JSON for rendering in the frontend
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("index.html", graphJSON=graphJSON, chart_type=chart_type)


if __name__ == "__main__":
    app.run(debug=True)
