from flask_restplus import fields
from src.server.server import server





customer_rest_model = server.api.model(
    "Customer",
    {
        "customer_email": fields.String(description="Email do cliente", required=True),
        "customer_name": fields.String(description="Nome do cliente", required=True)
     }
)

customer_email_rest_model = server.api.model(
    "Customer_email",
    {
        "customer_email": fields.String(description="Email do cliente", required=True)
     }
)

customer_response_rest_model = server.api.model(
    "Customer_response",
    {
        "customer_id": fields.Integer(description="ID do cliente"),
        "customer_email": fields.String(description="Email do cliente"),
        "customer_name": fields.String(description="Nome do cliente")
     }
)