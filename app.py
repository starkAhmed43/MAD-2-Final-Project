from flask import Flask,render_template, url_for, jsonify, request, redirect, send_file, flash
from flask_security import Security, SQLAlchemyUserDatastore,login_required
from flask_login import current_user
from flask_security.utils import hash_password
from os import path
from db import db, User, Role, Deck, Card
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "H9E2HP0284UMCRYH45N3IURDEMFP9U5P"
app.config["SECURITY_PASSWORD_SALT"] = "IVB3RIUHFP4XM3P9XHFHRE"


db.init_app(app)


if not path.exists("/db.sqlite3"):
	db.create_all(app=app)

user_datastore = SQLAlchemyUserDatastore(db,User,Role)
security = Security(app,user_datastore)

@app.route("/")
def index():
	return redirect(url_for("dashboard"))


@app.route("/register", methods=["GET","POST"])
def register():
	if request.method == "POST":
		user_datastore.create_user(email = request.form.get("email"),password = hash_password(request.form.get("password")))
		db.session.commit()
		return redirect("/login")
	return render_template("register.html")

@app.route("/profile")
@login_required
def profile():
	return render_template("profile.html")


@app.route("/dashboard")
@login_required
def dashboard():
	decks = Deck.query.filter_by(user_id=current_user.id).all()
	if request.headers.get("X-Requested-With") == "XMLHttpRequest":
		return jsonify(decks)

	return render_template("dashboard.html")

@app.route("/exportCSV")
@login_required
def download():
	decks = Deck.query.filter_by(user_id=current_user.id).all()
	export_file = open(str(current_user.email)+"-export.csv","w")
	for deck in decks:
		export_file.write("Deck\n")
		export_file.write(str(deck.name)+","+str(deck.last_reviewed)+","+str(deck.total_score)+"\n")
		deck_cards =  Card.query.filter_by(deck_id=deck.id).all()
		export_file.write("Card\n")
		for card in deck_cards:
			export_file.write(str(card.question)+","+str(card.answer)+","+str(card.difficulty)+","+str(card.last_reviewed)+","+str(card.last_score)+"\n")
		
		export_file.write("\n")
	export_file.close()
	return send_file("./"+str(current_user.email)+"-export.csv", as_attachment=True)


@app.route("/deck/create", methods=["POST"])
@login_required
def create_deck():
	name=request.get_json().get("name")
	print(name)
	print(current_user.id)
	deck = Deck.query.filter_by(name=name, user_id=current_user.id).first()
	if not deck:
		new_deck = Deck(name=name,user_id=current_user.id,last_reviewed=datetime.now())
		db.session.add(new_deck)
		db.session.commit()
		return jsonify(new_deck)
	else:
		return jsonify("None")

@app.route("/deck/delete", methods=["POST"])
@login_required
def delete_deck():
	deck_id = request.get_json().get("id")
	deck=Deck.query.filter_by(id=deck_id).first()
	cards=Card.query.filter_by(deck_id=deck_id).all()

	for card in cards:
		db.session.delete(card)
	db.session.delete(deck)
	db.session.commit()

	return jsonify({"result":"OK"},200)

@app.route("/deck/<int:deck_id>", methods=["GET","POST"])
@login_required
def view_deck(deck_id):
	deck = Deck.query.filter_by(id=deck_id).first()
	cards = Card.query.filter_by(deck_id=deck_id).all()
	if request.headers.get("X-Requested-With") == "XMLHttpRequest":
		if request.headers.get("TYPE") == "Card":
			return jsonify(cards)
		if request.headers.get("TYPE") == "Deck":
			return jsonify(deck)
	return render_template("view_deck.html")

@app.route("/deck<int:deck_id>/review", methods=["GET","POST"])
@login_required
def review_deck(deck_id):
	deck = Deck.query.filter_by(id=deck_id).first()
	cards = Card.query.filter_by(deck_id=deck_id).all()
	if request.headers.get("X-Requested-With") == "XMLHttpRequest":
		if request.headers.get("TYPE") == "Card":
			return jsonify(cards)
		if request.headers.get("TYPE") == "Deck":
			return jsonify(deck)

		if request.headers.get("Content-Type") == "application/json":
			score_key = {"easy":3,"medium":2,"difficult":1}
			review_submission = request.get_json()
			deck.last_reviewed = datetime.now()
			deck.total_score = 0
			for elem in review_submission:
				card = Card.query.filter_by(id=elem.get("id")).first()
				card.difficulty = elem.get("difficulty")
				card.last_reviewed = datetime.now()
				card.last_score = score_key[card.difficulty]
				deck.total_score += card.last_score

			db.session.commit()
			return jsonify(url_for("index"))
	return render_template("review_deck.html")

@app.route("/deck/<int:deck_id>/create", methods=["GET","POST"])
@login_required
def create_card(deck_id):
	user_input = request.get_json()
	question=user_input.get("question").strip()
	answer=user_input.get("answer").strip()
	if question and answer:
		new_card = Card(question=user_input.get("question"), answer=user_input.get("answer"), deck_id=deck_id)
		db.session.add(new_card)
		db.session.commit()
		return jsonify(new_card)
	return "None"

@app.route("/deck/<int:deck_id>/delete", methods=["POST"])
@login_required
def delete_card(deck_id):
	card_id = request.get_json().get("id")
	print(card_id)
	card = Card.query.filter_by(id=card_id).first()

	db.session.delete(card)
	db.session.commit()

	return jsonify({"result":"OK"},200)

if __name__ == "__main__":
	app.run(host="localhost", port="8000", debug=True)