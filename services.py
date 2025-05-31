from typing import List
from server.model.ticket import Ticket

class TicketService:
    """ticket service class"""
    
    def __init__(self):
        # here can init data library connect etc.
        pass
    
    def get_pending_tickets(self) -> List[Ticket]:
        """
        derive all un-solved ticket
        
        Returns:
            List[Ticket]: unsolved ticket list
        """
        # TODO: realize data library search logic
        # return example data
        return [
            Ticket(
                id="T001",
                elevator_id="E001",
                location="1 building 1 unit",
                description="elevator door can not close as usual",
                status="Pending",
                priority="High",
                create_time="2024-03-20 10:30:00",
                ai_suggestion="Recommend to check door and electronic system、door lock devices and door controller"
            ),
            Ticket(
                id="T002",
                elevator_id="E002",
                location="2 building 2 unit",
                description="abnormal sound when elevator is running",
                status="Pending",
                priority="Medium",
                create_time="2024-03-20 11:15:00",
                ai_suggestion="It is recommended to inspect the traction machine, guide rails, and guide shoes"
            )
        ]
    
    def get_ticket_by_id(self, ticket_id: str) -> Ticket:
        """
        require ticket detail according to ID
        
        Args:
            ticket_id (str): ticket ID
            
        Returns:
            Ticket: ticket detail
        """
        # TODO: realize data library search logic
        pass
    
    def create_ticket(self, ticket: Ticket) -> Ticket:
        """
        create new ticket
        
        Args:
            ticket (Ticket): ticket information
            
        Returns:
            Ticket: created ticket
        """
        # TODO: realize data library insert logic
        pass
    
    def update_ticket(self, ticket_id: str, ticket: Ticket) -> Ticket:
        """
        update ticket information
        
        Args:
            ticket_id (str): ticket ID
            ticket (Ticket): information of updated ticket
            
        Returns:
            Ticket: ticket after updating
        """
        # TODO: realize data library update logic
        pass 