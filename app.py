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
    resume['link'] = "https://example.com/resume.pdf"  

    result = collection.insert_one(resume)
    resume["_id"] = str(result.inserted_id)  # Convert ObjectId to string for JSON serialization
    return resume


@app.route('/get_resume', methods=['GET'])
def get_list():
    candidates = list(collection.find())
    for c  in candidates:
        c["_id"] = str(c["_id"])
    
    return render_template('list_candidate.html', applicants=candidates)

if __name__ == '__main__':
    app.run(debug=True , host="0.0.0.0", port=5000)