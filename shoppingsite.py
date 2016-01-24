"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken.
"""


from flask import Flask, render_template, redirect, flash, session, request
import jinja2

import melons, customers


app = Flask(__name__)

# Need to use Flask sessioning features

app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    return render_template("all_melons.html",
                           melon_list=melon_list)


# <int:melon_id> pass the melon_id parameter between the angle bracket
# from url in the route as an integer

@app.route("/melon/<int:melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)
    print melon
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def shopping_cart():
    """Display content of shopping cart."""

    melon_order = {}
    total_cost = 0
    
    # if user skips the "Add to Cart" step, session is empty
    # and does not have a "cart" key
    # if melon is added, 
    # session stores in the "cart" key a list of melon_id.

    if "cart" in session:
        melon_id_list = session['cart']

        for m_id in melon_id_list:
            melon = melons.get_by_id(m_id)
            
            # initialize melon_order dict with aggregated info
            # about melon of the same type
            # "key" in this dict is a melon object

            if melon not in melon_order:
                melon_order[melon] = {
                                        "price": melon.price,
                                        "name" : melon.common_name,
                                        "quantity": 1,
                                        "subtotal": melon.price
                }

            else:
                melon_order[melon]["quantity"] += 1
                melon_order[melon]['subtotal'] += melon.price


    # convert melon_order from a dict to a list of dicts
    # new melon_order follows a format of [{'name': , 'price': , 
    # 'quantity':, 'subtotal':}]
    # easier to access than a dict of dicts

    melon_order = melon_order.values()

    print melon_order

    if melon_order:
        for melon in melon_order:
            total_cost += melon['subtotal']

    return render_template("cart.html", melon_order=melon_order, 
                                        total_cost=total_cost)


@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Successfully added to cart'.
    """
    # On adding an item, check to see if the session contains a cart already.
    # to avoid key error, check cart in session or get() method (return None)

    if session.get('cart'):
        session['cart'].append(id)
    else:
        session['cart'] = [id]
 
    flash("Melon successfully added to cart.")

    return redirect("/cart")


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    email_submitted = request.form.get("email")
    password_submitted = request.form.get("password")
    
    # access customer_info dict in customers.py
    # use namespace customers.customer_info

    if email_submitted in customers.customer_info:
        customer = customers.get_by_email(email_submitted)
        if customer.password == password_submitted:
            session["logged_in_customer_email"] = email_submitted
            flash("Login successful.")
            return redirect("/melons")
        else:
            flash("Incorrect password.")
            return redirect("/login")
    else:
        flash("No such email.")
        return redirect("/login")

@app.route("/logout")
def process_logout():
    """Log user out of site"""

    # pop(key[, default])
    # If key is in the dictionary, remove it and return its value, 
    # else return default. 
    # If default is not given and key is not in the dictionary, 
    # a KeyError is raised

    del session["logged_in_customer_email"]
    flash("Logout successful.")
    return redirect("/melons")

@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True)
