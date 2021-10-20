from google.cloud import datastore
from flask import Flask, request
import json
import constants

app = Flask(__name__)
client = datastore.Client()

@app.route('/')
def index():
    return "Please navigate to /boats to use this API"\

@app.route('/boats', methods=['POST','GET'])
def boats_get_post():
    if request.method == 'POST':
        content = request.get_json()        
        if "name" in content and "type" in content and "length" in content:
            new_boat = datastore.entity.Entity(key=client.key(constants.boats))
            new_boat.update({"name": content["name"], "type": content["type"],
            "length": content["length"]})
            client.put(new_boat)
            return ({"name": content["name"], "type": content["type"],
            "length": content["length"], "id": new_boat.key.id, "self": "https://hw3-almahmoa.wl.r.appspot.com/boats/"+ str(new_boat.key.id)}, 201)
        return ({"Error" : "The request object is missing at least one of the required attributes"},400)        
    elif request.method == 'GET':
        query = client.query(kind=constants.boats)
        results = list(query.fetch())
        for e in results:
            e["id"] = e.key.id        
        return (json.dumps(results), 200)
    else:
        return 'Method not recognized'

@app.route('/boats/<id>', methods=['PUT','DELETE','GET', 'PATCH'])
def boats_put_delete(id):
    if request.method == 'PUT':
        content = request.get_json()
        boat_key = client.key(constants.boats, int(id))
        boat = client.get(key=boat_key)
        boat.update({"name": content["name"], "type": content["type"],
          "length": content["length"]})
        client.put(boat)
        return ('',200)
    elif request.method == 'DELETE':
        boat_key = client.key(constants.boats, int(id))
        boat = client.get(key=boat_key)
        if boat is None:
            return ({"Error" : "No boat with this boat_id exists"},404)  
        client.delete(boat_key )
        return ('',204)
    elif request.method == 'GET':
        boat_key = client.key(constants.boats, int(id))        
        boat = client.get(key=boat_key)
        if boat is None:
            return ({"Error" : "No boat with this boat_id exists"},404)         
        return {"name": boat["name"], "type": boat["type"],
            "length": boat["length"], "id": id, "self": "https://hw3-almahmoa.wl.r.appspot.com/boats/"+ str(id)}
    elif request.method == 'PATCH':
        content = request.get_json()
        if "name" in content and "type" in content and "length" in content:
            boat_key = client.key(constants.boats, int(id))
            boat = client.get(key=boat_key)
            if boat is None:
                return ({"Error" : "No boat with this boat_id exists"},404)  
            boat.update({"name": content["name"], "type": content["type"],
            "length": content["length"]})
            client.put(boat)
            return ( {"name": boat["name"], "type": boat["type"],
                "length": boat["length"], "id": id, "self": "https://hw3-almahmoa.wl.r.appspot.com/boats/"+ str(id)},200)
        return ({"Error" : "The request object is missing at least one of the required attributes"},400)      
    else:
        return 'Method not recognized'

@app.route('/slips', methods=['POST','GET'])
def slips_get_post():
    if request.method == 'POST':
        content = request.get_json()        
        if "number" in content:
            new_slip = datastore.entity.Entity(key=client.key(constants.slips))
            if "current_boat" in content:
                cur_boat = content["current_boat"]
                new_slip.update({"number": content["number"], "current_boat": cur_boat})
            else:
                cur_boat = None
                new_slip.update({"number": content["number"], "current_boat": cur_boat})
            client.put(new_slip)
            return ({"number": content["number"], "current_boat": cur_boat, "id": new_slip.key.id, "self": "https://hw3-almahmoa.wl.r.appspot.com/slips/"+ str(new_slip.key.id)}, 201)
        return ({"Error" : "The request object is missing the required number"},400)        
    elif request.method == 'GET':
        query = client.query(kind=constants.slips)
        results = list(query.fetch())
        for e in results:
            e["id"] = e.key.id       
        return (json.dumps(results), 200)
    else:
        return 'Method not recognized'

@app.route('/slips/<id>', methods=['PUT','DELETE','GET', 'PATCH'])
def slips_put_delete(id):
    if request.method == 'PUT':
        content = request.get_json()
        slip_key = client.key(constants.slips, int(id))
        slip = client.get(key=slip_key)
        slip.update({"number": content["number"], "current_boat": content["current_boat"]})
        client.put(slip)
        return ('',200)
    elif request.method == 'DELETE':
        slip_key = client.key(constants.slips, int(id))        
        slip = client.get(key=slip_key)
        if slip is None:
            return ({"Error" : "No slip with this slip_id exists"},404) 
        client.delete(slip_key)
        return ('',204)
    elif request.method == 'GET':
        slip_key = client.key(constants.slips, int(id))        
        slip = client.get(key=slip_key)
        if slip is None:
            return ({"Error" : "No slip with this slip_id exists"},404)
        if slip["current_boat"] is None:
             return {"number": slip["number"], "current_boat": slip["current_boat"],
                "id": id, "self": "https://hw3-almahmoa.wl.r.appspot.com/slips/"+ str(id)}
        if "current_boat" in slip:        
            boat_key = client.key(constants.boats, int(slip["current_boat"]))
            boat = client.get(key=boat_key)        
        if boat is None:
            slip.update({"number": slip["number"], "current_boat": None})
            client.put(slip)
        return {"number": slip["number"], "current_boat": slip["current_boat"],
                "id": id, "self": "https://hw3-almahmoa.wl.r.appspot.com/slips/"+ str(id)}
    elif request.method == 'PATCH':
        content = request.get_json()
        if "number" in content:
            slip_key = client.key(constants.slips, int(id))
            slip = client.get(key=slip_key)
            if slip is None:
                return ({"Error" : "No slip with this slip_id exists"},404)   
            slip.update({"number": content["number"], "current_boat": content["current_boat"]})
            client.put(slip)
            return ( {"number": slip["number"], "current_boat": slip["current_boat"],
                "id": id, "self": "https://hw3-almahmoa.wl.r.appspot.com/slips/"+ str(id)},200)
        return ({"Error" : "The request object is missing at least one of the required attributes"},400)      
    else:
        return 'Method not recognized'

@app.route('/slips/<s_id>/<b_id>', methods=['PUT','DELETE','GET', 'PATCH'])
def slips_boats_put_delete(s_id, b_id):
    if request.method == 'PUT':
        content = request.get_json()
        slip_key = client.key(constants.slips, int(s_id))
        slip = client.get(key=slip_key)
        boat_key = client.key(constants.boats, int(b_id))
        boat = client.get(key=boat_key)
        if slip and boat:
            if slip["current_boat"] is None:
                slip.update({"number": slip["number"], "current_boat": int(b_id)})
                client.put(slip)
                return ('', 204)
            return ({"Error":"The slip is not empty"}, 403)
        return ({"Error":"The specified boat and/or slip does not exist"}, 404)
    elif request.method == 'DELETE':
        slip_key = client.key(constants.slips, int(s_id))
        slip = client.get(key=slip_key)
        boat_key = client.key(constants.boats, int(b_id))
        boat = client.get(key=boat_key)
        if slip and boat:
            if slip["current_boat"] == int(b_id):
                slip.update({"number": slip["number"], "current_boat": None})
                client.put(slip)
                return ('',204)
        return ({"Error":"No boat with this boat_id is at the slip with this slip_id"}, 404)
    elif request.method == 'GET':
        slip_key = client.key(constants.slips, int(id))        
        slip = client.get(key=slip_key)
        if slip is None:
            return ({"Error" : "No slip with this slip_id exists"},404)         
        return {"number": slip["number"], "current_boat": slip["current_boat"],
            "id": id, "self": "https://hw3-almahmoa.wl.r.appspot.com/slips/"+ str(id)}
    elif request.method == 'PATCH':
        content = request.get_json()
        if "number" in content:
            slip_key = client.key(constants.slips, int(id))
            slip = client.get(key=slip_key)
            if slip is None:
                return ({"Error" : "No slip with this slip_id exists"},404)  
            slip.update({"number": content["number"], "current_boat": content["current_boat"]})
            client.put(slip)
            return ( {"number": slip["number"], "current_boat": slip["current_boat"],
                "id": id, "self": "https://hw3-almahmoa.wl.r.appspot.com/slips/"+ str(id)},200)
        return ({"Error" : "The request object is missing at least one of the required attributes"},400)      
    else:
        return 'Method not recognized'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)