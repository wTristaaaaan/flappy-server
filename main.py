import json

from fastapi import FastAPI, WebSocket
from entities.bdd import SessionLocal, User, Game

app = FastAPI()
db = SessionLocal()


@app.websocket("/connection")
async def websocket_endpoint(websocket: WebSocket):
    new_game = None
    await websocket.accept()
    while True:
        client_data = await websocket.receive_text()
        client_data = client_data.replace("'", '"')
        client_data = json.loads(client_data)
        action = client_data["action"]
        username = client_data["username"]
        if action == "connection":
            user = User(username=username)
            user = db.merge(user)
            db.add(user)
            db.commit()
            db.refresh(user)
            db.commit()
            games = db.query(Game).all()
            for game in games:
                print(f"{game.id} : {len(game.users)}")
                if len(game.users) < 5:
                    new_game = game

            if new_game is None:
                new_game = Game()
                db.add(new_game)
                db.commit()
                db.refresh(new_game)

            new_game.users.append(user)
            db.commit()
            await websocket.send_json({"id": user.id, "gameId": new_game.id})
