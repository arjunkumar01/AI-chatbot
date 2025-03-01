# importing the required modules
from flask import Flask, render_template, request, jsonify
import random
import json
import pickle
import numpy as np
import nltk
from nltk import WordNetLemmatizer
from tensorflow.keras.models import load_model

# download the nltk packages
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')

# intialize the flask app
app = Flask(__name__)

# load the data and model
lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))

chatbot_model = load_model('pikart_customer_service_chatbot.h5')

# function for cleaning the sentence
def clean_up_sentence(sentence):
    #tokensize
    sentence_words = nltk.word_tokenize(sentence)

    #lemmatize
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]

    return sentence_words

# function to create bag of words
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)

    bag = [0]*len(words)

    # create bag
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1

    return np.array(bag)

# function for getting class
def predict_class(sentence):
    bow = bag_of_words(sentence)

    res = chatbot_model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25

    # filter the predictions using the threshold
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    # sort the results in descending order
    results.sort(key=lambda X: X[1], reverse=True)

    return_list = []

    # create a list of intents and probabilities
    for r in results:
        return_list.append({'intents': classes[r[0]], 'probability': str(r[1])})

    return return_list

# get response from chatbot
def get_response(intents_list, intents_json):
    tag = intents_list[0]['intents']

    list_of_intents = intents_json['intents']
    
    # search for the matching intent tag
    for i in list_of_intents:
        if i['tag'] == tag:
            #choose random response from set of responses
            result = random.choice(i['responses'])
            break

    return result


@app.route("/")
def home():
    return render_template('index.html')

# define the route of chatbot
@ app.route("/chat", methods=['POST'])
def chat():
    # get the user sentence
    user_message = request.json.get("message")

    #predict the intent
    ints = predict_class(user_message)

    #get a response
    res = get_response(ints, intents)

    #return the response
    return jsonify({"response": res})

# run the app
if __name__ == "__main__":
    app.run(debug=True)