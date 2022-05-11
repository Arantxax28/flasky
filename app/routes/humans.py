from flask import Blueprint,jsonify, request, abort, make_response
from app.models.humans import Human
from app.models.cats import Cat
from app import db

humans_bp = Blueprint("humans_bp", __name__, url_prefix="/humans")

@humans_bp.route("", methods = ["POST"])
def create_human():
    request_body = request.get_json()
    new_human = Human(name=request_body["name"])
    db.session.add(new_human)
    db.session.commit()
    return{
        "msg": f"Successfully created {new_human.name}"
    }, 201

@humans_bp.route("", methods=["GET"])
def get_all_humans():
    humans = Human.query.all()

    response = []
    for human in humans:
        response.append({
            "name": human.name
        })
    return jsonify(response), 200

def validate_human(human_id):
    try:
        human_id = int(human_id)
    except:
        abort(make_response({"msg": f"invalid id{human_id}"}, 400))
    
    human = Human.query.get(human_id)
    if not human:
        abort(make_response({"msg":f"no human with id {human_id}"}, 404))
    return human
    
@humans_bp.route("/<human_id>/cats", methods=["POST"])
def create_cat(human_id):
    human = validate_human(human_id)
    request_body = request.get_json()

    new_cat = Cat(
        name = request_body["name"],
        color = request_body["color"],
        age = request_body["age"],
        human = human

    ) 

    db.session.add(new_cat)
    db.session.commit()
    return {
        "msg": f"new cat{new_cat.name} created for {human.name}"
    }, 201

@humans_bp.route("/<human_id>/cats", methods=["GET"])
def get_cats(human_id):
    human= validate_human(human_id)

    rsp = []
    for cat in human.cats:
        rsp.append({
            "id": cat.id,
            "name": cat.name,
            "color": cat.color,
            "age": cat.age
        })
    
    return jsonify(rsp), 200


