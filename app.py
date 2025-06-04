from flask import Flask, request, jsonify , render_template
import json 
from pymongo import MongoClient
from scoring import resume_text_to_json , get_score 

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
    resume  = resume_text_to_json(data)
    resume['score'] = get_score(resume) 

    result = collection.insert_one(resume)
    resume["_id"] = str(result.inserted_id)  # Convert ObjectId to string for JSON serialization
    return resume


@app.route('/get_resume', methods=['GET'])
def get_list():
    candidates = list(collection.find())
    n = len (candidates)
    for i in range(n):
        for j in range(i-1):
            score_1 = candidates[i]['score']
            score_2 = candidates[j]['score']

            if score_1 > score_2:
                candidates[i], candidates[j] = candidates[j], candidates[i]
    return render_template('list_candidate.html', applicants=candidates)

if __name__ == '__main__':
    app.run(debug=True , host="0.0.0.0", port=5000)