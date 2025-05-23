from preswald import connect, get_df, table, text, plotly, sidebar
import plotly.express as px
import pandas as pd


# -------------------
# 🔌 Load and Prepare Data
# -------------------
connect()
df = get_df("tesla_sales")

# Clean numeric fields
df["sold_price"] = df["sold_price"].str.replace(",", "").astype(float)
df["miles"] = df["miles"].str.replace(",", "").astype(float)

# -------------------
# 📊 Intro & Summary
# -------------------
text("# Tesla Sales Report 🚗")
text("This dashboard explores trends in used Tesla sales data — including pricing, mileage, model performance, and geographic distribution.")

# -------------------
# 🔍 Filtered Data for Analysis
# -------------------
filtered_df = df[(df["sold_price"] > 10000) & (df["miles"].notnull())]

text("## 📈 Miles vs Sold Price")
text("Explore how mileage impacts resale value across Tesla models.")
fig = px.scatter(
    filtered_df,
    x="miles",
    y="sold_price",
    color="model",
    title="Miles vs. Sold Price"
)
plotly(fig)

# -------------------
# 💰 Average Price by Model
# -------------------
text("## 💸 Average Sold Price by Model")
avg_price_by_model = df.groupby("model")["sold_price"].mean().reset_index()
fig1 = px.bar(
    avg_price_by_model,
    x="model",
    y="sold_price",
    title="Average Sold Price by Model",
    labels={"sold_price": "Average Price (USD)", "model": "Tesla Model"}
)
plotly(fig1)

# -------------------
# 🔧 Price by Trim
# -------------------
text("## 🔩 Price Trends by Trim")
fig2 = px.scatter(
    df,
    x="miles",
    y="sold_price",
    color="trim",
    title="Miles vs. Sold Price by Trim",
    hover_data=["model", "year"]
)
plotly(fig2)

# -------------------
# 🧭 Model Revenue Breakdown
# -------------------
text("## 🧱 Revenue Breakdown by Model and Trim")
fig_treemap = px.treemap(
    df,
    path=["model", "trim"],
    values="sold_price",
    title="Sales Revenue Breakdown by Model and Trim",
)
plotly(fig_treemap)

# -------------------
# 🌀 Year → Model → Trim Breakdown
# -------------------
text("## 🌞 Sunburst: Year → Model → Trim")
fig_sunburst = px.sunburst(
    df,
    path=["year", "model", "trim"],
    values="sold_price",
    title="Tesla Sales Breakdown by Year > Model > Trim"
)
plotly(fig_sunburst)

# -------------------
# 📦 Price Distribution
# -------------------
text("## 📦 Sold Price Distribution by Model")
fig_box = px.box(
    df,
    x="model",
    y="sold_price",
    color="model",
    title="Price Distribution by Tesla Model"
)
plotly(fig_box)

# -------------------
# 🧪 Mileage Distribution
# -------------------
text("## 🧪 Mileage Distribution by Model")
fig_violin = px.violin(
    df,
    x="model",
    y="miles",
    box=True,
    points="all",
    title="Mileage Distribution by Tesla Model"
)
plotly(fig_violin)

# -------------------
# 🗺️ Geographic Sales by State
# -------------------
if "state" in df.columns:
    text("## 🗺️ Tesla Sales Across the U.S.")
    state_sales = df["state"].value_counts().reset_index()
    state_sales.columns = ["state", "num_sales"]

    fig_state_map = px.choropleth(
        state_sales,
        locations="state",  # Must be 2-letter codes
        locationmode="USA-states",
        color="num_sales",
        scope="usa",
        color_continuous_scale="Blues",
        title="Number of Tesla Sales by State"
    )
    plotly(fig_state_map)
else:
    text("⚠️ State column not found. Skipping map.")
