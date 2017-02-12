import RPi.GPIO as GPIO
from flask import Flask, render_template  # , request
app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

pins = {
    23: {'name': 'GPIO 23', 'state': GPIO.LOW},
    24: {'name': 'GPIO 24', 'state': GPIO.LOW}
}


# App routes {{{1
@app.route('/gpio')  # {{{2
def main():
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)
        # Put the pin dictionary into the template data dictionary:
        templateData = {'pins': pins}
    return render_template('main.html', **templateData)


# function executed when URL requested with pin # and action:
@app.route("/<changePin>/<action>")  # {{{2
def action(changePin, action):
    # Convert the pin from the URL into an integer:
    changePin = int(changePin)
    # Get the device name for the pin being changed:
    deviceName = pins[changePin]['name']
    if action == "on":
        # Set the pin high:
        GPIO.output(changePin, GPIO.HIGH)
        # Save the status message to be passed into the template:
        message = "Turned " + deviceName + " on."
    if action == "off":
        GPIO.output(changePin, GPIO.LOW)
        message = "Turned " + deviceName + " off."
    print("message: ", message)
    # Read the pin state and store it in the pins dictionary:
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)
    # Put the message into the template data dictionary:
    templateData = {
        'pins': pins
    }

    return render_template('main.html', **templateData)


@app.route('/hello/<name>')  # {{{2
def hello(name):
        return render_template('page.html', name=name)


@app.route('/')  # {{{2
def index():
        return render_template('index.html')


if __name__ == "__main__":  # {{{1
    app.run(host='0.0.0.0', port=80, debug=True)
