from project import db
from flask import redirect, url_for, jsonify
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin, SQLAlchemyStorage
from .models import OAuth

oauth_blueprint = make_github_blueprint(
    client_id="f1f02af13bed0c2b9b41",
    scope='user:email',
    client_secret="d4cbd754ff35dc501ff8c3ae3b49b3fba4ea6a7e",
    redirect_url="/login/github/authorized"
)

oauth_blueprint.storage = SQLAlchemyStorage(OAuth, db.session)

@oauth_blueprint.route("/login/github")
def index():
    return redirect(url_for("github.login"))
    if not github.authorized:
        resp = github.get("/user")
    assert resp.ok
    return "You are @{login} on GitHub".format(login=resp.json()["login"])

@oauth_blueprint.route("/login/github/authorized")
def after_authorized():
    if not github.authorized:
        return redirect(url_for("github.login"))
    rsp = github.get("/user")
    if rsp.status_code == 200:
        user = rsp.json()
    rsp = github.get("/user/emails")
    if rsp.status_code == 200:
        user['emails'] = rsp.json()
    return user, 200

