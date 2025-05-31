from datetime import datetime
from server.model.ticket import Ticket


mock_tickets = [
                Ticket(
                    id="T001",
                    elevator_id="E001",
                    location="Building 1 Unit 1",
                    description="Elevator door cannot close properly",
                    status="Pending",
                    priority="High",
                    create_time=datetime.now()
                ),
                Ticket(
                    id="T002",
                    elevator_id="E002",
                    location="Building 2 Unit 2",
                    description="Abnormal noise during elevator operation",
                    status="Pending",
                    priority="Medium",
                    create_time=datetime.now()
                ),
                Ticket(
                    id="T003",
                    elevator_id="E003",
                    location="Building 3 Unit 1",
                    description="Elevator display screen not working",
                    status="Pending",
                    priority="Low",
                    create_time=datetime.now()
                )
            ]