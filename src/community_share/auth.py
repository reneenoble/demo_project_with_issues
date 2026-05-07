from __future__ import annotations

import hashlib
import hmac
import json
import re
from dataclasses import dataclass

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass(slots=True)
class SSOProfile:
    provider: str
    subject: str
    email: str


class SSOValidationError(ValueError):
    pass


class BasicSSOProvider:
    """Very small SSO token validator for demo purposes.

    The token format is: `<json payload>.<hex hmac>`
    """

    def __init__(self, secret: str) -> None:
        self._secret = secret.encode("utf-8")

    def validate_token(self, token: str) -> SSOProfile:
        try:
            payload_raw, signature = token.rsplit(".", 1)
        except ValueError as exc:
            raise SSOValidationError("Malformed token") from exc

        expected_signature = hmac.new(
            self._secret, payload_raw.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(signature, expected_signature):
            raise SSOValidationError("Invalid token signature")

        try:
            payload = json.loads(payload_raw)
        except json.JSONDecodeError as exc:
            raise SSOValidationError("Malformed token payload") from exc
        for key in ("provider", "subject", "email"):
            if key not in payload:
                raise SSOValidationError(f"Missing field: {key}")
        email = str(payload["email"]).strip().lower()
        if not _EMAIL_RE.match(email):
            raise SSOValidationError("Invalid email format")

        return SSOProfile(
            provider=payload["provider"],
            subject=payload["subject"],
            email=email,
        )
