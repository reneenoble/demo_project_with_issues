from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

from .models import Listing, Request, User


def _postal_distance(postal_a: str, postal_b: str) -> int:
    # A placeholder distance function for demo data.
    return abs(sum(ord(c) for c in postal_a) - sum(ord(c) for c in postal_b)) % 40


@dataclass(slots=True)
class Match:
    listing_id: str
    request_id: str
    allocated_quantity: int
    distance_km: int


class MatchingEngine:
    """Greedy matching for community resource sharing."""

    def match_requests(
        self,
        users: dict[str, User],
        listings: Iterable[Listing],
        requests: Iterable[Request],
        now: datetime,
    ) -> list[Match]:
        active_listings = [item for item in listings if item.is_active(now)]
        request_queue = sorted(requests, key=lambda req: req.created_at)
        results: list[Match] = []

        for request in request_queue:
            requester = users.get(request.requester_id)
            if requester is None:
                continue

            remaining = request.quantity
            for listing in active_listings:
                if remaining <= 0:
                    break
                if listing.listing_type != request.listing_type or listing.quantity <= 0:
                    continue

                owner = users.get(listing.owner_id)
                if owner is None:
                    continue

                distance = _postal_distance(requester.postal_code, owner.postal_code)
                if distance > request.max_distance_km:
                    continue

                allocated = min(remaining, listing.quantity)
                listing.quantity -= allocated
                remaining -= allocated
                results.append(
                    Match(
                        listing_id=listing.listing_id,
                        request_id=request.request_id,
                        allocated_quantity=allocated,
                        distance_km=distance,
                    )
                )

        return results
