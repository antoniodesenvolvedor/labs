from flask_restplus import fields
from src.server.server import server



customer_product_rest_model = server.api.model(
    "customer_product",
    {
        "customer_email": fields.String(description="Email do cliente", required=True),
        "product_id": fields.String(description="ID do produto", required=True)
     }
)