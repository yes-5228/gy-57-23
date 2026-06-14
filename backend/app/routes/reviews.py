from fastapi import APIRouter

from app.schemas import CoachReviewCreate, CoachReviewRead
from app.services.reviews import create_review, list_reviews

router = APIRouter()


@router.get("", response_model=list[CoachReviewRead])
def get_reviews(coach_id: int | None = None, student_id: int | None = None) -> list[CoachReviewRead]:
    return list_reviews(coach_id=coach_id, student_id=student_id)


@router.post("/appointments/{appointment_id}/review", response_model=CoachReviewRead, status_code=201)
def add_review(appointment_id: int, payload: CoachReviewCreate) -> CoachReviewRead:
    return create_review(appointment_id, payload)
