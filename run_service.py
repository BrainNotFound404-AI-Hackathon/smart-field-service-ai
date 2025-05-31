from server.service.ticket_service import TicketService

def main():
    try:
        service = TicketService()
        similar_tickets = service.find_similar_tickets()
        
        print("\nfind similar ticket:")
        for ticket in similar_tickets:
            print(f"\nticket ID: {ticket.ticket_id}")
            print(f"similarity: {ticket.similarity_score:.2f}")
            print(f"cause: {ticket.reason}")
    except Exception as e:
        print(f"run error: {e}")

if __name__ == "__main__":
    main() 