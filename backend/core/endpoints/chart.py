from fastapi import APIRouter
from core.managers.chart_manager import (
    DataChart,
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
    data = DataChart(list_categories, list_values)
    chart = GenerateChart(data)
    return chart.generate_chart()
