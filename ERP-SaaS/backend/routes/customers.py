
from flask import Blueprint, jsonify, request
from uuid import uuid4
from datetime import datetime, timezone

from backend.services.json_storage import read_data, write_data

customers_bp = Blueprint("customers", __name__)

FILE_NAME = "customers.json"


def get_customers():
    return read_data(FILE_NAME)


def validate_customer(data):
    if not isinstance(data, dict):
        return "Los datos enviados deben ser un objeto."

    name = data.get("name")

    if not isinstance(name, str) or not name.strip():
        return "El nombre del cliente es obligatorio."

    email = data.get("email", "")

    if not isinstance(email, str):
        return "El correo electrónico no es válido."

    phone = data.get("phone", "")

    if not isinstance(phone, str):
        return "El teléfono no es válido."

    return None


@customers_bp.route("/api/customers", methods=["GET"])
def list_customers():
    try:
        customers = get_customers()
        return jsonify({
            "success": True,
            "total": len(customers),
            "data": customers
        }), 200
    except ValueError as error:
        return jsonify({"success": False, "message": str(error)}), 500


@customers_bp.route("/api/customers/<customer_id>", methods=["GET"])
def get_customer(customer_id):
    customers = get_customers()

    customer = next(
        (item for item in customers if item["id"] == customer_id),
        None
    )

    if customer is None:
        return jsonify({
            "success": False,
            "message": "Cliente no encontrado."
        }), 404

    return jsonify({"success": True, "data": customer}), 200


@customers_bp.route("/api/customers", methods=["POST"])
def create_customer():
    data = request.get_json(silent=True)
    error = validate_customer(data)

    if error:
        return jsonify({"success": False, "message": error}), 400

    customers = get_customers()

    customer = {
        "id": str(uuid4()),
        "name": data["name"].strip(),
        "document": str(data.get("document", "")).strip(),
        "email": data.get("email", "").strip(),
        "phone": data.get("phone", "").strip(),
        "address": str(data.get("address", "")).strip(),
        "status": "active",
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    customers.append(customer)
    write_data(FILE_NAME, customers)

    return jsonify({
        "success": True,
        "message": "Cliente registrado correctamente.",
        "data": customer
    }), 201


@customers_bp.route("/api/customers/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    data = request.get_json(silent=True)
    error = validate_customer(data)

    if error:
        return jsonify({"success": False, "message": error}), 400

    customers = get_customers()

    for index, customer in enumerate(customers):
        if customer["id"] == customer_id:
            updated_customer = {
                **customer,
                "name": data["name"].strip(),
                "document": str(data.get("document", customer.get("document", ""))).strip(),
                "email": data.get("email", "").strip(),
                "phone": data.get("phone", "").strip(),
                "address": str(data.get("address", "")).strip()
            }

            customers[index] = updated_customer
            write_data(FILE_NAME, customers)

            return jsonify({
                "success": True,
                "message": "Cliente actualizado correctamente.",
                "data": updated_customer
            }), 200

    return jsonify({
        "success": False,
        "message": "Cliente no encontrado."
    }), 404


@customers_bp.route("/api/customers/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customers = get_customers()

    updated_customers = [
        customer for customer in customers
        if customer["id"] != customer_id
    ]

    if len(updated_customers) == len(customers):
        return jsonify({
            "success": False,
            "message": "Cliente no encontrado."
        }), 404

    write_data(FILE_NAME, updated_customers)

    return jsonify({
        "success": True,
        "message": "Cliente eliminado correctamente."
    }), 200
