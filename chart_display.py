"""Render charts on both Snowflake's warehouse runtime and recent Streamlit."""

from inspect import signature

import plotly.graph_objects as go
import streamlit as st


def display_chart(figure: go.Figure, *, description: str) -> None:
    """Keep descriptions without passing newer arguments to older Streamlit."""
    if "alt" in signature(st.plotly_chart).parameters:
        st.plotly_chart(figure, width="stretch", alt=description)
    else:
        # Streamlit 1.52.2 has width, but not the explicit alt parameter.
        st.plotly_chart(figure, width="stretch")
        st.caption(description)
