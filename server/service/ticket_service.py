import json
from typing import List
from datetime import datetime
from server.database.model import Ticket as SqlTicket
from server.model.ticket import SimilarTicket, Ticket, SimilarTicketsResponse
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from server.database.database import Database

class TicketService:
    """Ticket service class"""

    def __init__(self):
        """Initialize the ticket service"""
        load_dotenv()
        if "GOOGLE_API_KEY" not in os.environ:
            raise ValueError("GOOGLE_API_KEY environment variable is not set")

        # Initialize example data
        self.current = Ticket(
            id="N1",
            elevator_id="E100",
            location="Building 1 East",
            description="Door does not fully close on 2F",
            status="Pending",
            priority="High",
            create_time=datetime.now().isoformat(),
            ai_suggestion="Check door operator system, door lock, and door controller"
        )

        # Initialize AI model
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0,
            max_retries=2
        )
        self.structured_llm = self.llm.with_structured_output(SimilarTicketsResponse)

    def _format_ticket_info(self, ticket: Ticket) -> str:
        """Format ticket information into a string"""
        return f"""ID: {ticket.id}
        Elevator: {ticket.elevator_id}
        Location: {ticket.location}
        Description: {ticket.description}
        Status: {ticket.status}
        Priority: {ticket.priority}
        Create Time: {ticket.create_time}
        Solution: {ticket.solution if ticket.solution else 'N/A'}
        AI Suggestion: {ticket.ai_suggestion if ticket.ai_suggestion else 'N/A'}"""

    def get_all_tickets(self) -> List[Ticket]:
        db = Database()
        tickets = db.list_tickets()
        return tickets

    def get_pending_tickets(self) -> List[Ticket]:
        """
        Retrieve all pending tickets

        Returns:
            List[Ticket]: List of pending tickets
        """
        db = Database()
        tickets = db.list_tickets()
        return [t for t in tickets if t.status == "Pending"]

    def get_ticket_by_id(self, ticket_id: str) -> Ticket:
        """
        Retrieve ticket details by ID

        Args:
            ticket_id (str): Ticket ID

        Returns:
            Ticket: Ticket details
        """
        db = Database()
        ticket = db.get_ticket_by_id(ticket_id)
        return ticket

    def create_ticket(self, ticket: Ticket) -> Ticket:
        """
        Create a new ticket

        Args:
            ticket (Ticket): Ticket information

        Returns:
            Ticket: Created ticket
        """
        ticket_dict = ticket.dict()
        if ticket_dict.get("images"):
            ticket_dict["images"] = json.dumps(ticket_dict["images"])
        db_ticket = SqlTicket(**ticket_dict)

        db_ticket.create_time = datetime.now()
        db = Database()
        db.add_ticket(db_ticket)
        return ticket

    def update_ticket(self, ticket_id: str, ticket: Ticket) -> Ticket:
        """
        Update ticket information

        Args:
            ticket_id (str): Ticket ID
            ticket (Ticket): Updated ticket info

        Returns:
            Ticket: Updated ticket
        """
        db = Database()
        db.update_ticket(ticket_id, ticket.model_dump())
        return ticket


    def find_similar_tickets(self, current_ticket: Ticket = None, max_results: int = 2) -> List[SimilarTicket]:
        """
        Find historical tickets similar to the current ticket

        Args:
            current_ticket: Current ticket (uses self.current if None)
            max_results: Maximum number of similar tickets to return

        Returns:
            List[SimilarTicket]: List of similar tickets, sorted by similarity score (descending)
        """
        current_ticket = current_ticket or self.current

        historical_ticket = self.get_all_tickets()

        # 格式化工单信息
        current_ticket_info = self._format_ticket_info(current_ticket)
        historical_tickets_info = "\n".join([
            f"{self._format_ticket_info(t)}\n---"
            for t in historical_ticket
        ])

        # Construct prompt
        prompt = f"""You are an AI assistant specialized in identifying similar elevator maintenance tickets.
            Please analyze the current ticket and historical tickets below and find the most similar ones.
            Consider the following similarity factors:
            1. Same elevator or location
            2. Similar issue type
            3. Similar fault description
            4. Related past solutions
            5. Similar priority level
            6. Related AI suggestions

            Current ticket:
            {current_ticket_info}

            Historical tickets:
            {historical_tickets_info}

            Please return {max_results} most similar tickets, sorted in descending order of similarity.
            """

        try:
            # Get structured response
            response = self.structured_llm.invoke(prompt)
            return response.similar_tickets[:max_results]
        except Exception as e:
            print(f"Error getting model response: {e}")
            return []