########IMPORT CONFIG############
import sys
sys.path.append('/var/www/html')
from include.api import *
#################################


app = Flask(__name__)
api = Api()

class Main(Resource):
    def post(self, method):
        parser = reqparse.RequestParser()
        parser.add_argument("data", type=dict)
        data = parser.parse_args()

        Bot = tg.TelegramUserAPI(bot_id=data['data']['bot_id'])

        context = mp.get_context('spawn')
        answer = context.Queue()
        new_process = context.Process(target=Bot.routeApi, args=(method, data['data'], answer,), daemon=False)
        new_process.start()
        response = answer.get()
        new_process.join()
        return response

api.add_resource(Main, "/methods/<string:method>")
api.init_app(app)


if __name__ == "__main__":
    app.run(host="62.217.179.39", port=5000, debug=False)