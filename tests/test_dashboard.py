"""Local regressions; these tests do not connect to a Snowflake account."""

import json
import unittest
from pathlib import Path
from unittest.mock import patch

import plotly.graph_objects as go
from streamlit.testing.v1 import AppTest

from chart_display import display_chart

ROOT = Path(__file__).resolve().parents[1]


class ChartCompatibilityTests(unittest.TestCase):
    def test_new_streamlit_receives_alt_text(self):
        calls = []

        def render(figure, *, width, alt):
            calls.append((figure, width, alt))

        figure = go.Figure()
        with patch("chart_display.st.plotly_chart", render), patch(
            "chart_display.st.caption"
        ) as caption:
            display_chart(figure, description="Chart description")

        self.assertEqual(calls, [(figure, "stretch", "Chart description")])
        caption.assert_not_called()

    def test_warehouse_streamlit_uses_caption_without_new_arguments(self):
        calls = []

        def render(figure, *, width):
            calls.append((figure, width))

        figure = go.Figure()
        with patch("chart_display.st.plotly_chart", render), patch(
            "chart_display.st.caption"
        ) as caption:
            display_chart(figure, description="Chart description")

        self.assertEqual(calls, [(figure, "stretch")])
        caption.assert_called_once_with("Chart description")


class DashboardTests(unittest.TestCase):
    def test_three_charts_render_and_radial_values_are_stable_on_rerun(self):
        app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=20).run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(app.title[0].value, "Infografía Radial en Streamlit")
        self.assertEqual(len(app.subheader), 2)
        self.assertIn("datos sintéticos", app.caption[1].value)
        charts = app.get("plotly_chart")
        self.assertEqual(len(charts), 3)
        radial = json.loads(charts[0].proto.spec)
        self.assertEqual(len(radial["data"]), 2)
        self.assertEqual([trace["base"] for trace in radial["data"]], [32, 6])
        self.assertTrue(all(len(trace["theta"]) == 100 for trace in radial["data"]))
        self.assertEqual(len(json.loads(charts[1].proto.spec)["data"]), 1)
        self.assertEqual(len(json.loads(charts[2].proto.spec)["data"]), 2)

        app.run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(json.loads(app.get("plotly_chart")[0].proto.spec), radial)


if __name__ == "__main__":
    unittest.main()
