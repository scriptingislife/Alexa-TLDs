import requests
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session


help = "Say 'Alexa, ask random t. l. d. for a new domain.' "
welcome_msg = "Welcome to the Random T. L. D. skill. Would you like a random T. L. D. to explore?"
fallback = "Would you like a random T. L. D. to explore?"


app = Flask(__name__)
ask = Ask(app, "/")


@ask.launch
def new_session():
    return question(welcome_msg)


@ask.intent("AMAZON.YesIntent")
@ask.intent("RandomIntent")
def random_intent():
    readme = list(requests.get('http://data.iana.org/TLD/tlds-alpha-by-domain.txt').text.split('\n'))
    line_num = randint(0, len(readme))
    line = readme[line_num]
    while '-' in line:
        line_num = randint(0, len(readme))
        line = readme[line_num]

    response = "How about dot {}?".format(line)
    return statement(response)

@ask.intent("AMAZON.HelpIntent")
def help_intent():
    return question(help)


@ask.intent("AMAZON.FallbackIntent")
def fallback_intent():
    return statement(fallback)


@ask.intent("AMAZON.NoIntent")
@ask.intent("AMAZON.StopIntent")
@ask.intent("AMAZON.CancelIntent")
def stop():
    return statement("Goodbye.")


if __name__ == "__main__":
    app.run(debug=False, port=7000)