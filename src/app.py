from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def main():
    return '''
    <form action="/echo_user_input" method="POST">
        <input name="user_input">
        <input type="submit" value="Submit!">
    </form>    
    '''
z
@app.route("/echo_user_input", methods=["POST"])
def echo_input():
    input_text = request.form.get("user_input","")
    return f"You entered: {input_text}" 
