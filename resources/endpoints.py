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
        user-dict: keys(int), values(int).
        place_id: integer

        """
        try:
            user_dict = match_data["user_dict"]
            place_id = match_data["place_id"]
            score = float(model.predict(user_dict, place_id, k=200))
            return jsonify({'similarity': score}), 200
        except:
            return jsonify({'server_default': 3.953258745}), 200


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
        try:
            data = pd.read_csv("data/attractions_cleaned.csv")
            ids = data["id"].tolist()
            reviews = data["num_reviews"].tolist()
            attr = [[x, y] for x, y in zip(ids, reviews)]
            id_filter = []

            for i in attr:
                if i[1] > 2000:  # 860 to get a 100 place
                    id_filter.append(i[0])

            top_n = model.get_top_N(rec_data["user_dict"], id_filter)
            result = {item[0]: item[1] for item in top_n}
            return jsonify({'Top_N_Recommendations': result}), 200
        except:
            return jsonify({
                "server_default": [
                    [
                        308825,
                        3.8336775330925805
                    ],
                    [
                        1216558,
                        3.3712502447045107
                    ],
                    [
                        20398123,
                        3.3045898493621824
                    ],
                    [
                        7736828,
                        3.281773145019484
                    ],
                    [
                        1432066,
                        3.2328487279129767
                    ]]})


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
        the user will send me a user-dict, start location,
        number of days, city name. the return will be an optimized plan.
        user-dict: keys(int), values(int).
        start_position: list of two float values as longitude and latitude.
        num_days: Integer number but must be less than 7.
        city_name: string.
        """
        try:
            city = ai_data['city']

            longitude = ai_data["longitude"]
            latitude = ai_data["latitude"]
            start_position = [longitude, latitude]
            num_days = ai_data["days"]
            data = self.search_csv_for_substring('data/finalofthefinal_filtered.csv', 'location_string', city)
            ids = data["id"].tolist()
            if data.shape[0] > 50:
                reviews = data["num_reviews"].tolist()
                attr = [[x, y] for x, y in zip(ids, reviews)]
                id_filter = []

                for i in attr:
                    if i[1] > 200: # will return 20 place with Alexandria
                        id_filter.append(i[0])
                top_n = model.get_top_N(ai_data["user_dict"], id_filter)
            else:
                top_n = model.get_top_N(ai_data["user_dict"], ids)

            top_10 = top_n[:num_days*2]
            plan_ids = [x[0] for x in top_10]

            longitudes = []
            latitudes = []
            for i in plan_ids:
                matched_rows = data.loc[data['id'] == i]
                longitudes.append(float(matched_rows["longitude"].iloc[0]))
                latitudes.append(float(matched_rows["latitude"].iloc[0]))

            destination = [[x, y] for x, y in zip(longitudes, latitudes)]
            destination.insert(0, start_position)
            op = optimizer()
            plan = op.genrate_itinerary(destination, start=0, num_days=num_days)
            updatedplan = []
            for li in plan:
                li.pop(0)
                temp = [value - 1 for value in li]
                tempid = []
                for item in temp:
                    for i in range(len(plan_ids)):
                        if item == i:
                            tempid.append(plan_ids[i])
                updatedplan.append(tempid)

            return jsonify({'plan': updatedplan}), 200
        except:
            return jsonify({"server_default": [[2706184, 16962913],
                                               [1725002, 13136186, 3838091],
                                               [10438680, 459902],
                                               [550320],
                                               [1997633],
                                               [4817133, 2615654]]}), 200


@blp.route("/make-manual")
class MakeManual(MethodView):
    @blp.arguments(ManualSchema)
    @blp.response(200, ManualSchema)
    def post(self, manual_data):
        """
        the user will send me The places ID's,
        start position, number of days. the return will be an optimized plan.
        ID's: list of integers.
        start position: list of two float values as longitude and latitude.
        number of days: Integer number but must be less than 7.
        """
        try:
            places_id = manual_data["places_id"]
            longitude = manual_data["longitude"]
            latitude = manual_data["latitude"]
            start_position = [longitude, latitude]
            num_days = manual_data["days"]
            if num_days > len(places_id):
                return jsonify({"no plan": "make sure the amount of days you entered"
                                           " are less than the places you choose."}), 400

            data = pd.read_csv("data/finaldata.csv")
            longitudes = []
            latitudes = []
            for i in places_id:
                matched_rows = data.loc[data['id'] == i]
                longitudes.append(float(matched_rows["longitude"].iloc[0]))
                latitudes.append(float(matched_rows["latitude"].iloc[0]))

            destination = [[x, y] for x, y in zip(longitudes, latitudes)]
            destination.insert(0, start_position)
            op = optimizer()
            plan = op.genrate_itinerary(destination, start=0, num_days=num_days)
            updatedplan = []
            for li in plan:
                li.pop(0)
                temp = [value - 1 for value in li]
                tempid = []
                for item in temp:
                    for i in range(len(places_id)):
                        if item == i:
                            tempid.append(places_id[i])
                updatedplan.append(tempid)

            return jsonify({'plan': updatedplan}), 200
        except:
            return jsonify({"server_default": [[2706184, 16962913],
                                               [1725002, 13136186, 3838091],
                                               [10438680, 459902],
                                               [550320],
                                               [1997633],
                                               [4817133, 2615654]]}), 200


@blp.route("/make-square")
class MakeSquare(MethodView):
    @blp.arguments(MakeSquare)
    @blp.response(200, MakeSquare)
    def post(self, square_data):
        try:
            data = pd.read_csv('data/finalofthefinal_filtered.csv')

            matched_rows = data.loc[data['id'] == square_data['place_id']]
            longitude, latitude = matched_rows['longitude'], matched_rows['latitude']
            location = []
            location.append(longitude)
            location.append(latitude)
            op = optimizer()
            location_box = op.generate_location_box(location, 5)

            return jsonify({"Loc_box": location_box}), 200
        except:
            return jsonify({
                "Loc_box": {
                    "max_lat": 30.074066009716738,
                    "max_lon": 31.311757508447283,
                    "min_lat": 29.98413399028327,
                    "min_lon": 31.207882491552724
                }
            }), 200


