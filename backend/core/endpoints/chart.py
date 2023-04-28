from fastapi import Cookie, APIRouter
from core.chart.chart_manager import DataCategoryChart, DataPointsChart, GenerateChart
from core.utils.get_sum_dicts import get_sum_dicts
from core.utils.consume_queue import consume_queue
from core.schemas.schemas import QueueCreateSchema

router = APIRouter(
    prefix="/chart",
    tags=["chart"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=QueueCreateSchema)
def create_chart(queue: QueueCreateSchema):
    quiz_data = consume_queue(queue.queue)
    sum_quiz_data = get_sum_dicts(quiz_data)
    list_categories = list(sum_quiz_data.keys())
    list_values = list(sum_quiz_data.values())
    cat = DataCategoryChart(list_categories)
    poi = DataPointsChart(list_values)
    chart = GenerateChart(cat, poi)
    chart.generate_chart()
    return {"queue": queue.queue}
