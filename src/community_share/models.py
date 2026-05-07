from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ListingType(str, Enum):
    BOOK = "book"
    EQUIPMENT = "equipment"
    VEGETABLE = "vegetable"


@dataclass(slots=True)
class User:
    user_id: str
    display_name: str
    postal_code: str
    trust_score: float = 0.5
    interests: set[ListingType] = field(default_factory=set)


@dataclass(slots=True)
class Listing:
    listing_id: str
    owner_id: str
    title: str
    listing_type: ListingType
    quantity: int
    created_at: datetime
    expires_at: datetime | None = None
    tags: set[str] = field(default_factory=set)

    def is_active(self, now: datetime) -> bool:
        return self.quantity > 0 and (self.expires_at is None or self.expires_at >= now)


@dataclass(slots=True)
class Request:
    request_id: str
    requester_id: str
    listing_type: ListingType
    quantity: int
    max_distance_km: int
    created_at: datetime
