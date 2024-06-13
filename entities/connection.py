from fastapi import WebSocket
import pprint


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.games = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    @staticmethod
    async def send_personal_message(message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def users_joined(self, message: str, game_id: int):
        for lobbies in self.games:
            if lobbies[0]["game"] == game_id:
                for user in lobbies:
                    await user["ws"].send_text(message)

    async def join_game(self, game_id, user_id, ws):
        if len(self.games) == 0:
            self.games.append([{
                "game": game_id,
                "user_id": user_id,
                "ws": ws
            }])
        else:
            for lobbies in self.games:
                if len(lobbies) == 5:
                    self.games.append([{
                        "game": game_id,
                        "user_id": user_id,
                        "ws": ws
                    }])
                    break
                else:
                    if lobbies[0]["game"] == game_id:
                        lobbies.append({
                            "game": game_id,
                            "user_id": user_id,
                            "ws": ws
                        })
        await self.users_joined(f"New player joined the game {game_id}", game_id)

