import json

from fastapi import FastAPI, WebSocket
from entities.bdd import SessionLocal, User, Game

app = FastAPI()
db = SessionLocal()


@app.websocket("/connection")
async def websocket_endpoint(websocket: WebSocket):
    game = None
    await websocket.accept()
    while True:
        client_data = await websocket.receive_text()
        print(client_data)
        client_data = client_data.replace("'", '"')
        print(client_data)
        client_data = json.loads(client_data)
        action = client_data["action"]
        username = client_data["username"]
        if action == "connection":
            user = User(username=username)
            db.add(user)
            db.commit()
            db.refresh(user)
            db.commit()
            games = db.query(Game).all()
            if games is not None:
                for game in games:
                    if len(game.users) <= 5:
                        game = game

                if game or game is None:
                    game = Game()
                    db.add(game)
                    db.commit()
                    db.refresh(game)

            else:
                game = Game()
                db.add(game)
                db.commit()
                db.refresh(game)

            game.users.append(user)
            db.commit()
            db.close()

