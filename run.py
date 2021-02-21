import os  # os installed with python and os.environ mapping is captured
import json
from flask import Flask, render_template, request, flash  # flask installed with pip
if os.path.exists("env.py"):
    import env  # only imports env.py module if it exists in project root directory

app = Flask(__name__)  # 1st param needed to find templates and static files in project directory. (__name__ = __main__ if run.py is run directly)
app.secret_key = os.environ.get('SECRET_KEY')

@app.route("/")  # arg of app.route decorator defines the URL that should trigger the decorated function
def index():
    return render_template("index.html")


@app.route("/about/")  # trailing '/' in path resolves to both '/about/' and '/about'
def about():
    data = []
    with open("data/company.json") as json_data:
        data = json.load(json_data)

    return render_template("about.html", page_title="About", company=data)  # can pass any number of named arguments which will be available in context of the template

@app.route("/about/<member_name>/")  # member_name suffix (can be any string w/o '/' by default) from URL path is passed to decorated view function as named parameter
def about_member(member_name):  # this view func will be called whenever any URL of form "/about/<member_name>/" is looked up
    member = {}
    with open("data/company.json") as json_data:
        data = json.load(json_data)
        for obj in data:
            if obj["url"] == member_name:
                member = obj
    return render_template("member.html", member=member)

@app.route("/contact/", methods=["GET", "POST"])  
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        flash(f"Thanks {name}, we received your message!")
    return render_template("contact.html", page_title="Contact")


@app.route("/careers/")
def careers():
    return render_template("careers.html", page_title="Careers")


if __name__ == "__main__":  # checks run.py is not an imported module and is being run directly
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),  # os.environ is a mapping containing environment variables
        port=int(os.environ.get("PORT", "5000")),  # 2nd param of .get() is default value if key lookup fails
        debug=True,  # server will auto reload for code changes and display debugger upon exception
    )