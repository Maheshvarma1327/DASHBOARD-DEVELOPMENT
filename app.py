import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("dataset.csv", parse_dates=["Date"])

# App initialization
app = dash.Dash(__name__)
app.title = "Retail Sales Dashboard"

# Layout
app.layout = html.Div([
    html.H1("📊 Retail Dashboard", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Select Region:"),
        dcc.Dropdown(
            options=[{"label": r, "value": r} for r in df["Region"].unique()],
            id="region-filter",
            value=df["Region"].unique()[0],
            clearable=False
        ),
    ], style={"width": "30%", "margin": "10px"}),

    dcc.Graph(id="sales-over-time"),
    dcc.Graph(id="category-pie"),
    dcc.Graph(id="profit-bar")
])

# Callbacks for interactivity
@app.callback(
    [Output("sales-over-time", "figure"),
     Output("category-pie", "figure"),
     Output("profit-bar", "figure")],
    [Input("region-filter", "value")]
)
def update_dashboard(selected_region):
    filtered = df[df["Region"] == selected_region]

    # Line chart - Sales over time
    fig1 = px.line(filtered, x="Date", y="Sales", title="Sales Over Time")

    # Pie chart - Category distribution
    fig2 = px.pie(filtered, names="Category", values="Sales", title="Sales by Category")

    # Bar chart - Profit by category
    fig3 = px.bar(filtered, x="Category", y="Profit", title="Profit by Category", color="Category")

    return fig1, fig2, fig3

# Run the server
if __name__ == '__main__':
    app.run(debug=True)
