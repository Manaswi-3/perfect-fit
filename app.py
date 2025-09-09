from flask import Flask, render_template, session, redirect, url_for, request, jsonify
from db import init_app, mongo
from auth import auth_bp
from datetime import datetime
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "replace_with_random_string"

app.config["MONGO_URI"] = "mongodb+srv://manu-333:Sailaja123@cluster.qp4yxz5.mongodb.net/perfectfit"

init_app(app)

app.register_blueprint(auth_bp)

# ---------------- ROUTES ----------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/guide")
def guide():
    if "username" in session:
        return render_template("guide.html", username=session["username"])
    return redirect(url_for("auth.login"))

@app.route("/sizeinfo")
def sizeinfo():
    if "username" in session:
        return render_template("sizeinfo.html", username=session["username"])
    return redirect(url_for("auth.login"))

@app.route("/feedback", methods=["POST"])
def feedback():
    quires = mongo.db.quires

    name = request.form.get("name")
    email = request.form.get("email")
    subject = request.form.get("subject")
    message = request.form.get("message")

    quires.insert_one({
        "name": name,
        "email": email,
        "subject": subject,
        "message": message,
        "created_at": datetime.utcnow()
    })

    return render_template("thankyou.html", name=name)

@app.route("/save_sizeinfo", methods=["POST"])
def save_sizeinfo():
    if "username" not in session:
        return jsonify({"success": False, "msg": "Not logged in"})
    
    data = request.get_json()

    user_data = {
        "username": session["username"],
        "waist": data.get("waist"),
        "inseam": data.get("inseam"),
        "hip": data.get("hip"),
        "thigh": data.get("thigh"),
        "pantLength": data.get("pantLength"),
        "style": data.get("style"),
        "color": data.get("color"),
        "street": data.get("street"),
        "city": data.get("city"),
        "state": data.get("state"),
        "zip": data.get("zip"),
        "phone": data.get("phone"),
        "status": "Order Received",   
        "created_at": datetime.utcnow()
    }

    mongo.db.data.insert_one(user_data)

    return jsonify({"success": True})

@app.route("/admin")
def admin_dashboard():
    if "role" not in session or session["role"] != "admin":
        return redirect("/")  # deny access
    return render_template("admin.html", username=session.get("username"))

@app.route("/admin/orders")
def admin_orders():
    if "role" not in session or session["role"] != "admin":
        return jsonify({"success": False, "msg": "Unauthorized"}), 403

    orders = list(mongo.db.data.find())
    for order in orders:
        order["_id"] = str(order["_id"])
    return jsonify({"orders": orders})

@app.route("/admin/update_status/<order_id>", methods=["POST"])
def update_status(order_id):
    if "role" not in session or session["role"] != "admin":
        return jsonify({"success": False, "msg": "Unauthorized"}), 403

    new_status = request.json.get("status")
    if new_status not in ["Order Received", "In Production", "Ready to Delivery"]:
        return jsonify({"success": False, "msg": "Invalid status"}), 400

    mongo.db.data.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": {"status": new_status}}
    )

    return jsonify({"success": True, "new_status": new_status})


@app.route("/my_status")
def my_status():
    if "username" not in session:
        return jsonify({"success": False, "msg": "Not logged in"}), 403

    orders = list(mongo.db.data.find({"username": session["username"]}).sort("created_at", -1))

    for order in orders:
        order["_id"] = str(order["_id"])
        order["created_at"] = order["created_at"].strftime("%Y-%m-%d %H:%M")

    return jsonify({"success": True, "orders": orders})

@app.route("/status")
def status_page():
    if "username" not in session:
        return redirect(url_for("auth.login"))
    return render_template("status.html", username=session["username"])  # ✅ Fixed


if __name__ == "__main__":
    app.run(debug=True)
