import sqlite3

import click
from flask import Flask, render_template, g, current_app, request
from flask.cli import with_appcontext


app = Flask(__name__)
DATABASE_PATH = 'db/store.db'
SCHEMA_PATH = "db/store_schema.sql"


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            DATABASE_PATH,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def init_db():
    db = get_db()
    with current_app.open_resource(SCHEMA_PATH) as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else []) if one else rv



@app.route("/")
def home():
    # Filters options.
    min_lens_d = request.args.get("min__lens_diameter", '')
    max_lens_d = request.args.get("max__lens_diameter", '')

    min_side_l = request.args.get("min__side_length", '')
    max_side_l = request.args.get("max__side_length", '')

    min_bridge_w = request.args.get("min__bridge_width", '')
    max_bridge_w = request.args.get("max__bridge_width", '')

    brand = request.args.get('brand', '')
    model = request.args.get('model', '')

    products = []

    filters = {
        "min_lens_d": min_lens_d,
        "max_lens_d": max_lens_d,
        "min_side_l": min_side_l,
        "max_side_l": max_side_l,
        "min_bridge_w": min_bridge_w,
        "max_bridge_w": max_bridge_w,
        "brand": brand,
        "model": model
    }

    if request.args.get("filter") and request.args.get("filter") == "True":
        query = "SELECT * FROM product WHERE 1=1 "
    else:
        return render_template("home.html", data={"products": query_db("SELECT * FROM product"), "filters": filters})

    if min_lens_d:
        query += " AND lens_diameter >= {} ".format(min_lens_d)
    if max_lens_d:
        query += " AND lens_diameter <= {}".format(max_lens_d)

    if min_bridge_w:
        query += " AND bridge_width >= {} ".format(min_bridge_w)
    if max_bridge_w:
        query += " AND bridge_width <= {} ".format(max_bridge_w)

    if min_side_l:
        query += " AND side_length >= {} ".format(min_side_l)
    if max_side_l:
        query += " AND side_length <= {} ".format(max_side_l)

    if brand:
        query += " AND brand='{}'".format(brand)

    if model:
        query += " AND model='{}'".format(model)

    try:
        products = query_db(query)
    except sqlite3.OperationalError as e:
        print(e)

    return render_template("home.html", data={"products": products, "filters": filters})

@app.route('/g1')
def abc():
    query = "SELECT * FROM product WHERE name='Glasses 2'"
    products = query_db(query)
    return render_template('details.html',data={"products": products})



app.teardown_appcontext(close_db)
app.cli.add_command(init_db_command)

if __name__ == '__main__':
    app.run(debug=True)
