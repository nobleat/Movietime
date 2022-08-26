from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.show import Show
from flask_app.models.user import User

@app.route('/addform')
def addpg():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        "id":session['user_id']
    }
    return render_template ("addshow.html", user=User.get_by_id(data))

@app.route("/create", methods=['POST'])
def create():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Show.validate_show(request.form):
        return redirect('/addform')
    data={
        "title": request.form["title"],
        "network": request.form["network"],
        "releasedate": request.form["releasedate"],
        "description": request.form["description"],
        "user_id": session["user_id"],
    }
    Show.create(data)
    return redirect("/dashboard")

@app.route("/delete/<int:id>")
def destroy(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        "id":id
    }
    Show.destroy(data)
    return redirect('/dashboard')

@app.route("/edit/show/<int:id>")
def editshow(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data= {
        "id":id
    }
    userdata={
        "id":session['user_id']
    }
    return render_template("editshow.html", show=Show.get_one(data), user=User.get_by_id(userdata))

@app.route("/update/show", methods=['POST'])
def update():
        if 'user_id' not in session:
            return redirect('/logout')
        if not Show.validate_show(request.form):
            return redirect('/addform')
        data={
            "title": request.form["title"],
            "network": request.form["network"],
            "releasedate": request.form["releasedate"],
            "description": request.form["description"],
            "id": request.form["id"],
        }
        Show.update(data)
        return redirect('/dashboard')

@app.route("/viewshow/<int:id>")
def view_show(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        "id":id
        }
    userdata={
        "id":session['user_id']
    }
    show=Show.get_one(data)
    print(show.postedby.first_name)
    return render_template("view.html", show=show, user=User.get_by_id(userdata))
