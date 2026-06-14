from datetime import datetime

from fastapi import HTTPException, status

from app.models import AppointmentStatus, CoachReview
from app.schemas import CoachReviewCreate, CoachReviewRead
from app.store import appointments, coaches, next_id, reviews, students


def review_to_read(review: CoachReview) -> CoachReviewRead:
    student = students[review.student_id]
    coach = coaches[review.coach_id]
    return CoachReviewRead(
        id=review.id,
        appointment_id=review.appointment_id,
        student_id=student.id,
        student_name=student.name,
        coach_id=coach.id,
        coach_name=coach.name,
        rating=review.rating,
        feedback=review.feedback,
        created_at=review.created_at,
    )


def list_reviews(coach_id: int | None = None, student_id: int | None = None) -> list[CoachReviewRead]:
    values = sorted(reviews.values(), key=lambda item: item.created_at, reverse=True)
    if coach_id is not None:
        values = [item for item in values if item.coach_id == coach_id]
    if student_id is not None:
        values = [item for item in values if item.student_id == student_id]
    return [review_to_read(item) for item in values]


def get_review_by_appointment(appointment_id: int) -> CoachReviewRead | None:
    for review in reviews.values():
        if review.appointment_id == appointment_id:
            return review_to_read(review)
    return None


def create_review(appointment_id: int, payload: CoachReviewCreate) -> CoachReviewRead:
    appointment = appointments.get(appointment_id)
    if not appointment:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Appointment not found")

    if appointment.status != AppointmentStatus.completed:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Only completed appointments can be reviewed",
        )

    existing = get_review_by_appointment(appointment_id)
    if existing:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "This appointment has already been reviewed",
        )

    review = CoachReview(
        id=next_id("review"),
        appointment_id=appointment_id,
        student_id=appointment.student_id,
        coach_id=appointment.coach_id,
        rating=payload.rating,
        feedback=payload.feedback,
        created_at=datetime.now(),
    )
    reviews[review.id] = review
    return review_to_read(review)


def get_coach_avg_rating(coach_id: int) -> float:
    coach_reviews = [r for r in reviews.values() if r.coach_id == coach_id]
    if not coach_reviews:
        return 0.0
    return round(sum(r.rating for r in coach_reviews) / len(coach_reviews), 1)
