from server.api import ticket_gateway
from server.model.ticket import Ticket


class TicketRobot:
    def __init__(self):
        pass

    def create_ticket(self, ticket: Ticket):
        ticket_gateway.create_ticket(ticket)
        import asyncio
        from datetime import datetime

        async def check_pending_tickets():
            while True:
                try:
                    # Get all pending tickets
                    tickets = await ticket_gateway.get_tickets()

                    # Process each pending ticket
                    for ticket in tickets:
                        print(f"[{datetime.now()}] Processing ticket: {ticket.id}")
                        # TODO: Add specific ticket handling logic here

                    # Wait 30 seconds
                    await asyncio.sleep(30)

                except Exception as e:
                    print(f"An error occurred while processing tickets: {str(e)}")
                    await asyncio.sleep(30)

        # Start the scheduled task
        asyncio.create_task(check_pending_tickets())