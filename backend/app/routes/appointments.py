from fastapi import APIRouter

from app.models import AppointmentStatus
from app.schemas import AppointmentCancel, AppointmentCreate, AppointmentRead, AppointmentReadWithReview
from app.services.appointments import (
    cancel_appointment,
    complete_appointment,
    create_appointment,
    get_appointment_with_review,
    list_appointments,
)

router = APIRouter()


@router.get("", response_model=list[AppointmentRead])
def get_appointments(status: AppointmentStatus | None = None) -> list[AppointmentRead]:
    return list_appointments(status)


@router.post("", response_model=AppointmentRead, status_code=201)
def book_appointment(payload: AppointmentCreate) -> AppointmentRead:
    return create_appointment(payload)


@router.get("/{appointment_id}", response_model=AppointmentReadWithReview)
def get_appointment(appointment_id: int) -> AppointmentReadWithReview:
    return get_appointment_with_review(appointment_id)


@router.post("/{appointment_id}/cancel", response_model=AppointmentRead)
def cancel(appointment_id: int, payload: AppointmentCancel) -> AppointmentRead:
    return cancel_appointment(appointment_id, payload.reason)


@router.post("/{appointment_id}/complete", response_model=AppointmentReadWithReview)
def complete(appointment_id: int) -> AppointmentReadWithReview:
    return complete_appointment(appointment_id)
