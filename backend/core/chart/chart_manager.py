from dataclasses import dataclass
import plotly.graph_objects as go


@dataclass
class DataCategoryChart:
    category: list[str]


@dataclass
class DataPointsChart:
    points: list[int]


class GenerateChart:
    def __init__(self, category: DataCategoryChart, points: DataPointsChart):
        assert isinstance(category, DataCategoryChart)
        assert isinstance(points, DataPointsChart)
        self.category = category
        self.points = points

    def generate_chart(self):
        fig = go.Figure()

        fig.add_trace(
            go.Scatterpolar(
                r=self.points.points,
                theta=self.category.category,
                fill="toself",
                name="A",
            )
        )
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10])), showlegend=False
        )
        fig.show()
