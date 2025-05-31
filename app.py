from flask import Flask, request, jsonify , render_template
app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')



@app.route('/adding' , methods=['POST' , 'GET'])
def check():

    data = request.form.get('argument') # this was taken from the HTML form

    if not data:
        data = request.args.get("argument")  # fallback to query parameter if form data is not present

    return jsonify({'message': f'You entered: {data}'})


if __name__ == '__main__':
    app.run(debug=True)