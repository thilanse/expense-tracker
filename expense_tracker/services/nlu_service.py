import requests

URL = "http://localhost:5005"

def get_nlu_prediction(query):

    model_parse_url = URL + "/model/parse"

    request_body = {
        'text': query
    }

    response = requests.post(model_parse_url, json=request_body).json()

    return response

def get_nlu_intent_prediction(query):

    model_prediction = get_nlu_prediction(query)

    return model_prediction["intent"]["name"]