from server.database.database import Database

if __name__ == "__main__":
    db = Database()
    db.init_data()
    print([t.dict() for t in db.list_tickets()])