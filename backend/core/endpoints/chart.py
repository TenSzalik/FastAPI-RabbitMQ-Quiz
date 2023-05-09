from fastapi import APIRouter
from core.managers.chart_manager import (
    DataCategoryChart,
    DataPointsChart,
    GenerateChart,
)
from core.models.schemas import ChartSchema

router = APIRouter(
    prefix="/chart",
    tags=["chart"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
def create_chart(queue_smooth_data: ChartSchema):
    list_categories = list(queue_smooth_data.queue_smooth_data.keys())
    list_values = list(queue_smooth_data.queue_smooth_data.values())
    category = DataCategoryChart(list_categories)
    points = DataPointsChart(list_values)
    chart = GenerateChart(category, points)
    chart.generate_chart()
    return "Chart was created"
