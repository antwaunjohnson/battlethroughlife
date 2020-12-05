from flask import flash
from api import db
from api.User.user_model import User, OAuth
from flask_login import current_user, login_user
from flask_dance.contrib.google import make_google_blueprint
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from sqlalchemy.orm.exc import NoResultFound


google_blueprint = make_google_blueprint(
    scope=['profile', 'email'],
    storage=SQLAlchemyStorage(OAuth, db.session, user=current_user)
)

# create/login local user on successful OAuth login
@oauth_authorized.connect_via(google_blueprint)
def google_logged_in(google_blueprint, token):
    if not token:
        flash("Failed to log in.", category="error")
        return False

    resp = google_blueprint.session.get("/oauth2/vs/userinfo")
    if not resp.ok:
        msg = "Failed to fetch user info."
        flash(msg, category="error")
        return False

    google_info = resp.json()
    google_user_id = google_info["id"]

    # Find this OAuth token in the database, or create it
    query = OAuth.query.filter_by(
        provider=google_blueprint.name, provider_user_id=google_user_id
    )
    try:
        oauth = query.one()
    except NoResultFound:
        google_user_login = str(google_info["email"])
        oauth = OAuth(
            provider=google_blueprint.name,
            provider_user_id=google_user_id,
            provider_user_login=google_user_login,
            token=token
        )
    
    if oauth.user:
        login_user(oauth.user)
        flash("Successfully signed in.")

    else:
        # Create a new local user account for the user
        user = User(username=google_info["email"])
        # Associate the new local user account with OAuth token
        oauth.user = user
        #Save and commit database models
        db.session.add_all([user, oauth])
        db.session.commit()
        # Log in the new local user account
        login_user(user)
        flash("Successfully signed in.")

    #Disable Flask-Dance's default behavor for saving the OAuth token
    return False


# create/login local user on successful OAuth login
@oauth_authorized.connect_via(google_blueprint)
def google_logged_in(google_blueprint, token):
    if not token:
        flash("Failed to log in with Google.", category="error")
        return

    resp = google_blueprint.session.get("/oauth2/v2/userinfo")
    if not resp.ok:
        msg = "Failed to fetch user info from Google."
        flash(msg, category="error")
        return

    google_info = resp.json()
    google_user_id = str(google_info["id"])

    # Find this OAuth token in the database, or create it
    query = OAuth.query.filter_by(
      provider=google_blueprint.name, provider_user_id=google_user_id
    )
    try:
        oauth = query.one()
    except NoResultFound:
        google_user_login = str(google_info["email"])
        oauth = OAuth(
            provider=google_blueprint.name,
            provider_user_id=google_user_id,
            provider_user_login=google_user_login,
            token=token
        )

    if current_user.is_anonymous:
        if oauth.user:
            #If the user is not loggin in and the token is linked,
            # log the user into the linked user account
            login_user(oauth.user)
            flash("Successfully signed in with Google")
        else:
            # If the user is not logged in and the token is unlinked,
            # create a new local user account and log that account in.
            # This means that one person can make multiple accounts, but it's OK becasue they can merge those accounts later.
            user = User(usernme=google_info["email"])
            oauth.user = user
            db.session.add_all([user, oauth])
            db.session.commit()
            login_user(user)
            flash("Successfully signed in with Google.")
    
    # Indicate that the backend shouldn't manage creating the OAuth object in the database, since we've already done so!
    return False

# notify on OAuth provider error
@oauth_error.connect_via(google_blueprint)
def google_error(google_blueprint, message, response):
    msg = ("OAuth error from {name}! " "message={message} response={response}").format(
        name=google_blueprint.name, message=message, response=response
    )
    flash(msg, category="error")
