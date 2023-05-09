from flask import Flask, request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
import pickle
import sys
sys.path.append('model')
from Model import Model

from schemas import MatchSchema

blp = Blueprint("RECOMMENDER ENDPOINTS", __name__, description="4 endpoints"
                                                               " use the recommender system and the optimizer.")
# Load the saved model object from disk
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)


@blp.route("/match")
class Match(MethodView):
    @blp.arguments(MatchSchema)
    @blp.response(200, MatchSchema)
    def post(self, match_data):
        """
        This endpoint takes a user-dict and place ID and return
         the predicted rating .
        """
        user_dict = match_data["user_dict"]
        place_id = match_data["place_id"]
        score = float(model.predict(user_dict, place_id, k=200))
        return jsonify({'similarity': score}), 200


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