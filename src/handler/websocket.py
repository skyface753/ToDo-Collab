from fastapi import WebSocket


class active_connection:
    def __init__(self, websocket: WebSocket, user_id, collection_id):
        self.websocket = websocket
        self.user_id = user_id
        self.collection_id = collection_id


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[active_connection] = []

    async def connect(self, websocket: WebSocket, user_id, collection_id):
        await websocket.accept()
        self.active_connections.append(
            active_connection(websocket, user_id, collection_id))

    def disconnect(self, websocket: WebSocket):
        for connection in self.active_connections:
            if connection.websocket == websocket:
                self.active_connections.remove(connection)
                break

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, collection_id: str):
        for connection in self.active_connections:
            if connection.collection_id == collection_id:
                await connection.websocket.send_text(message)


manager = ConnectionManager()
