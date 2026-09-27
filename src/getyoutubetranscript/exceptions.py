"""Exceptions raised by the GetYouTubeTranscript SDK."""

from __future__ import annotations

from typing import Any, Optional


class GetYouTubeTranscriptError(Exception):
    """Raised whenever the API returns a non-2xx status or ``{"success": false}``.

    The API always responds to errors with a JSON body shaped like
    ``{"success": false, "code": "...", "message": "..."}``. This exception
    parses that shape so callers can branch on ``code`` instead of guessing
    from an HTTP status or a generic exception message.

    Common codes: ``MISSING_API_KEY``, ``INVALID_API_KEY``, ``RATE_LIMITED``,
    ``PAYMENT_REQUIRED``, ``NOT_FOUND``. ``NETWORK_ERROR`` is used locally by
    this SDK (status_code 0) when the request never reached the server at all
    (DNS failure, timeout, connection refused, etc).

    Attributes:
        code: Machine-readable error code from the API's ``code`` field.
        message: Human-readable message from the API's ``message`` field.
        status_code: HTTP status code (400/401/402/404/429/503), or 0 if the
            request never reached the server.
        response_body: The full parsed JSON error body, if any, for callers
            that need fields beyond ``code``/``message`` (e.g. ``RATE_LIMITED``
            includes ``requestsThisMinute``; ``PAYMENT_REQUIRED`` includes
            ``creditsLeft`` and ``topupCreditsLeft``).
    """

    def __init__(
        self,
        code: str,
        message: str,
        status_code: int,
        *,
        response_body: Optional[dict[str, Any]] = None,
    ) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        self.response_body = response_body or {}
        super().__init__(f"[{code}] {message} (HTTP {status_code})")

    def __repr__(self) -> str:  # pragma: no cover - cosmetic
        return (
            f"GetYouTubeTranscriptError(code={self.code!r}, "
            f"message={self.message!r}, status_code={self.status_code!r})"
        )
