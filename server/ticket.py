"""ticket_model.py
---------------------------------------------------------------------
Ticket data model (English‑only) **plus** a handful of handy utility
methods that are commonly needed when working with such data types.

Highlights
~~~~~~~~~~
* Enum‑based `Status` & `Priority` for type‑safety.
* `Ticket` dataclass with:
  • `to_dict()` / `from_dict()`
  • `to_json()` / `from_json()`
  • `close()` helper to mark a ticket as closed.
  • `add_image()` to append an image URL.
  • Nice `__str__` representation for logging.
---------------------------------------------------------------------
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict, replace
from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional

__all__ = [
    "Status",
    "Priority",
    "Ticket",
]

# ---------------------------------------------------------------------
# Enum definitions
# ---------------------------------------------------------------------


class Status(str, Enum):
    PENDING = "Pending"
    CLOSED = "Closed"
    # Extend with additional states as needed


class Priority(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


# ---------------------------------------------------------------------
# Helper for mutable default field
# ---------------------------------------------------------------------

def _default_list() -> List[str]:
    """Return a new empty list. Helps `dataclasses` avoid mutable defaults."""
    return []


# ---------------------------------------------------------------------
# Ticket dataclass + utilities
# ---------------------------------------------------------------------


@dataclass(slots=True)
class Ticket:
    """Data model representing a maintenance ticket."""

    # Core identifiers
    id: str                          # Ticket ID
    elevator_id: str                 # Elevator ID

    # Location & description
    location: str                    # Elevator location (e.g. "Building 1 East")
    description: str                 # Fault description

    # Status & priority
    status: Status = Status.PENDING
    priority: Priority = Priority.MEDIUM

    # Timeline
    create_time: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds"))
    close_time: Optional[str] = None  # ISO‑8601 closing timestamp

    # Resolution details (optional for pending tickets)
    solution: Optional[str] = None    # Repair solution or suggestion
    result: Optional[str] = None      # Repair outcome/verification

    # Additional information
    images: List[str] = field(default_factory=_default_list)  # Related image URLs
    ai_suggestion: Optional[str] = None  # AI‑generated troubleshooting advice

    # --------------------------------------------------
    # Convenience methods
    # --------------------------------------------------

    def to_dict(self) -> dict:
        """Return a plain dict suitable for JSON serialisation or DB storage."""
        data = asdict(self)
        # Convert Enum members to their value strings
        data["status"] = self.status.value
        data["priority"] = self.priority.value
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Ticket":
        """Create a :class:`Ticket` from a dict (reverse of :py:meth:`to_dict`)."""
        return cls(
            id=data["id"],
            elevator_id=data["elevator_id"],
            location=data["location"],
            description=data["description"],
            status=Status(data.get("status", Status.PENDING)),
            priority=Priority(data.get("priority", Priority.MEDIUM)),
            create_time=data.get("create_time", datetime.now(timezone.utc).isoformat(timespec="seconds")),
            close_time=data.get("close_time"),
            solution=data.get("solution"),
            result=data.get("result"),
            images=list(data.get("images", [])),
            ai_suggestion=data.get("ai_suggestion"),
        )

    # JSON helpers ---------------------------------------------------
    def to_json(self, **json_kwargs) -> str:
        """Return a JSON string of the ticket. Accepts normal `json.dumps` kwargs."""
        return json.dumps(self.to_dict(), ensure_ascii=False, **json_kwargs)

    @classmethod
    def from_json(cls, json_str: str) -> "Ticket":
        """Create a :class:`Ticket` from its JSON representation."""
        return cls.from_dict(json.loads(json_str))

    # Domain‑specific helpers ---------------------------------------
    def close(self, solution: str, result: str) -> None:
        """Mark the ticket as *Closed* and set resolution details/time."""
        self.status = Status.CLOSED
        self.solution = solution
        self.result = result
        self.close_time = datetime.now(timezone.utc).isoformat(timespec="seconds")

    def add_image(self, url: str) -> None:
        """Attach an image URL to the ticket (duplicates are ignored)."""
        if url not in self.images:
            self.images.append(url)

    # Dataclass override --------------------------------------------
    def __str__(self) -> str:  # pragma: no cover
        return (
            f"<Ticket #{self.id} | {self.status.value} | {self.priority.value} | "
            f"Elevator {self.elevator_id}>"
        )

    # Transformational helper (immutable style) ---------------------
    def copy_with(self, **changes) -> "Ticket":
        """Return a *new* Ticket with selected attributes replaced."""
        return replace(self, **changes)


# ---------------------------------------------------------------------
# Quick demo (disabled by default)
# ---------------------------------------------------------------------
if __name__ == "__main__":
    t = Ticket(
        id="T-100",
        elevator_id="E-1",
        location="Building 1 East",
        description="Unusual noise during ascent",
        priority=Priority.HIGH,
    )

    t.add_image("https://example.com/img1.jpg")
    print("Created:", t)

    t.close("Replaced traction wire rope", "Normal operation restored")
    print("Closed :", t)

    json_blob = t.to_json(indent=2)
    print("JSON   :", json_blob)

    restored = Ticket.from_json(json_blob)
    print("Restored:", restored, "\nEqual?", restored == t)
