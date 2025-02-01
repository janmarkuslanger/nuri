from flask import Blueprint, render_template, request, redirect, url_for
from nuri.models import Role, WebhookType, RequestMethod, Webhook, WebhookItem
from nuri.utils.message import created_error, created_success, deleted_success, deleted_error
from nuri.views.auth import roles_required


view = Blueprint("webhook", __name__, url_prefix="/webhook")


@view.route("/")
@roles_required(Role.ADMIN)
def index():
    items = Webhook.query.all()
    return render_template("/webhook/index.html", items=items)


@view.route("/create", methods=["GET", "POST"])
@roles_required(Role.EDITOR, Role.ADMIN)
def create():
    if request.method == "POST":
        name = request.form.get("name")
        request_method = request.form.get("request_method")
        url = request.form.get("url")
        
        webhook = Webhook(
            name=name,
            request_method=request_method,
            url=url
        )
        
        for webhook_type in WebhookType:
            if request.form.get(webhook_type.name) == "on":
                webhook.items.append(WebhookItem(
                    type=webhook_type
                ))
            
        try:
            webhook.save()
            created_success("Webhook")
            return redirect(url_for("webhook.index"))
        except:
            created_error("Webhook")

    return render_template("webhook/create_or_edit.html", WebhookType=WebhookType, RequestMethod=RequestMethod)

@view.route("/edit/<int:id>", methods=["GET", "POST"])
@roles_required(Role.EDITOR, Role.ADMIN)
def edit(id):
    item = Webhook.query.get_or_404(id)
    
    if request.method == "POST":
        name = request.form.get("name")
        request_method = request.form.get("request_method")
        url = request.form.get("url")
        
        item.name = name
        item.request_method = request_method
        item.url = url
        
        item.items = []
        
        for webhook_type in WebhookType:
            if request.form.get(webhook_type.name) == "on":
                item.items.append(WebhookItem(
                    type=webhook_type
                ))
        try:
            item.save()
            created_success("Webhook")
            return redirect(url_for("webhook.index"))
        except:
            created_error("Webhook")

    return render_template(
        "webhook/create_or_edit.html",
        WebhookType=WebhookType,
        RequestMethod=RequestMethod,
        item=item,
        types=[ webhook_item.type for webhook_item in item.items if item and item.items ]
    )
    
@view.route("/delete/<int:id>", methods=["GET", "POST"])
@roles_required(Role.ADMIN)
def delete(id):
    item = Webhook.query.get_or_404(id)

    if request.method == "POST":
        try:
            item.delete()
            deleted_success("Webhook")
        except:
            deleted_error("Webhook")    
        
        return redirect(url_for("webhook.index"))

    return render_template("/webhook/delete.html", item=item)