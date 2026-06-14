from fastapi import APIRouter, HTTPException, status

from app.models import Coach
from app.schemas import CoachCreate, CoachRead, CoachReadWithRating
from app.services.reviews import get_coach_avg_rating
from app.store import coaches, next_id, reviews

router = APIRouter()


@router.get("", response_model=list[CoachRead])
def list_coaches(active: bool | None = None) -> list[Coach]:
    values = list(coaches.values())
    if active is not None:
        values = [coach for coach in values if coach.active == active]
    return values


@router.get("/{coach_id}", response_model=CoachReadWithRating)
def get_coach(coach_id: int) -> CoachReadWithRating:
    coach = coaches.get(coach_id)
    if not coach:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Coach not found")
    avg_rating = get_coach_avg_rating(coach_id)
    review_count = sum(1 for r in reviews.values() if r.coach_id == coach_id)
    return CoachReadWithRating(
        **coach.model_dump(),
        avg_rating=avg_rating,
        review_count=review_count,
    )


@router.post("", response_model=CoachRead, status_code=201)
def create_coach(payload: CoachCreate) -> Coach:
    coach = Coach(id=next_id("coach"), **payload.model_dump())
    coaches[coach.id] = coach
    return coach


@router.patch("/{coach_id}/active", response_model=CoachRead)
def update_coach_active(coach_id: int, active: bool) -> Coach:
    coach = coaches.get(coach_id)
    if not coach:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Coach not found")
    coach.active = active
    coaches[coach.id] = coach
    return coach
