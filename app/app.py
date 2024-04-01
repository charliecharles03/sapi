from flask import Flask
from .resources.auth.userAPI import UserAPI

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, world!'


app.add_url_rule('/api/userprofile/', view_func=UserAPI.as_view('user_profile'),methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True)

