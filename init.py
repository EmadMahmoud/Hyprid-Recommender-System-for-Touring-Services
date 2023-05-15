import sys
import os
import pickle
import pandas as pd

sys.path.append('model')

# script_directory = os.path.dirname(os.path.abspath("endpoints.py"))
# sys.path.append(os.path.join(script_directory, './data'))
# sys.path.append(os.path.join(script_directory, './model'))
# from Model import Model

if __name__ == '__main__':


    # Save the model object to disk using pickle
    # model = Model()
    # model.fit()
    # with open('model.pkl', 'wb') as f:
    #     pickle.dump(model, f)

    # Load the saved model object from disk
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)

    # u, i = '31447', '553171'
    # print(model.predict(u, i))
    #
    new_u = {553171: 4, 459804: 3, 308825: 5}
    # score = float(model.predict(new_u, i, k=200))
    # print(score)
    #
    # print(model.get_top_N(u, [553171, 459804, 308825]))

    data = pd.read_csv("data/attractions_cleaned.csv")
    # do the prediction on random 100 attraction
    # first_column = data["id"].tolist()
    # attr_ids = list(set(first_column))
    # attr50 = attr_ids[:100]
    # print(model.get_top_N(new_u, attr50))

    # do the prediction on top_100 reviewed attractions
    ids = data["id"].tolist()
    reviews = data["num_reviews"].tolist()
    attr = [[x, y] for x, y in zip(ids, reviews)]
    id_filter = []

    for i in attr:
        if i[1] > 4000:  # 860 to get a 100 place
            id_filter.append(i[0])

    print(model.get_top_N(new_u, id_filter))
