from flask import Flask, request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from optimizer import optimizer
import pickle
import sys
sys.path.append('model')
from Model import Model
import pandas as pd

from schemas import MatchSchema, RecommendationsSchema, ManualSchema, AISchema, MakeSquare

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
    @blp.arguments(RecommendationsSchema)
    @blp.response(200, RecommendationsSchema)
    def post(self, rec_data):
        """
        This endpoint takes a user-dict and return
         will be the places ID's sorted as Top-N.
        """
        # do the prediction on top_100 reviewed attractions
        data = pd.read_csv("data/attractions_cleaned.csv")
        ids = data["id"].tolist()
        reviews = data["num_reviews"].tolist()
        attr = [[x, y] for x, y in zip(ids, reviews)]
        id_filter = []

        for i in attr:
            if i[1] > 2000:  # 860 to get a 100 place
                id_filter.append(i[0])

        top_n = model.get_top_N(rec_data["user_dict"], id_filter)
        return jsonify({'Top_N Recommendations': top_n}), 200


@blp.route("/make-ai")
class MakeAI(MethodView):
    def search_csv_for_substring(self, filename, column, substring):
        data = pd.read_csv('data/finalofthefinal_filtered.csv')
        df = pd.read_csv(filename)
        matching_rows = df[df[column].str.contains(substring, case=False)]
        return matching_rows

    @blp.arguments(AISchema)
    @blp.response(200, AISchema)
    def post(self, ai_data):
        """
        the back-end will send me a user-dict, The places ID's and positions,
        position entry point. the return will be an optimized plan.
        """
        city = ai_data['city_name']
        start_position = ai_data["start_position"]
        num_days = ai_data["num_days"]
        data = self.search_csv_for_substring('data/finalofthefinal_filtered.csv', 'location_string', city)
        ids = data["id"].tolist()
        if data.shape[0]>100:
            reviews = data["num_reviews"].tolist()
            attr = [[x, y] for x, y in zip(ids, reviews)]
            id_filter = []

            for i in attr:
                if i[1] > 50:
                    id_filter.append(i[0])
            top_n = model.get_top_N(ai_data["user_dict"], id_filter)
        else:
            top_n = model.get_top_N(ai_data["user_dict"], ids)

        top_10 = top_n[:10]
        plan_ids = [x[0] for x in top_10]
        longitudes = []
        latitudes = []
        for i in plan_ids:
            matched_rows = data.loc[data['id'] == i]
            longitudes.append(float(matched_rows["longitude"]))
            latitudes.append(float(matched_rows["latitude"]))

        destination = [[x, y] for x, y in zip(longitudes, latitudes)]
        destination.insert(0, start_position)
        # des_tuples = [tuple(row) for row in destination]
        op = optimizer()
        plan = op.genrate_itinerary(destination, start=0, num_days=num_days)

        return jsonify({'The Plan': plan}), 200


@blp.route("/make-manual")
class MakeManual(MethodView):
    @blp.arguments(ManualSchema)
    @blp.response(200, ManualSchema)
    def post(self, manual_data):
        """
        the back-end will send me The places ID's and positions,
        position entry point. the return will be an optimized plan.
        """
        places_id = manual_data["places_id"]
        start_position = manual_data["start_position"]
        num_days = manual_data["num_days"]

        data = pd.read_csv("data/finaldata.csv")
        longitudes = []
        latitudes = []
        for i in places_id:
            matched_rows = data.loc[data['id'] == i]
            longitudes.append(float(matched_rows["longitude"]))
            latitudes.append(float(matched_rows["latitude"]))

        destination = [[x, y] for x, y in zip(longitudes, latitudes)]
        destination.insert(0, start_position)
        # des_tuples = [tuple(row) for row in destination]
        op = optimizer()
        plan = op.genrate_itinerary(destination, start=0, num_days=num_days)

        return jsonify({'The Plan': plan}), 200


@blp.route("/make-square")
class MakeSquare(MethodView):
    @blp.arguments(MakeSquare)
    @blp.response(200, MakeSquare)
    def post(self, square_data):
        data = pd.read_csv('data/finalofthefinal_filtered.csv')

        matched_rows = data.loc[data['id'] == square_data['place_id']]
        longitude, latitude = matched_rows['longitude'], matched_rows['latitude']
        location = []
        location.append(longitude)
        location.append(latitude)
        op = optimizer()
        location_box = op.generate_location_box(location, 5)

        return jsonify({"The square": location_box}), 200


