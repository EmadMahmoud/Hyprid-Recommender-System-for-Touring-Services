from flask.views import MethodView
from flask_smorest import Blueprint

from schemas import MatchSchema

blp = Blueprint("RECOMMENDER ENDPOINTS", __name__, description="4 endpoints"
                                                               " use the recommender system and the optimizer.")


@blp.route("/match")
class Match(MethodView):
    @blp.arguments(MatchSchema)
    def post(self, match_data):
        """
        This endpoint takes a user-dict and place ID and return
         the predicted rating .
        """

        return match_data


@blp.route("/recommendations")
class Recommendations(MethodView):
    def post(self):
        """
        This endpoint takes a user-dict and return
         will be the places ID's sorted as Top-N.
        """
        pass


@blp.route("/make-ai")
class MakeAI(MethodView):
    def post(self):
        """
        the back-end will send me a user-dict, The places ID's and positions,
        position entry point. the return will be an optimized plan.
        """
        pass


@blp.route("/make-manual")
class MakeManual(MethodView):
    def post(self):
        """
        the back-end will send me The places ID's and positions,
        position entry point. the return will be an optimized plan.
        """
        pass