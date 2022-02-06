from flask import Flask, flash, redirect, render_template, request
from twilio.rest import Client
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
app.config['SECRET_KEY'] = 'password'
app.run(debug=True)

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if 'quote' in incoming_msg:
        # return a quote
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'I could not retrieve a quote at this time, sorry.'
        msg.body(quote)
        responded = True
    if 'cat' in incoming_msg:
        # return a cat pic
        msg.media('https://cataas.com/cat')
        responded = True
    if not responded:
        msg.body('I only know about famous quotes and cats, sorry!')
    return str(resp)


if __name__ == '__main__':
    app.run()

@app.route('/')
def Index():
    return render_template('index.html')

@app.route('/about')
def About():
    return render_template('about.html')

@app.route('/handle_data', methods=['POST'])
def handle_data():
    nameForm = request.form['nameFormpath']
    phoneForm = request.form['phoneFormpath']
    flash('Submission Successful!')

    account_sid = 'AC3845e18a119c32dcff8bc6af2dc14079' 
    auth_token = '155ca39d35909ded613d11646e3645e3' 
    client = Client(account_sid, auth_token) 
    
    message = client.messages.create(  
                                messaging_service_sid='MGa8fdaf4f3a21336895f3f71f48fc00b1', 
                                body=f'Hey {nameForm}, this is Fin, ',      
                                to=f'+1{phoneForm}' 
                            ) 
 
    print(message.sid)


    return redirect(request.referrer)