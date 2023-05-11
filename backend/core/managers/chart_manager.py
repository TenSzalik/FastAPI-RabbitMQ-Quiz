from dataclasses import dataclass
import plotly.graph_objects as go
import plotly.io as pio


@dataclass
class DataChart:
    category: list[str]
    points: list[int]


class GenerateChart:
    def __init__(self, data: DataChart):
        assert isinstance(data, DataChart)
        self.category = data.category
        self.points = data.points

    def generate_chart(self):
        fig = go.Figure()

        fig.add_trace(
            go.Scatterpolar(
                r=self.points,
                theta=self.category,
                fill="toself",
                name="A",
            )
        )
        fig.update_layout(
            polar={"radialaxis": {"visible": True, "range": [0, 10]}}, showlegend=False
        )
        fig.show()
        html_str = pio.to_html(fig, include_plotlyjs="cdn", full_html=False)
        return html_str
