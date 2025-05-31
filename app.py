from flask import Flask, request, jsonify , render_template
import json 
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["pfe_db"]
collection = db["students"]

app = Flask(__name__)
@app.route('/')
def hello():
    return render_template('index.html')



@app.route('/add_resume' , methods=['POST' , 'GET'])
def add_resume():

    data = request.form.get('argument') # this was taken from the HTML form

    if not data:
        data = request.args.get("argument")  # fallback to query parameter if form data is not present

    json_resume = resume_text_to_json(data) 

    result = collection.insert_one(json_resume)    
    json_resume["_id"] = str(result.inserted_id)

    return json_resume









def resume_text_to_json(resume):
    clean_text = resume.encode().decode('unicode_escape')
    data = json.loads(clean_text)
    return data 


if __name__ == '__main__':
    app.run(debug=True , host="0.0.0.0", port=5000)