import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, current_app, url_for
from app.models import Asset

view = Blueprint("asset", __name__)


@view.route("/", methods=["GET"])
def index():
    assets = Asset.query.all()
    return render_template("/asset/index.html", assets=assets)


@view.route("/create", methods=["GET", "POST"])
def create():
    if request.method == 'POST':
        file = request.files.get('file')
        name = request.form.get('name')
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        if os.path.exists(filepath):
            pass # TODO: Handle error

        file.save(filepath)

        asset = Asset(name=name if name else filename, path=filepath, is_public=True)
        asset.save()
        
        return redirect(url_for('asset.index'))
    
    return render_template("/asset/create_or_edit.html")


@view.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    asset = Asset.query.get(id)
    if not asset:
        return "Asset not found", 404

    if request.method == 'POST':
        name = request.form.get('name')
        file = request.files.get('file')

        asset.name = name if name else asset.name

        if file and file.filename:
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

            if os.path.exists(asset.path):
                os.remove(asset.path) 

            file.save(filepath)
            asset.path = filepath

        asset.save()
        return redirect(url_for('asset.index'))

    return render_template("/asset/create_or_edit.html", asset=asset)



@view.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    asset = Asset.query.get(id)
    
    if request.method == 'POST':    
        if os.path.exists(asset.path):
            os.remove(asset.path)
            
        asset.delete()
        
        return redirect(url_for('asset.index'))
        
    return render_template("/asset/delete.html", asset=asset)