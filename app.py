import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from chart_display import display_chart

# Snowflake does not support the page_title, page_icon or menu_items settings.
st.set_page_config(layout="wide")
st.title("Infografía Radial en Streamlit")
st.caption("Vista reproducible con un gráfico radial y dos resúmenes inferiores")
st.caption("Demostración con datos sintéticos; no consulta tablas de Snowflake.")

# A fixed seed keeps the dashboard stable between Streamlit reruns.
rng = np.random.default_rng(42)
categories = [f"Elemento {index}" for index in range(1, 101)]
primary_values = rng.integers(10, 100, size=100)
secondary_values = rng.integers(5, 30, size=100)

# Normalize both metrics into separate radial bands while preserving raw values
# in the tooltip. This creates two actual rings instead of overlapping traces.
primary_radius = 32 + (primary_values / primary_values.max()) * 60
secondary_radius = 6 + (secondary_values / secondary_values.max()) * 20

radial_figure = go.Figure()
radial_figure.add_trace(
    go.Barpolar(
        r=primary_radius - 32,
        base=32,
        theta=categories,
        customdata=primary_values,
        name="Métrica principal",
        marker_color="#d4847c",
        marker_line_color="#ffffff",
        marker_line_width=0.35,
        hovertemplate="%{theta}<br>Métrica principal: %{customdata}<extra></extra>",
    )
)
radial_figure.add_trace(
    go.Barpolar(
        r=secondary_radius - 6,
        base=6,
        theta=categories,
        customdata=secondary_values,
        name="Métrica secundaria",
        marker_color="#9cb5bd",
        marker_line_color="#ffffff",
        marker_line_width=0.35,
        hovertemplate="%{theta}<br>Métrica secundaria: %{customdata}<extra></extra>",
    )
)
radial_figure.update_layout(
    polar={
        "hole": 0.28,
        "bgcolor": "rgba(0, 0, 0, 0)",
        "radialaxis": {"visible": False, "range": [0, 96]},
        "angularaxis": {
            "tickmode": "array",
            "tickvals": categories[::10],
            "ticktext": categories[::10],
            "tickfont": {"size": 10, "color": "#5f6368"},
            "showgrid": False,
            "showline": False,
        },
    },
    height=700,
    margin={"l": 40, "r": 40, "t": 40, "b": 40},
    legend={"orientation": "h", "x": 0.5, "xanchor": "center", "y": -0.08},
)

display_chart(
    radial_figure,
    description="Dos anillos radiales comparan las métricas principal y secundaria de cien elementos.",
)

left_column, right_column = st.columns(2)

with left_column:
    st.subheader("Categorías principales")
    bubble_data = pd.DataFrame(
        {
            "Categoria": ["Cat A", "Cat B", "Cat C", "Cat D", "Cat E"],
            "Y": [1.0, 1.7, 1.2, 2.1, 1.5],
            "Cantidad": [28, 54, 38, 74, 46],
        }
    )
    bubble_figure = px.scatter(
        bubble_data,
        x="Categoria",
        y="Y",
        size="Cantidad",
        size_max=52,
        color_discrete_sequence=["#d4847c"],
        hover_data={"Y": False, "Cantidad": True},
    )
    bubble_figure.update_layout(height=350, margin={"l": 20, "r": 20, "t": 20, "b": 20})
    bubble_figure.update_yaxes(visible=False)
    bubble_figure.update_xaxes(title=None, showgrid=False)
    display_chart(
        bubble_figure,
        description="Cinco burbujas comparan la cantidad de las categorías A a E.",
    )

with right_column:
    st.subheader("Evolución acumulada")
    area_data = pd.DataFrame(
        {
            "Mes": ["Ene", "Feb", "Mar", "Abr", "May"] * 2,
            "Valor": [12, 24, 39, 58, 82, 8, 18, 31, 45, 63],
            "Tipo": ["Serie 1"] * 5 + ["Serie 2"] * 5,
        }
    )
    area_figure = px.area(
        area_data,
        x="Mes",
        y="Valor",
        color="Tipo",
        color_discrete_sequence=["#8c8c8c", "#b8746d"],
    )
    area_figure.update_layout(
        height=350,
        margin={"l": 20, "r": 20, "t": 20, "b": 20},
        yaxis_title=None,
        xaxis_title=None,
        legend_title=None,
    )
    display_chart(
        area_figure,
        description="Dos áreas muestran el crecimiento acumulado de enero a mayo.",
    )
