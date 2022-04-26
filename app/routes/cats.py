from flask import Blueprint,jsonify

class Cat:
    def __init__(self, id, name, age, color):
        self.id = id
        self.name = name
        self.age = age
        self.color = color

cats = [
    Cat(1, "Chidi", 0.5, "grey"),
    Cat(2, "Siba", 3, "orange"),
    Cat(3, "Tucker", 5, "black")
]

cats_bp = Blueprint('cats_bp', __name__, url_prefix = '/cats')

@cats_bp.route("", methods = ["GET"])
def get_all_cats():
    cat_response = []
    for cat in cats:
        cat_response.append({
            "id": cat.id,
            "name": cat.name,
            "age": cat.age,
            "color": cat.color
        })
    return jsonify(cat_response), 300

@cats_bp.route("/<cat_id>", methods = ["GET"])
def get_one_cat(cat_id):
    try:
        cat_id = int(cat_id)
    except ValueError:
        response = {"msg": f"Invalid id: {cat_id}"}
        return jsonify(response), 400
    chosen_cat = None
    for cat in cats:
        if cat.id == cat_id:
            chosen_cat = cat
            break
    if chosen_cat is None:
        response = {"msg": f"Could not find cat with id {cat_id}"}
        return jsonify(response), 404
    response = {
        "id": chosen_cat.id,
        "name": chosen_cat.name,
        "age": chosen_cat.age,
        "color": chosen_cat.color
    }
    return jsonify(response), 200


