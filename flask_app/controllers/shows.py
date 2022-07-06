
from flask import Flask, render_template, redirect, request, session, flash, url_for
from flask_app import app
from flask_app.models.show import Show
from flask_app.models.user import User


@app.route('/shows/new')
def newshow():
    return render_template("newshow.html")

@app.route('/addshow', methods = ['Post'])
def addshow():
    data = { 
        "title" : request.form["title"] 
        }
    show_exists = Show.get_show_by_title(data)
    if show_exists:
        flash("Show Already exists")
        return redirect("/shows/new")
    if not Show.validate_show(request.form):
        return redirect("/shows/new")
    else:
        data = {
            "user_id": session["user_id"],
            "title": request.form["title"],
            "network": request.form["network"],
            "release_date": request.form["release_date"],
            "description": request.form["description"]
        }
        Show.save(data)
        return redirect("/shows")


@app.route('/shows/<int:id>')
def recipe(id):
    count = 0
    data = {
        "id": id
    }
    users = User.get_all()
    show_likes = Show.get_show_by_like(data)
    shows = Show.get_show(data)
    if show_likes:
        likes = Show.how_many_liked(data)
        for like in likes.likes:
            count += 1
        return render_template("show.html", id = id, shows = shows, count = count, users = users)
    else:
        return render_template("show.html", id = id, shows = shows, count = count, users = users)


@app.route('/like', methods = ['Post'])
def likeshow():
    data = { 
        "show_id" : request.form["id"],
        "user_id": session["user_id"]
        }
    Show.likeshow(data)
    return redirect("/shows")


@app.route("/deletelike", methods = ['Post'])
def deletelike():
    data = {
        "show_id": request.form["id"],
        "user_id": session['user_id']
    }
    Show.deletelike(data)
    return redirect("/shows")


@app.route('/editshows/<int:id>')
def editshow(id):
    data = {
        "id": id
    }
    session['show_id'] = id
    shows = Show.get_show(data)
    return render_template("editshow.html", id = id, shows = shows)

@app.route('/updateshow', methods = ['Post'])
def updaterecipe():
    id = session['show_id']
    if not Show.validate_show(request.form):
        return redirect(url_for('editshow', id = session['show_id']))
    else:
        data = {
            "user_id": session["user_id"],
            "title": request.form["title"],
            "network": request.form["network"],
            "release_date": request.form["release_date"],
            "description": request.form["description"],
            "id" : id
        }
        Show.update(data)
        return redirect("/shows")

@app.route("/delete/<int:id>")
def delete(id):
    data = {
        "id": id
    }
    Show.delete(data)
    return redirect("/shows")