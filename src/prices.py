from flask import Flask
from flask import request

from src.db import create_lift_pass_db_connection
from src.delivery.api.get_lift_pass_cost_controller import GetLiftPassCostController

app = Flask("lift-pass-pricing")

connection_options = {
    "host": "mariadb",
    "user": "root",
    "database": "lift_pass",
    "password": "mysql",
}

connection = create_lift_pass_db_connection(connection_options)


@app.route("/prices", methods=["GET"])
def get_lift_pass_cost() -> dict[str, int]:
    get_lift_pass_controller = GetLiftPassCostController(connection)
    return get_lift_pass_controller()


@app.route("/prices", methods=["PUT"])
def add_lift_pass() -> dict:
    lift_pass_cost = request.args["cost"]
    lift_pass_type = request.args["type"]
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO `base_price` (type, cost) VALUES (?, ?) "
        + "ON DUPLICATE KEY UPDATE cost = ?",
        (lift_pass_type, lift_pass_cost, lift_pass_cost),
    )
    return {}


if __name__ == "__main__":
    app.run(port=3005)
