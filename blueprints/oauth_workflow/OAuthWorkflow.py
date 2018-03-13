from flask import Blueprint, render_template, url_for, request, make_response, redirect
from flask_login import login_required

from CONSTANT import LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET, LINKEDIN_RETURN_URL, TWITTER_CLIENT_ID, \
    TWITTER_CLIENT_SECRET, TWITTER_REDIRECT_URL, TUMBLR_CLIENT_ID, TUMBLR_CLIENT_SECRET, TUMBLR_REDIRECT_URL, \
    FACEBOOK_CLIENT_ID, FACEBOOK_CLIENT_SECRET
from Forms.InstagramLoginForm import InstagramLoginForm
from SocialMedia.Facebook.Facebook import Facebook
from SocialMedia.LinkedIn.LinkedIn import LinkedInAuth
from blueprints.login.Login import get_current_user
from models.Credentials import get_credentials, save_credentials

oauth_workflow = Blueprint('OAuthWorkflow', __name__)


@oauth_workflow.route('/dashboard')
@login_required
def dashboard():
    # stored_c = get_cookie(request)
    stored_c = get_credentials(get_current_user())
    print("Stored Cookies:", stored_c)
    linkedin_auth = LinkedInAuth(LINKEDIN_CLIENT_ID,
                                 LINKEDIN_CLIENT_SECRET, LINKEDIN_RETURN_URL)

    from flask import session
    from SocialMedia.Twitter import TwitterAuth
    twitter_auth_url, key, secret \
        = TwitterAuth.get_authorization_url_auth(TWITTER_CLIENT_ID,
                                                 TWITTER_CLIENT_SECRET,
                                                 TWITTER_REDIRECT_URL)
    session['twitter_request_token'] = (key, secret)

    from SocialMedia.Tumblr.TumblrAuth import get_authorization_url
    tum_url, tum_key, tum_sec = get_authorization_url(TUMBLR_CLIENT_ID,
                                                      TUMBLR_CLIENT_SECRET,
                                                      TUMBLR_REDIRECT_URL)
    session['tumblr_request_token'] = (tum_key, tum_sec)

    return render_template('dashboard/dashboard.html',
                           facebook_client_id=FACEBOOK_CLIENT_ID,
                           linkedin_login=linkedin_auth.get_authorization_url(),
                           tumblr_login=tum_url,
                           twitter_login=twitter_auth_url,
                           instagram_login=url_for('OAuthWorkflow.instagram_login'))


@oauth_workflow.route('/facebook_redirect')
@login_required
def facebook_redirect():
    # We get this from dashboard.html as querystring
    access_token = request.args.get('accessToken')
    print("Facebook Access Token:", access_token)
    facebook_api = Facebook(FACEBOOK_CLIENT_ID,
                            FACEBOOK_CLIENT_SECRET,
                            access_token)
    access_token = facebook_api.generate_long_lived_token()
    print("Facebook Long Lived Access Token:", access_token)

    resp = make_response(redirect(url_for('OAuthWorkflow.dashboard')))
    # resp = set_cookie(resp=resp, facebook_access_token=access_token)

    save_credentials(get_current_user(), facebook_access_token=access_token)
    return resp


@oauth_workflow.route('/linkedin_redirect', methods=('GET', 'POST'))
@login_required
def linkedin_redirect():
    # We get this from dashboard.html as querystring
    linkedin_auth = LinkedInAuth(LINKEDIN_CLIENT_ID,
                                 LINKEDIN_CLIENT_SECRET,
                                 LINKEDIN_RETURN_URL)
    access_token = linkedin_auth.get_access_token_from_url(request.url)
    print("LinkedIn Access Token:", access_token)
    resp = make_response(redirect(url_for('OAuthWorkflow.dashboard')))
    # resp = set_cookie(resp=resp, linkedin_access_token=access_token)

    save_credentials(get_current_user(), linkedin_access_token=access_token)
    return resp


@oauth_workflow.route('/instagram_login', methods=('GET', 'POST'))
@login_required
def instagram_login():
    form = InstagramLoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        print("Instagram Username:", username)
        print("Instagram Password:", password)
        resp = make_response(redirect(url_for('OAuthWorkflow.dashboard')))
        # resp = set_cookie(resp=resp, instagram_email=username, instagram_password=password)

        save_credentials(get_current_user(), instagram_email=username, instagram_password=password)
        return resp
    return render_template('dashboard/instagram_login.html', form=form)


@oauth_workflow.route('/twitter_redirect', methods=('GET', 'POST'))
@login_required
def twitter_redirect():
    from flask import session
    from SocialMedia.Twitter.TwitterAuth import get_access_token_from_url

    token = session['twitter_request_token']
    del session['twitter_request_token']

    access_token, access_token_secret = \
        get_access_token_from_url(response_url=request.url,
                                  consumer_key=TWITTER_CLIENT_ID,
                                  consumer_secret=TWITTER_CLIENT_SECRET,
                                  token=token)

    resp = make_response(redirect(url_for('OAuthWorkflow.dashboard')))
    # resp = set_cookie(resp=resp, twitter_access_token=access_token,
    #                   twitter_access_secret=access_token_secret)

    save_credentials(get_current_user(), twitter_access_token=access_token,
                     twitter_access_secret=access_token_secret)
    return resp


@oauth_workflow.route('/tumblr_redirect', methods=('GET', 'POST'))
@login_required
def tumblr_redirect():
    from flask import session

    sess = session['tumblr_request_token']
    res_key = sess[0]
    res_sec = sess[1]
    del session['tumblr_request_token']

    from SocialMedia.Tumblr.TumblrAuth import get_access_token_from_url
    tokens = get_access_token_from_url(TUMBLR_CLIENT_ID, TUMBLR_CLIENT_SECRET,
                                       res_key, res_sec,
                                       request.url,
                                       callback_url=TUMBLR_REDIRECT_URL)

    print(tokens)
    resp = make_response(redirect(url_for('OAuthWorkflow.dashboard')))
    # resp = set_cookie(resp=resp, tumblr_access_token=tokens['oauth_token'],
    #                   tumblr_access_secret=tokens['oauth_token_secret'])

    save_credentials(get_current_user(), tumblr_access_token=tokens['oauth_token'],
                     tumblr_access_secret=tokens['oauth_token_secret'])

    return resp