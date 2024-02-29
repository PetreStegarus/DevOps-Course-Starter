from flask import Flask, render_template, request, redirect, url_for
from todo_app.data.session_items import get_items, add_item, save_item

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    return render_template('index.html', items=get_items())


@app.route('/items', methods=['POST'])
def post_item():
    add_item(request.form['item-title'])
    return redirect(url_for('index'))


@app.route('/complete_item', methods=['POST'])
def complete_item():
    save_item(
        {
            "id": request.form['item-id'],
            "status": "Done",
        }
    )
    return redirect(url_for('index'))
