from flask import Flask,jsonify,Response,request
app = Flask(__name__)
import json
import requests

service_prefix="http://localhost:8080/music_services_war/webapi/musicresources"

global uuid_x
global user_x
global genre_list

def get_response_object(json_obj):

    resp = Response(json.dumps(json_obj))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods: '] = 'GET, POST, PATCH, PUT, DELETE, OPTIONS'
    resp.headers['Access-Control-Allow-Headers: '] = 'Origin, Content-Type, X-Auth-Token'
    return resp


@app.route('/musixperience/user/<string:uuid>',methods=['GET'])
def get_user_genre(uuid):
    """
    Get user genre based on user id
    :param uuid: User ID
    :return: List of genre(json format)
    """
    response = requests.get(service_prefix+"/usersMongo/"+uuid,headers={"Accept": "application/json"})
    users = json.loads(response.text)
    user = [user for user in users if user['userID'] == uuid]

    i=0
    global uuid_x
    global user_x
    global genre_list
    genre_list = []

    uuid_x=uuid
    user_x=user
    for g in user:
        dict_genre={}
        dict_genre["genre"]=g["genre"]
        dict_genre["rank"]=g["rank"]
        genre_list+=[dict_genre]
        i=i+1
    r = get_response_object(genre_list)
    return r

@app.route('/musixperience/artist/city/<string:city>',methods=['GET'])
def get_artist_city(city):
    """
    Return list of local artist's tracks in a city
    :param city: city name
    :return: list of tracks(json format)
    """
    tracks=[]
    i=0
    for genre in genre_list:
        response = requests.get(service_prefix+"/artistsCityMongo/"+city+"/"+genre["genre"],
                                headers={"Accept": "application/json"})
        artists = json.loads(response.text)
        artist_id = [artist["artistID"] for artist in artists]
        for a in artist_id:
            response = requests.get(service_prefix+"/tracksMongo/"+a,
                                    headers={"Accept": "application/json"})
            t_tracks = json.loads(response.text)
            if len(t_tracks) > 3:
                tracks += t_tracks[:3]
            else:
                tracks += t_tracks

            if i > 2 and len(tracks) > 15:
                break
        i = i + 1
    tracks_to_return = []
    for track in tracks:
        t = {}
        t['trackTitle'] = track.get('trackTitle')
        t['albumName'] = track.get('albumName')
        t['artistName'] = track.get('artistName')
        t['year'] = track.get('year')
        t['Genre'] = track.get('genre')
        t['city'] = track.get('city')
        t['state'] = track.get('state')
        t['location'] = track.get('location')
        tracks_to_return += [t]

    r = get_response_object(tracks_to_return)
    return r


@app.route('/musixperience/artist/state/<string:state>',methods=['GET'])
def get_artist_state(state):
    """
    Return list of local artist's tracks in a state
    :param state: state name
    :return: list of tracks(json format)
    """
    tracks=[]
    i=0
    for genre in genre_list:
        response = requests.get(service_prefix+"/artistsStateMongo/"+state+"/"+genre["genre"],
                                headers={"Accept": "application/json"})
        artists = json.loads(response.text)
        artist_id = [artist["artistID"] for artist in artists]
        for a in artist_id:
            response = requests.get(service_prefix+"/tracksMongo/"+a,
                                    headers={"Accept": "application/json"})
            t_tracks = json.loads(response.text)
            if (len(t_tracks) > 3):
                tracks += t_tracks[:3]
            else:
                tracks += t_tracks
            if (i > 2 and len(tracks)>15):
                break
        i = i + 1
    tracks_to_return = []
    for track in tracks:
        t = {}
        t['trackTitle'] = track.get('trackTitle')
        t['albumName'] = track.get('albumName')
        t['artistName'] = track.get('artistName')
        t['year'] = track.get('year')
        t['Genre'] = track.get('genre')
        t['city'] = track.get('city')
        t['state'] = track.get('state')
        t['location'] = track.get('location')
        tracks_to_return += [t]

    r = get_response_object(tracks_to_return)
    return r


@app.route('/musixperience/event/state/<string:state>',methods=['GET'])
def get_event_state(state):
    """
    Return events of a particular state according to user's genre preference
    :param state: state name
    :return: list of events(json format)
    """
    events=[]
    for genre in genre_list:
        response = requests.get(service_prefix+"/eventsStateMongo/"+state+"/"+genre["genre"],
                                headers={"Accept": "application/json"})
        t_events = json.loads(response.text)
        if(len(t_events)>3):
            events+=t_events[:3]
        else:
            events+=t_events
        if(len(events)>10):
            break
    events_to_return = []
    for event in events:
        e = {}
        e['artistName'] = event.get('artistName')
        e['genre'] = event.get('genre')
        e['eventDate'] = event.get('eventDate')
        e['venueCity'] = event.get('venueCity')
        e['venueState'] = event.get('venueState')
        e['venueName'] = event.get('venueName')
        e['tourName'] = event.get('tourName')
        events_to_return += [e]
    r = get_response_object(events_to_return)
    return r


@app.route('/musixperience/event/city/<string:city>',methods=['GET'])
def get_event_city(city):
    """
    Return events of a particular city according to user's genre preference
    :param state: city name
    :return: list of events(json format)
    """
    events=[]
    for genre in genre_list:
        response = requests.get(service_prefix+"/eventsCityMongo/"+city+"/"+genre["genre"],
                                headers={"Accept": "application/json"})
        t_events = json.loads(response.text)
        if (len(t_events) > 3):
            events += t_events[:3]
        else:
            events += t_events
        if (len(events) > 10):
            break
    events_to_return = []
    for event in events:
        e = {}
        e['artistName'] = event.get('artistName')
        e['genre'] = event.get('genre')
        e['eventDate'] = event.get('eventDate')
        e['venueCity'] = event.get('venueCity')
        e['venueState'] = event.get('venueState')
        e['venueName'] = event.get('venueName')
        e['tourName'] = event.get('tourName')
        events_to_return += [e]
    r = get_response_object(events_to_return)
    return r


@app.route('/musixperience/search/<string:keyword>',methods=['GET'])
def search(keyword):
    """
    Search tracks based on keyword
    :param keyword: keyword
    :return: list of tracks(json format)
    """
    response = requests.get(service_prefix+"/tracksSearchMongo/"+keyword.lower(),headers={"Accept": "application/json"})
    tracks = json.loads(response.text)

    tracks_to_return = []
    for track in tracks:
        t = {}
        t['trackTitle'] = track.get('trackTitle')
        t['albumName'] = track.get('albumName')
        t['artistName'] = track.get('artistName')
        t['year'] = track.get('year')
        t['Genre'] = track.get('genre')
        t['city'] = track.get('city')
        t['state'] = track.get('state')
        t['location'] = track.get('location')
        tracks_to_return += [t]

    r = get_response_object(tracks_to_return)
    return r


@app.route('/musixperience/track',methods=['POST'])
def insert_track():
    """
    Insert track
    :param track: track to be inserted
    :return: track inserted with the Id
    """
    track = request.form.to_dict(flat=True)
    track_str=json.dumps(track)
    track=json.loads(track_str)
    response = requests.post(service_prefix+"/insertTrackMongo",json=track)
    r = get_response_object(response.text)
    return r


if __name__ == '__main__':
    app.run(debug=True, host="localhost", port=8397)