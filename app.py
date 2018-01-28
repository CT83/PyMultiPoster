from datetime import datetime

from flask import Flask

app = Flask(__name__)


@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%h")

    return """         <div id="fb-root"></div>

        <script>
        window.fbAsyncInit = function() {
                FB.init({
                appId: '101206834030831',
                status: true,
                cookie: true,
                xfbml: true
            });
        };

        // Load the SDK asynchronously
        (function(d){
        var js, id = 'facebook-jssdk', ref = d.getElementsByTagName('script')[0];
        if (d.getElementById(id)) {return;}
        js = d.createElement('script'); js.id = id; js.async = true;
        js.src = "https://connect.facebook.net/en_US/all.js";
        ref.parentNode.insertBefore(js, ref);
        }(document));

        function login() {
            FB.login(function(response) {

            // handle the response
            console.log("Response goes here!");
            if (response.authResponse) {
             var access_token =   FB.getAuthResponse()['accessToken'];
             console.log('Access Token = '+ access_token);
             FB.api('/me', function(response) {
             console.log('Good to see you, ' + response.name + '.');
             });
           } else {
             console.log('User cancelled login or did not fully authorize.');
           }

            }, {scope: 'publish_actions'});            
        }

        function logout() {
            FB.logout(function(response) {
              // user is now logged out
            });
        }

        var status = FB.getLoginStatus();

        console.log(status);

        </script>

        <button onclick="javascript:login();">Login Facebook</button>

        <br>

        <button onclick="javascript:logout();">Logout from Facebook</button>
    """
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
