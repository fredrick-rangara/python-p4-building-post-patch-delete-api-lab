from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

# --- POST /baked_goods ---
@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    # Use request.form since the lab specifies "the request will send data in a form"
    new_item = BakedGood(
        name=request.form.get('name'),
        price=float(request.form.get('price')),
        bakery_id=int(request.form.get('bakery_id'))
    )
    db.session.add(new_item)
    db.session.commit()
    return make_response(jsonify(new_item.to_dict()), 201)

# --- PATCH /bakeries/<id> ---
@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.filter_by(id=id).first()
    if not bakery:
        return make_response(jsonify({"error": "Bakery not found"}), 404)
    
    # Update only the name if provided in the form
    new_name = request.form.get('name')
    if new_name:
        bakery.name = new_name
        db.session.commit()
    
    return make_response(jsonify(bakery.to_dict()), 200)

# --- DELETE /baked_goods/<id> ---
@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    item = BakedGood.query.filter_by(id=id).first()
    if not item:
        return make_response(jsonify({"error": "Baked good not found"}), 404)
    
    db.session.delete(item)
    db.session.commit()
    
    return make_response(jsonify({"message": "Record successfully deleted"}), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)