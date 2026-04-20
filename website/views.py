from flask import Blueprint, render_template, redirect, url_for
from flask import request
import os
from openai import OpenAI

# Create a blueprint
main_blueprint = Blueprint('main', __name__)
OPENAI_KEY = os.environ.get('OPEN_AI_KEY')


def translateAPI(to_translate, toSlang=False):

    content_text = (
        "Create a clear recipe based on this user request: "
        + to_translate
        + ". Return the recipe with a short title, an ingredients list, and numbered steps."
    )

    client = OpenAI(api_key=OPENAI_KEY)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        #store=True,
        messages=[
            {"role": "user", "content": content_text}
        ]
    )

    if completion.choices[0].message.content == None:
        return "Sorry, I don't understand that."
    
    return completion.choices[0].message.content


@main_blueprint.route('/', methods=['GET', 'POST'])
# @login_required
def main_page():
    return render_template('index.html')
    

@main_blueprint.route('/translate', methods=['GET', 'POST'])
def translate():

    if request.method == 'POST':

        # we got the request as a json object
        data = request.get_json()       
        # we use a function to communicate with the API
        translation = translateAPI(data['input'])

        # we return the result as a json object, notice no render_template
        result = {"translatedText": translation}
        return result