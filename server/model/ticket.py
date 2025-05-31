from datetime import datetime
from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class Ticket(BaseModel):
    """Ticket data model"""
    id: str = Field(description="Ticket ID")
    elevator_id: str = Field(description="Elevator ID")
    location: str = Field(description="Elevator location")
    description: str = Field(description="Fault description")
    status: Literal["Pending", "Closed"] | str = Field(description="Ticket status")
    priority: Literal["High", "Medium", "Low"] | str = Field(description="Priority level")
    create_time: datetime = Field(default=datetime.now(), description="Creation time")
    close_time: Optional[str] = Field(default=None, description="Closure time (for closed tickets)")
    solution: Optional[str] = Field(default=None, description="Solution (maintenance operations entered/AI suggestions/manual input)")
    result: Optional[str] = Field(default=None, description="Repair result (manually entered)")
    images: Optional[List[str]] = Field(default=None, description="Array of related image URLs")
    ai_suggestion: Optional[str] = Field(default=None, description="AI-generated key troubleshooting suggestions")

class SimilarTicket(BaseModel):
    """Structure for similar ticket response."""
    ticket_id: str = Field(..., description="The ID of the similar ticket")
    similarity_score: float = Field(..., description="Similarity score between 0 and 1")
    reason: str = Field(..., description="Brief explanation of why this ticket is similar")

class SimilarTicketsResponse(BaseModel):
    """Response containing a list of similar tickets."""
    similar_tickets: List[SimilarTicket] = Field(..., description="List of similar tickets")
