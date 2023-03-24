from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
openai.api_key = os.environ["API_KEY"]
@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})

@app.route("/test", methods=["GET"])
def suggestions():
    return "<h1>done</h1>"

@app.route("/generate-content", methods=["POST"])
def generateContent():
    # Get the input string from the request
    processInput = "Act as a copywriter and write a professional youtube video title " \
                   "and a pretty detailed description by using the input keyword." \
                   "Separate the title and description with a line space. Here is the keyword:  "
    processInput += request.json["input_string"]
    # Generate a response
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=processInput,
        temperature=0.5,
        max_tokens=2024,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=1
    )

    generated_sentences = response["choices"]

    # Get the first generated sentence
    generated_sentence = generated_sentences[0]["text"]

    # Create a JSON object containing the generated sentence
    result = {"generated_sentence": generated_sentence}
    return result

def generate_suggestions(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1000,
        n=1,
        temperature=0.7,
    )

    suggestions = [suggestion.text.strip() for suggestion in response.choices]
    # return up to 10 suggestions
    return suggestions

# define Flask endpoint
@app.route("/search-suggestions", methods=["POST"])
def suggestions():
    processInput = "Act as a search engine and give 10 search phrases without numbering based on this input: "
    # get prompt from request body
    processInput+= request.json["prompt"]

    # generate suggestions
    suggestions = generate_suggestions(processInput)

    # return JSON response
    return jsonify({"suggestions": suggestions})

@app.route("/test", methods=["GET"])
def suggestions():
    return "<h1>done</h1>"

@app.route("/keyword-suggestions-common", methods=["POST"])
def keywordSuggestionsCommon():
    processInput = "I want you to generate 20 keywords based on the input" \
                   "and tell the ranking competition whether it is low, high, or moderate, " \
                   "analysis, and volume of every keyword in the round brackets." \
                   " Here is the sample output: software development (low competition, high volume). " \
                   "Here is the input: "
    # get prompt from request body
    processInput+= request.json["prompt"]
    # generate suggestions
    suggestions = generate_suggestions(processInput)
    # return JSON response
    return jsonify({"suggestions": suggestions})

@app.route("/keyword-suggestions-uncommon", methods=["POST"])
def keywordSuggestionsUncommon():
    processInput = "I want you to generate 20 uncommon keywords based on the input" \
                   "and tell the ranking competition whether it is low, high, or moderate, " \
                   "analysis, and volume of every keyword in the round brackets." \
                   " Here is the sample output: software development (low competition, high volume). " \
                   "Here is the input: "
    # get prompt from request body
    processInput+= request.json["prompt"]
    # generate suggestions
    suggestions = generate_suggestions(processInput)
    # return JSON response
    return jsonify({"suggestions": suggestions})

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
