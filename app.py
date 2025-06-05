from flask import Flask, request,  render_template , redirect , url_for
from bson.objectid import ObjectId
from pymongo import MongoClient
from scoring import resume_text_to_json , get_score 
from dotenv import load_dotenv
import os
import logging
load_dotenv()
uri = os.getenv("MONGODB_URI")
if not uri:
    raise RuntimeError("MONGODB_URI is not set!")

client = MongoClient(uri)
db = client["pfe_db"]
collection = db["candidates"]



app = Flask(__name__)

@app.route('/')
def hello():
    logging.info("Serving welcome page")
    return render_template('welcome.html')



@app.route('/add_resume' , methods=['POST' , 'GET'])
def add_resume():

    data = request.form.get('argument') # take data from html form

    if not data:
        data = request.args.get("argument")  # passing data from the URL query string for n8n integration
    resume  = resume_text_to_json(data)
    work_experience_score , skills_score , overall_score = get_score(resume) 
    resume.setdefault("scoring", {})  # creates scoring dict if not present
    resume['scoring']['work_experience_score'] = work_experience_score
    resume['scoring']['skills_score'] = skills_score
    resume['scoring']['overall_score'] = overall_score

    result = collection.insert_one(resume)
    resume["_id"] = str(result.inserted_id)  

    return resume #returning json for testing purposes


@app.route('/get_resume', methods=['GET'])
def get_list():
    candidates = list(collection.find())
    n = len (candidates)
    for i in range(n):
        for j in range(i-1):
            score_1 = candidates[i]['scoring']['overall_score']
            score_2 = candidates[j]['scoring']['overall_score']
            if score_1 > score_2:
                candidates[i], candidates[j] = candidates[j], candidates[i]

    return render_template('list_candidate.html', applicants=candidates)



@app.route('/delete_resume', methods=['POST'])
def delete_resume():
    resume_id = request.form.get('_id')
    if not resume_id:
        return redirect('/get_resume')

    try:
        obj_id = ObjectId(resume_id)
    except Exception:
        return redirect('/get_resume')

    collection.delete_one({"_id": obj_id})
    return redirect('/get_resume')


@app.route('/delete_all', methods=['GET '])
def delete_all_resumes():
    collection.delete_many({})
    return redirect('/get_resume')



@app.route("/check")
def check():  # this is only for deployment health check
    return "OK", 200

if __name__ == '__main__':
    app.run()