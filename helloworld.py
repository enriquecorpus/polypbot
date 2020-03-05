import bot
import flask

app = flask.Flask(__name__)


@app.route('/')
def index():
    _polypbot = bot.PolypBot()
    _polypbot.run()
    response = app.response_class(
        response=flask.json.dumps({'status': 'ok'}),
        status=200,
        mimetype='application/json'
    )
    return response
