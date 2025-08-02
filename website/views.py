# contains standard website routes & endpoints
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

# blueprint of the flask app
views = Blueprint('views', __name__) #name of the blueprint in ''

# defining a view
@views.route('/', methods=['GET', 'POST']) # / = decorator for the homepage/root
# user must be logged in to access home page
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short.', category="error")
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added.', category='success')
            
    return render_template("home.html", user=current_user)

# takes request JSON data (which is sent to index.js), turn it into a python dictionary object, so we can access the noteID.
# then, look for the note with that ID, check if it exists, and if the user owns that note, then we delete it. then empty response.
@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteID = note['noteID']
    note = Note.query.get(noteID)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash('Note deleted.', category="success")
            
    return jsonify({})