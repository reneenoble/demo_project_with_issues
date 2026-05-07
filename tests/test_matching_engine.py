from datetime import UTC, datetime, timedelta
import hashlib
import hmac
import unittest

from community_share.auth import BasicSSOProvider, SSOValidationError
from community_share.models import Listing, ListingType, Request, User
from community_share.services import MatchingEngine


class MatchingEngineTests(unittest.TestCase):
    def test_matches_respect_distance_and_quantity(self) -> None:
        now = datetime.now(UTC)
        users = {
            "u1": User("u1", "Alice", "AA11"),
            "u2": User("u2", "Bob", "AA12"),
            "u3": User("u3", "Cara", "ZZ99"),
        }
        listings = [
            Listing("l1", "u1", "Garden shovel", ListingType.EQUIPMENT, 2, now),
            Listing("l2", "u3", "Far away shovel", ListingType.EQUIPMENT, 3, now),
        ]
        requests = [
            Request("r1", "u2", ListingType.EQUIPMENT, 2, max_distance_km=20, created_at=now),
        ]

        matches = MatchingEngine().match_requests(users, listings, requests, now)

        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].listing_id, "l1")
        self.assertEqual(matches[0].allocated_quantity, 2)

    def test_expired_listings_are_ignored(self) -> None:
        now = datetime.now(UTC)
        users = {
            "u1": User("u1", "Alice", "AA11"),
            "u2": User("u2", "Bob", "AA12"),
        }
        listings = [
            Listing(
                "l1",
                "u1",
                "Tomatoes",
                ListingType.VEGETABLE,
                5,
                now,
                expires_at=now - timedelta(minutes=1),
            )
        ]
        requests = [
            Request("r1", "u2", ListingType.VEGETABLE, 1, max_distance_km=20, created_at=now),
        ]

        matches = MatchingEngine().match_requests(users, listings, requests, now)
        self.assertEqual(matches, [])


class SSOProviderTests(unittest.TestCase):
    def test_malformed_payload_raises_validation_error(self) -> None:
        provider = BasicSSOProvider("secret")
        payload = "{invalid-json"
        signature = hmac.new(
            b"secret",
            payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        with self.assertRaises(SSOValidationError):
            provider.validate_token(f"{payload}.{signature}")


if __name__ == "__main__":
    unittest.main()
