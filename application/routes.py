from flask import render_template, redirect, url_for, Response, request
from flask_login import login_user, current_user, logout_user, login_required
from application import app, db, password_hash as pw
from application.models import users, card_list, deck_list
import json
from application.forms import RegisterForm, LoginForm, CreateCard, CreateDeck, PasswordForm, AccountForm, EditCardForm, SearchCard

@app.route('/')
@app.route('/home') #done HTML
def home():
	return render_template('home.html', title='YuGiCRUD')

@app.route('/login', methods=['GET','POST']) #done HTML
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = users.query.filter_by(user_name=form.user_name.data).first()
        if user and pw.verify_password(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('dashboard'))
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET','POST']) #done HTML
def register():
    form = RegisterForm()
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if form.validate_on_submit():
        hashed = pw.hash_password(form.password.data)
        user = users(
            user_name=form.user_name.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password=hashed
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    else:
        print(RegisterForm.errors)
        return render_template('register.html', title='Register', form=form)

@app.route('/dashboard', methods=['GET','POST']) #done HTML
@login_required
def dashboard():
    query = deck_list.query.filter_by(user_ID=current_user.id).all()
    deck_names = []
    for row in query:
        deck_names.append(row.deck_name)
    deck_names = list(dict.fromkeys(deck_names))
    return render_template('dashboard.html', title='Dashboard', decks=deck_names)

@app.route('/admin', methods=['GET','POST']) #NEED HTML
@login_required
def admin():
    if current_user.admin == False:
        return redirect(url_for('home'))
    query = users.query.all()
    return render_template('admin.html', title='Admin Dashboard', user_list=query)

@app.route("/account", methods=['GET','POST']) #done HTML
@login_required
def account():
	form = AccountForm()
	if form.validate_on_submit():
		current_user.first_name = form.first_name.data
		current_user.last_name = form.last_name.data
		current_user.email = form.email.data
		db.session.commit()
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.first_name.data = current_user.first_name
		form.last_name.data = current_user.last_name
		form.email.data = current_user.email
	return render_template('account.html', title='Account', form=form)

@app.route("/change_password", methods=['GET','POST']) #done HTML
@login_required
def change_password():
	form = PasswordForm()
	if form.validate_on_submit():
		if pw.verify_password(current_user.password, form.current_password.data):
			hash = pw.hash_password(form.password.data)
			current_user.password = hash
			db.session.commit()
			return redirect(url_for('account'))
	else:
		return render_template('change_password.html', title='Change Password', form=form)

@app.route("/logout") #done
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))

@app.route("/edit_card/<card>", methods=['GET','POST']) #done HTML
@login_required
def edit_card(card, deck):
    form = EditCardForm()
    card = card_list.query.filter_by(card_name=card)
    if form.validate_on_submit():
        card.card_name = form.card_name.data
        card.card_attk = form.card_attk.data
        card.card_def = form.card_def.data
        db.session.commit()
        return redirect(url_for('deck', deck_id=deck))
    elif request.method == 'GET':
        form.card_name.data = card.card_name
        form.card_attk.data = card.card_attk
        form.card_def.data = card.card_def
    return render_template('edit_card.html', title=card, form=form)

@app.route("/create_card", methods=['GET','POST']) #done HTML
@login_required
def create_card():
    form = EditCardForm()
    if form.validate_on_submit():
        card = card_list(
            card_name = form.card_name.data,
            card_attk = form.card_attk.data,
            card_def = form.card_def.data
        )
        db.session.add(card)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('create_card.html', title=card, form=form)

@app.route("/edit_user", methods=['GET','POST']) #done HTML
@login_required
def edit_user(user_ID):
    form = AccountForm()
    user = users.query.filter_by(id=user_ID).first()
    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.user_name = form.user_name.data
        db.session.commit()
        return redirect(url_for('admin'))
    elif request.method == 'GET':
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.user_name.data = user.user_name
    return render_template('edit_user.html', title=user.user_name, form=form)

@app.route("/delete_user", methods=['GET','POST']) #done
@login_required
def delete_user(user_ID):
    deck_list.filter_by(user_ID=user_ID).delete()
    db.session.commit()
    users.query.filter_by(id=user_ID).delete()
    db.session.commit()
    return redirect(url_for('admin'))

@app.route("/remove_card/<card>", methods=['GET','POST']) #done
@login_required
def remove_card(card, deck):
    card_full = card_list.query.filter_by(card_name=card).first()
    deck_list.query.filter_by(deck_name=deck, card_ID=card_full.card_ID).delete()
    db.session.commit()
    return redirect(url_for('deck', deck_id=deck))

@app.route('/create_deck', methods=['GET','POST']) #done
@login_required
def create_deck():
    form = CreateDeck()
    if form.validate_on_submit():
        return redirect(url_for('deck', deck_id=form.deck_name.data))
    return render_template('create_deck.html', title='Create A Deck', form=form)
    
@app.route("/deck/<deck_id>", methods=['GET','POST']) #done HTML
@login_required
def deck(deck_id):
    query = deck_list.query.filter_by(deck_name=deck_id).all()
    if query:
        card_ids = []
        card_names = []
        for entry in query:
            card_ids.append(entry.card_ID)
        for card in card_ids:
            query = card_list.query.filter_by(card_ID=card).first()
            card_names.append(query.card_name, query.card_attk, query.card_def)
        return render_template('deck.html', title=deck_id, cards=card_names)
    else:
        return render_template('deck.html', title=deck_id, cards=[], deck_id=deck_id)

@app.route("/delete_deck/<deck>", methods=['GET','POST']) #done HTML
@login_required
def delete_deck(deck):
    query = deck_list.query.filter_by(deck_name=deck).delete()
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route("/add_card/<deck>", methods=['GET','POST']) #NEED HTML
@login_required
def add_card(deck):
    form = SearchCard()
    results = []
    if form.validate_on_submit:
        query = card_list.query.filter(card_list.card_name.ilike(form.card_search.data)).all()
        for entry in query:
            results.append(entry.card_name, entry.card_attk, entry.card_def)
        return render_template('add_card.html', title=deck, form=form, results=results)
    return render_template('add_card.html', title=deck, deck=deck, form=form, results=results)

@app.route("/confirm_card/<deck>/<card_name>", methods=['GET','POST']) #done
@login_required
def confirm_card(card_name, deck):
    card = card_list.query.filter_by(card_name=card_name).first()
    append_deck = deck_list(
        deck_name = deck,
        user_ID = current_user.id,
        card_ID = card.card_ID
    )
    db.session.add(append_deck)
    db.session.commit()
    return redirect(url_for('deck', deck_id=deck))

@app.route('/_autocomplete', methods=['GET']) #done
def autocomplete():
    query = card_list.query.all()
    cards = []
    for entry in query:
        cards.append(entry.card_name)
    return Response(json.dumps(cards), mimetype='application/json')
