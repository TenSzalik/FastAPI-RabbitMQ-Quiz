from fastapi import APIRouter
from core.chart.chart_manager import DataCategoryChart, DataPointsChart, GenerateChart
from core.schemas.schemas import ChartSchema

router = APIRouter(
    prefix="/chart",
    tags=["chart"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
def create_chart(queue_smooth_data: ChartSchema):
    list_categories = list(queue_smooth_data.queue_smooth_data.keys())
    list_values = list(queue_smooth_data.queue_smooth_data.values())
    cat = DataCategoryChart(list_categories)
    poi = DataPointsChart(list_values)
    chart = GenerateChart(cat, poi)
    chart.generate_chart()
    return "Chart was created"
