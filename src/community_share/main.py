from __future__ import annotations

from datetime import UTC, datetime

try:
    from fastapi import FastAPI
except ImportError:  # pragma: no cover - demo fallback when FastAPI is unavailable.
    FastAPI = None

from .models import Listing, ListingType, Request, User
from .services import MatchingEngine


if FastAPI is not None:
    app = FastAPI(title="Community Share Demo")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/demo/matches")
    def demo_matches() -> dict[str, object]:
        request_time = datetime.now(UTC)
        users = {
            "u1": User("u1", "Alice", "AB12", interests={ListingType.BOOK}),
            "u2": User("u2", "Bob", "AB22", interests={ListingType.BOOK}),
        }
        listings = [
            Listing(
                listing_id="l1",
                owner_id="u1",
                title="Python in Practice",
                listing_type=ListingType.BOOK,
                quantity=1,
                created_at=request_time,
            )
        ]
        requests = [
            Request(
                request_id="r1",
                requester_id="u2",
                listing_type=ListingType.BOOK,
                quantity=1,
                max_distance_km=30,
                created_at=request_time,
            )
        ]
        matches = MatchingEngine().match_requests(users, listings, requests, request_time)
        return {"matches": [match.__dict__ for match in matches]}
else:
    app = None
