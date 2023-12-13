from fastapi import WebSocket

class aConnection:
    def __init__(self, websocket: WebSocket, user_id, team_id):
        self.websocket = websocket
        self.user_id = user_id
        self.team_id = team_id

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[aConnection] = []

    async def connect(self, websocket: WebSocket, user_id, team_id):
        await websocket.accept()
        self.active_connections.append(aConnection(websocket, user_id, team_id))

    def disconnect(self, websocket: WebSocket):
        for connection in self.active_connections:
            if connection.websocket == websocket:
                self.active_connections.remove(connection)
                break

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, team_id: str):
        for connection in self.active_connections:
            if connection.team_id == team_id:
                await connection.websocket.send_text(message)
                


manager = ConnectionManager()