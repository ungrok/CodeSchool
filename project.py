
import bottle
from bottle.ext import sqlite
from bottle import HTTPError, response, request
from json import dumps
import macaron

app = bottle.Bottle()
plugin = sqlite.Plugin(dbfile='database.db')
app.install(plugin)

app.install(macaron.MacaronPlugin("database.db"))

class Skills(macaron.Model):
    title = macaron.CharField()
    description = macaron.CharField()
    url = macaron.CharField()
    image_path = macaron.CharField()
    
class Challenges(macaron.Model):
    title = macaron.CharField()
    description = macaron.CharField()
    image_url = macaron.CharField()
    skill = macaron.ManyToOne(Skills, related_name="skill")
        
def results(query):
    limit = int(request.params.get("limit", 20))
    if limit < 0 or limit > 100:
        limit = 20
    if "page" in request.params:
        page = int(request.params.get("page", 1))
        if page <= 0:
            page = 0
        offset = page * limit
    else:
        offset = int(request.params.get("offset", 0))
    if offset <= 0:
        offset = 0
    query_limit = offset + limit
    if isinstance(query, macaron.QuerySet):
        query = query[offset:query_limit]
    
    return { "head": 
             {"code":200,
              "status": "OK",
              "collection": 
              {"limit": limit,
               "offset": offset
           }},
             "response": query.dict }
def error(ex):
    return { "head": 
             {"code":404,
              "status": "Error",
              "collection": 
              {"limit": 0,
               "offset": 0
           }},
             "response": str(ex) }
    


@app.get('/skills')
def get_all_skills(db):
    try:
        skills = Skills.all()
        return results(skills)
    except Exception, ex:
        return error(ex)

@app.get('/skills/<t>')
def get_skills_by_title(t):
    try:
        skills = Skills.get(title=t)
        return results(skills)
    except Exception, ex:
        return error(ex)

@app.get('/skills/<skill_id:int>')
def skills_by_id(skill_id):
    return results(Skills.get(skill_id))


    return HTTPError(404, 'Page not found')

@app.get('/skills/<skill_id:int>/challenges/<challenge_id:int>')
def get_challenge_by_skill_id_and_challenge_id(skill_id, challenge_id):
    s = Skills.get(skill_id)
    challenge = Challenges.get(challenge_id, skill=s)
    return results(challenge)

@app.get('/join/<challenge_id:int>')
def join_awesomeness(challenge_id):
    challenge = Challenges.get(challenge_id)
    return {"challenge_title": challenge.title, 'skill_title': challenge.skill.title} 

@app.get('/skills/<skill_id>/challenges')
def get_all_challenges_by_skill_id(skill_id, db):
    results = []
    rows = db.execute('SELECT * FROM challenges WHERE skill_id=?', (skill_id,))
    if rows:
        for row in rows:
            results.append({'title': row['title']})
        return dumps(results)
    return HTTPError(404, 'Page not found')

@app.hook('after_request')
def set_headers():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

app.run(host='localhost', port=8080, debug=True)
