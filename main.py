import src.controllers.favorite_product_list
import src.controllers.customer
from src.db_models.database import db_session
from src.server.server import server

app = server.app
api = server.api

server.run()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

