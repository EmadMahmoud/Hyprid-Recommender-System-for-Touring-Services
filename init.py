import sys
import os
import pickle
script_directory = os.path.dirname(os.path.abspath("endpoints.py"))
sys.path.append(os.path.join(script_directory, './data'))
sys.path.append(os.path.join(script_directory, './model'))
from Model import Model

if __name__ == '__main__':
    model = Model()
    model.fit()

    # Save the model object to disk using pickle
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)

    u, i = '31447', '553171'
    print(model.predict(u, i))

    new_u = {553171: 4, 459804: 3, 308825: 5}
    score = float(model.predict(new_u, i, k=200))
    print(score)
    print(type(score))

    print(model.get_top_N(u, [553171, 459804, 308825]))
