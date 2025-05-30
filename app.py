from flask import Flask, request, jsonify , render_template
app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')



@app.route('/adding' , methods=['GET'])
def check():
    name = request.args.get('argument')
    
    print("----",name )


    return jsonify({'message': "message"})

if __name__ == '__main__':
    app.run(debug=True)