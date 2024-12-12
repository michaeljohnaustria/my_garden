import re
from datetime import datetime
from flask import Flask, jsonify, request
from http import HTTPStatus
import mysql.connector
from myDB import Config 
import jwt
import datetime
import json
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps 

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(**Config)

def is_valid_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False
    

# my facts

@app.route("/api/facts", methods=["GET"])
@token_required
def get_facts():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM facts")
        facts = cursor.fetchall()
        return jsonify({"success": True, "data": facts, "total": len(facts)}), HTTPStatus.OK
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        if 'cursor' in locals():  
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route("/api/facts/<int:fact_id>", methods=["GET"])
def get_fact(fact_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM facts WHERE fact_ID = %s", (fact_id,))
        fact = cursor.fetchone()
        if not fact:
            return jsonify({"success": False, "error": "Fact not found"}), HTTPStatus.NOT_FOUND
        return jsonify({"success": True, "data": fact}), HTTPStatus.OK
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        if 'cursor' in locals(): 
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route("/api/facts", methods=["POST"])
@token_required
def create_fact():
    data = request.get_json()
    if not data or not data.get("vegetable_ID") or not data.get("soil_type_ID") or not data.get("best_time_to_sow") or not data.get("best_time_to_harvest"):
        return jsonify({"success": False, "error": "vegetable_ID, soil_type_ID, best_time_to_sow, and best_time_to_harvest are required"}), HTTPStatus.BAD_REQUEST
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO facts (vegetable_ID, soil_type_ID, best_time_to_sow, best_time_to_harvest) VALUES (%s, %s, %s, %s)",
            (data["vegetable_ID"], data["soil_type_ID"], data["best_time_to_sow"], data["best_time_to_harvest"])
        )
        conn.commit()
        new_fact_id = cursor.lastrowid
        return jsonify({"success": True, "data": {"fact_ID": new_fact_id, **data}}), HTTPStatus.CREATED
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route("/api/facts/<int:fact_id>", methods=["PUT"])
@token_required
def update_fact(fact_id):
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "error": "No data provided"}), HTTPStatus.BAD_REQUEST

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE facts SET vegetable_ID = %s, soil_type_ID = %s, best_time_to_sow = %s, best_time_to_harvest = %s WHERE fact_ID = %s",
            (data["vegetable_ID"], data["soil_type_ID"], data["best_time_to_sow"], data["best_time_to_harvest"], fact_id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"success": False, "error": "Fact not found"}), HTTPStatus.NOT_FOUND
        return jsonify({"success": True, "message": "Fact updated successfully"}), HTTPStatus.OK
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route("/api/facts/<int:fact_id>", methods=["DELETE"])
@token_required
def delete_fact(fact_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM facts WHERE fact_ID = %s", (fact_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"success": False, "error": "Fact not found"}), HTTPStatus.NOT_FOUND
        return jsonify({"success": True, "message": f"Fact with ID {fact_id} has been deleted"}), HTTPStatus.OK
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        if 'cursor' in locals(): 
            cursor.close()
        if 'conn' in locals():
            conn.close()
# pests

@app.route("/api/pests", methods=["GET"])
@token_required
def get_pests():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pests")
        pests = cursor.fetchall()
        return jsonify({"success": True, "data": pests, "total": len(pests)}), HTTPStatus.OK
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        if 'cursor' in locals(): 
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route("/api/pests/<int:pest_id>", methods=["GET"])
def get_pest(pest_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pests WHERE pest_ID = %s", (pest_id,))
        pest = cursor.fetchone()
        if not pest:
            return jsonify({"success": False, "error": "Pest not found"}), HTTPStatus.NOT_FOUND
        return jsonify({"success": True, "data": pest}), HTTPStatus.OK
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        if 'cursor' in locals(): 
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route("/api/pests", methods=["POST"])
@token_required
def create_pest():
    data = request.get_json()
    if not data or not data.get("pest_Description") or not data.get("remedy_Description"):
        return jsonify({"success": False, "error": "pest_Description and remedy_Description are required"}), HTTPStatus.BAD_REQUEST
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO pests (pest_Description, remedy_Description) VALUES (%s, %s)",
            (data["pest_Description"], data["remedy_Description"])
        )
        conn.commit()
        new_pest_id = cursor.lastrowid
        return jsonify({"success": True, "data": {"pest_ID": new_pest_id, **data}}), HTTPStatus.CREATED
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route("/api/pests/<int:pest_id>", methods=["PUT"])
@token_required
def update_pest(pest_id):
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "error": "No data provided"}), HTTPStatus.BAD_REQUEST

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE pests SET pest_Description = %s, remedy_Description = %s WHERE pest_ID = %s",
            (data["pest_Description"], data["remedy_Description"], pest_id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"success": False, "error": "Pest not found"}), HTTPStatus.NOT_FOUND
        return jsonify({"success": True, "message": "Pest updated successfully"}), HTTPStatus.OK
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route("/api/pests/<int:pest_id>", methods=["DELETE"])
@token_required
def delete_pest(pest_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pests WHERE pest_ID = %s", (pest_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"success": False, "error": "Pest not found"}), HTTPStatus.NOT_FOUND
        return jsonify({"success": True, "message": f"Pest with ID {pest_id} has been deleted"}), HTTPStatus.OK
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# soil_types

@app.route("/api/soil_types", methods=["GET"])
@token_required
def get_soil_types():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM soil_types")
        soil_types = cursor.fetchall()
        return jsonify({"success": True, "data": soil_types, "total": len(soil_types)}), HTTPStatus.OK
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route("/api/soil_types/<int:soil_type_id>", methods=["GET"])
def get_soil_type(soil_type_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM soil_types WHERE soil_type_ID = %s", (soil_type_id,))
        soil_type = cursor.fetchone()
        if not soil_type:
            return jsonify({"success": False, "error": "Soil type not found"}), HTTPStatus.NOT_FOUND
        return jsonify({"success": True, "data": soil_type}), HTTPStatus.OK
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route("/api/soil_types", methods=["POST"])
@token_required
def create_soil_type():
    data = request.get_json()
    if not data or not data.get("soil_type_Description"):
        return jsonify({"success": False, "error": "soil_type_Description is required"}), HTTPStatus.BAD_REQUEST
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO soil_types (soil_type_Description) VALUES (%s)",
            (data["soil_type_Description"],)
        )
        conn.commit()
        new_soil_type_id = cursor.lastrowid
        return jsonify({"success": True, "data": {"soil_type_ID": new_soil_type_id, **data}}), HTTPStatus.CREATED
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route("/api/soil_types/<int:soil_type_id>", methods=["PUT"])
@token_required
def update_soil_type(soil_type_id):
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "error": "No data provided"}), HTTPStatus.BAD_REQUEST

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE soil_types SET soil_type_Description = %s WHERE soil_type_ID = %s",
            (data["soil_type_Description"], soil_type_id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"success": False, "error": "Soil type not found"}), HTTPStatus.NOT_FOUND
        return jsonify({"success": True, "message": "Soil type updated successfully"}), HTTPStatus.OK
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route("/api/soil_types/<int:soil_type_id>", methods=["DELETE"])
@token_required
def delete_soil_type(soil_type_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM soil_types WHERE soil_type_ID = %s", (soil_type_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"success": False, "error": "Soil type not found"}), HTTPStatus.NOT_FOUND
        return jsonify({"success": True, "message": f"Soil type with ID {soil_type_id} has been deleted"}), HTTPStatus.OK
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


# my vegetables

@app.route("/api/vegetables", methods=["GET"])
@token_required
def get_vegetables():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vegetables")
        vegetables = cursor.fetchall()
        return jsonify({"success": True, "data": vegetables, "total": len(vegetables)}), HTTPStatus.OK
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route("/api/vegetables/<int:vegetable_id>", methods=["GET"])
def get_vegetable(vegetable_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vegetables WHERE vegetable_ID = %s", (vegetable_id,))
        vegetable = cursor.fetchone()
        if not vegetable:
            return jsonify({"success": False, "error": "Vegetable not found"}), HTTPStatus.NOT_FOUND
        return jsonify({"success": True, "data": vegetable}), HTTPStatus.OK
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route("/api/vegetables", methods=["POST"])
@token_required
def create_vegetable():
    data = request.get_json()
    if not data or not data.get("vegetable_Name") or not data.get("recommended_soil_type"):
        return jsonify({"success": False, "error": "vegetable_Name and recommended_soil_type are required"}), HTTPStatus.BAD_REQUEST
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO vegetables (vegetable_Name, recommended_soil_type) VALUES (%s, %s)",
            (data["vegetable_Name"], data["recommended_soil_type"])
        )
        conn.commit()
        new_vegetable_id = cursor.lastrowid
        return jsonify({"success": True, "data": {"vegetable_ID": new_vegetable_id, **data}}), HTTPStatus.CREATED
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route("/api/vegetables/<int:vegetable_id>", methods=["PUT"])
@token_required
def update_vegetable(vegetable_id):
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "No data provided"}), HTTPStatus.BAD_REQUEST

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE vegetables SET vegetable_Name = %s, recommended_soil_type = %s WHERE vegetable_ID = %s",
            (data.get("vegetable_Name"), data.get("recommended_soil_type"), vegetable_id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"success": False, "error": "Vegetable not found"}), HTTPStatus.NOT_FOUND
        return jsonify({"success": True, "message": "Vegetable updated successfully"}), HTTPStatus.OK
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route("/api/vegetables/<int:vegetable_id>", methods=["DELETE"])
@token_required
def delete_vegetable(vegetable_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM vegetables WHERE vegetable_ID = %s", (vegetable_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"success": False, "error": "Vegetable not found"}), HTTPStatus.NOT_FOUND
        return jsonify({"success": True, "message": f"Vegetable with ID {vegetable_id} has been deleted"}), HTTPStatus.OK
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


if __name__ == "__main__":
    app.run(debug=True)
