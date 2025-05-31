from server.service.ticket_service import TicketService

def main():
    try:
        service = TicketService()
        similar_tickets = service.find_similar_tickets()
        
        print("\n找到的相似工单:")
        for ticket in similar_tickets:
            print(f"\n工单ID: {ticket.ticket_id}")
            print(f"相似度: {ticket.similarity_score:.2f}")
            print(f"原因: {ticket.reason}")
    except Exception as e:
        print(f"运行出错: {e}")

if __name__ == "__main__":
    main() 