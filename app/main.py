# from fastapi import FastAPI, Depends, HTTPException
# from pydantic import BaseModel
# from langgraph.types import Command

# from app.graph.graph import graph
# from app.core.auth import get_current_user
# from app.core.security import (
#     verify_password,
#     create_access_token
# )


# app = FastAPI()


# # =========================
# # Request Models
# # =========================

# class TravelRequest(BaseModel):

#     query: str
#     thread_id: str


# class LoginRequest(BaseModel):

#     user_id: str
#     password: str


# class ClarificationRequest(BaseModel):

#     answer: str
#     thread_id: str


# # =========================
# # LOGIN
# # =========================

# @app.post("/auth/login")
# async def login(req: LoginRequest):

#     # Demo user
#     stored_user_id = "101"

#     # This must be a REAL bcrypt hash
#     stored_password_hash = "$2b$12$AKM8zFnU/vVNsjEXhH2MbOwThK6XR6ICrZzu8eEZwRIwBnuJoEegq"

#     if req.user_id != stored_user_id:

#         raise HTTPException(
#             status_code=401,
#             detail="Invalid credentials"
#         )

#     if not verify_password(
#         req.password,
#         stored_password_hash
#     ):

#         raise HTTPException(
#             status_code=401,
#             detail="Invalid credentials"
#         )

#     access_token = create_access_token(
#         user_id=stored_user_id
#     )

#     return {
#         "access_token": access_token,
#         "token_type": "bearer"
#     }


# # =========================
# # PLAN TRIP
# # =========================

# @app.post("/trips/plan")
# async def plan_trip(
#     req: TravelRequest,
#     current_user: str = Depends(get_current_user)
# ):

#     # Make thread user-specific
#     thread_id = f"{current_user}_{req.thread_id}"

#     config = {
#         "configurable": {
#             "thread_id": thread_id
#         }
#     }

#     result = graph.invoke(
#         {
#             "user_query": req.query
#         },
#         config=config
#     )

#     # =========================
#     # HUMAN CLARIFICATION
#     # =========================

#     if result.get("missing_fields"):

#         return {
#             "status": "needs_clarification",
#             "missing_fields": result.get(
#                 "missing_fields",
#                 []
#             ),
#             "question": result.get(
#                 "clarification_question"
#             )
#         }

#     # =========================
#     # SUCCESS
#     # =========================

#     return {
#         "status": "success",

#         "destination":
#             result.get("destination"),

#         "transport":
#             result.get("best_transport"),

#         "hotels":
#             result.get("hotels"),

#         "budget":
#             result.get("budget"),

#         "total_budget":
#             result.get("total_budget"),

#         "itinerary":
#             result.get("itinerary")
#     }


# # =========================
# # CLARIFICATION / RESUME
# # =========================

# # We'll implement this next after JWT

# @app.post("/trips/clarify")
# async def clarify_trip(
#     req: ClarificationRequest,
#     current_user: str = Depends(get_current_user)
# ):

#     thread_id = f"{current_user}_{req.thread_id}"

#     config = {
#         "configurable": {
#             "thread_id": thread_id
#         }
#     }

#     result = graph.invoke(
#         Command(resume=req.answer),
#         config=config
#     )

#     return result

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from langgraph.types import Command

from app.graph.graph import graph
from app.core.auth import get_current_user
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database.connection import engine
from app.database.connection import Base, engine
from app.database.models import User, Trip
from app.database.connection import get_db

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.logging_config import setup_logging
from app.core.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    global_exception_handler,
)
setup_logging()

app = FastAPI(
    title="AI Travel Planner API",
    description="AI-powered travel planning system using LangGraph",
    version="1.0.0"
)
app.add_exception_handler(
    StarletteHTTPException,
    http_exception_handler
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

app.add_exception_handler(
    Exception,
    global_exception_handler
)
import time
import uuid

from fastapi import Request


@app.middleware("http")
async def logging_middleware(
    request: Request,
    call_next
):
    request_id = str(uuid.uuid4())
    start_time = time.perf_counter()

    logger.info(
        "Request started | request_id=%s method=%s path=%s",
        request_id,
        request.method,
        request.url.path,
    )

    try:
        response = await call_next(request)

        duration = time.perf_counter() - start_time

        response.headers["X-Request-ID"] = request_id

        logger.info(
            "Request completed | request_id=%s status=%s duration=%.3fs",
            request_id,
            response.status_code,
            duration,
        )

        return response

    except Exception:
        duration = time.perf_counter() - start_time

        logger.exception(
            "Request failed | request_id=%s duration=%.3fs",
            request_id,
            duration,
        )

        raise
    
Base.metadata.create_all(bind=engine)

# =========================================================
# REQUEST MODELS
# =========================================================

class LoginRequest(BaseModel):
    user_id: str
    password: str


class TravelRequest(BaseModel):

    query: str = Field(
        ...,
        min_length=3,
        description="Travel request"
    )

    thread_id: str = Field(
        ...,
        min_length=1
    )


class ClarificationRequest(BaseModel):

    answer: str = Field(
        ...,
        min_length=1
    )

    thread_id: str = Field(
        ...,
        min_length=1
    )

class RegisterRequest(BaseModel):
    user_id: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)

# =========================================================
# RESPONSE MODELS
# =========================================================

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

class TripHistoryItem(BaseModel):
    id: int
    destination: str | None = None
    duration_days: int | None = None
    transport: str | None = None
    total_budget: float | None = None
    itinerary: str | None = None
    created_at: datetime | None = None


class TripHistoryResponse(BaseModel):
    count: int
    trips: list[TripHistoryItem]

class TripResponse(BaseModel):
    status: str
    missing_fields: list[str] = Field(default_factory=list)
    question: str | None = None

    destination: str | None = None

    transport: dict | str | None = None

    hotels: list = Field(default_factory=list)

    budget: dict | None = None

    total_budget: float | None = None

    itinerary: dict | str | None = None

# =========================================================
# HELPER FUNCTIONS
# =========================================================

def build_config(current_user: str, thread_id: str):

    user_thread_id = f"{current_user}_{thread_id}"

    return {
        "configurable": {
            "thread_id": user_thread_id
        }
    }


def format_trip_response(result: dict):

    # ==========================================
    # Graph paused again
    # ==========================================

    interrupts = result.get("__interrupt__")

    if interrupts:

        interrupt_data = interrupts[0].value

        return {
            "status": "needs_clarification",

            "missing_fields": interrupt_data.get(
                "missing_fields",
                []
            ),

            "question": interrupt_data.get(
                "question",
                "Please provide more information."
            ),

            "destination": result.get(
                "destination"
            ),

            "transport": None,

            "hotels": [],

            "budget": None,

            "total_budget": None,

            "itinerary": None
        }

    # ==========================================
    # Missing fields
    # ==========================================

    if result.get("missing_fields"):

        return {
            "status": "needs_clarification",

            "missing_fields": result.get(
                "missing_fields",
                []
            ),

            "question": result.get(
                "clarification_question"
            ),

            "destination": result.get(
                "destination"
            ),

            "transport": None,

            "hotels": [],

            "budget": None,

            "total_budget": None,

            "itinerary": None
        }

    # ==========================================
    # Success
    # ==========================================

    return {
        "status": "success",

        "missing_fields": [],

        "question": None,

        "destination": result.get(
            "destination"
        ),

        "transport": result.get(
            "best_transport"
        ),

        "hotels": result.get(
            "hotels",
            []
        ),

        "budget": result.get(
            "budget"
        ),

        "total_budget": result.get(
            "total_budget"
        ),

        "itinerary": result.get(
            "itinerary"
        )
    }

#--------------------------register----------------

@app.post("/auth/register")
async def register(
    req: RegisterRequest,
    db: Session = Depends(get_db)
):

    existing_user = (
        db.query(User)
        .filter(User.user_id == req.user_id)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="User already exists"
        )

    password_hash = hash_password(req.password)

    user = User(
        user_id=req.user_id,
        password_hash=password_hash
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "User registered successfully",
        "user_id": user.user_id
    }

# =========================================================
# AUTHENTICATION
# =========================================================

@app.post("/auth/login", response_model=LoginResponse)
async def login(
    req: LoginRequest,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.user_id == req.user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
        req.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    access_token = create_access_token(
        user_id=user.user_id
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# =========================================================
# PLAN TRIP
# =========================================================

@app.post(
    "/trips/plan",
    response_model=TripResponse
)
async def plan_trip(
    req: TravelRequest,
    current_user: str = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    logger.info(
        "Trip planning started | user=%s | thread=%s",
        current_user,
        req.thread_id
    )

    config = build_config(
        current_user,
        req.thread_id
    )

    try:

        result = graph.invoke(
            {
                "user_query": req.query
            },
            config=config
        )
        result = graph.invoke(
            {"user_query": req.query},
            config=config
        )

        response_data = format_trip_response(result)

        logger.info(
            "Trip planning completed | user=%s | thread=%s",
            current_user,
            req.thread_id
        )

        if response_data["status"] == "success":

            trip = Trip(
                user_id=current_user,
                thread_id=req.thread_id,
                destination=response_data.get("destination"),
                duration_days=result.get("duration_days"),
                transport=str(response_data.get("transport")),
                total_budget=response_data.get("total_budget"),
                itinerary=str(response_data.get("itinerary"))
            )

            db.add(trip)
            db.commit()
            db.refresh(trip)
            print("✅ Trip saved:", trip.id)
        return response_data
    
    except Exception as e:

        logger.error(
            "Trip planning failed | user=%s | thread=%s",
            current_user,
            req.thread_id,
            exc_info=True
        )

        raise HTTPException(
            status_code=500,
            detail="Trip planning failed. Please try again."
        )


# =========================================================
# CLARIFICATION / HUMAN-IN-THE-LOOP
# =========================================================

@app.post(
    "/trips/clarify",
    response_model=TripResponse
)
async def clarify_trip(
    req: ClarificationRequest,
    current_user: str = Depends(
        get_current_user
    )
):

    logger.info(
        "Trip clarification | user=%s | thread=%s",
        current_user,
        req.thread_id
    )

    config = build_config(
        current_user,
        req.thread_id
    )

    try:

        result = graph.invoke(
            Command(
                resume=req.answer
            ),
            config=config
        )

        return format_trip_response(result)

    except Exception as e:

        logger.error(
            "Trip clarification failed | user=%s | thread=%s",
            current_user,
            req.thread_id,
            exc_info=True
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to continue trip planning."
        )

@app.get("/trips", response_model=TripHistoryResponse)
async def get_my_trips(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    trips = (
        db.query(Trip)
        .filter(Trip.user_id == current_user)
        .order_by(Trip.created_at.desc())
        .all()
    )

    return {
        "count": len(trips),
        "trips": [
            {
                "id": trip.id,
                "destination": trip.destination,
                "duration_days": trip.duration_days,
                "transport": trip.transport,
                "total_budget": trip.total_budget,
                "itinerary": trip.itinerary,
                "created_at": trip.created_at
            }
            for trip in trips
        ]
    }
