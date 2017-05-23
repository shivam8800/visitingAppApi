from flask import Flask,request,abort,jsonify, make_response
from flask_httpauth import HTTPBasicAuth
import time
auth =HTTPBasicAuth()
app =Flask(__name__)

app.config.update({
    "DEBUG": True
})

users =[
    {'username': 'shivam', 'password': 'jaan', 'age': 26, 'city': 'sarita vihar', 'bio': "hi i am shivam and i am learning programming at navgurukul"},
    {'username': 'jaan', 'password': 'shivam', 'age': 22, 'city': 'gurgaon', 'bio': "hi i am jann and i am jaan of my shivam"}
]

places =[
    {'username': 'shivam','placeName': 'mandaula', 'addedOn': time.strftime("%d/%m/%Y"), 'details': 'this is awesome place for everyone', 'likes': 200, 'id': 1},
    {'username': 'jaan','placeName': 'saket', 'addedOn': time.strftime("%d/%m/%Y"), 'details': 'this is awesome place for every couple', 'likes': 2300, 'id': 2},
    {'username': 'shivam','placeName': 'lal kila', 'addedOn': time.strftime("%d/%m/%Y"), 'details': 'this is place for incient kings', 'likes': 210, 'id': 3},
    {'username': 'jaan','placeName': 'five sence', 'addedOn': time.strftime("%d/%m/%Y"), 'details': 'this is awesome place for every couple', 'likes': 2300, 'id': 2}
]

comments =[
    {'username': 'jaan','id': 2, 'text': "i love this place and i am owner of the place", 'addedOn': time.strftime("%d/%m/%Y")},
    {'username': 'shivam','id': 3, 'text': "this is famous place since 1990", 'addedOn': time.strftime("%d/%m/%Y")},
    {'username': 'shivam','id': 2, 'text': "kdsjfjkljsklfjsdklfj", 'addedOn': time.strftime("%d/%m/%Y")}
]

@auth.get_password
def get_password(username):
    user =[user for user in users if username ==user['username']]
    if len(user) == 0:
        abort(400)
    return user[0]['password']

@auth.error_handler
def unauthorzed():
    return make_response(jsonify({'error': 'unauthorized access'}), 401)

@app.route('/get/user/current_user_place', methods=['GET'])
@auth.login_required
def get_current_user_place():
    search = request.args.get('search')
    new_list = []
    for place in places:
        if search in place['placeName']:
            new_list.append(place)
    if len(new_list) == 0:
        new_list.append({'typeerror':'sorry, your search word does not exist in our server'})
    return jsonify({'user_place': new_list}), 201

@app.route('/get/user/current_user_one_place/<int:place_id>', methods=['GET'])
@auth.login_required
def get_current_user_particular_place(place_id):
    place =[place for place in places if auth.username() == place['username']]
    one_place =[one_place for one_place in place if place_id ==one_place['id']]
    return jsonify({'user_place': one_place}), 201

@app.route('/get/user/comment_from_id/<int:comment_id>', methods=['GET'])
@auth.login_required
def get_comment_from_id(comment_id):
    user_comment =[user_comment for user_comment in comments if auth.username() ==user_comment['username']]
    one_comment =[one_comment for one_comment in user_comment if comment_id ==one_comment['id']]
    return jsonify({'user_place': one_comment}), 201

@app.route('/put/user/update_place/<int:place_id>', methods=['PUT'])
@auth.login_required
def update_place_from_id(place_id):
    all_user_place =[all_user_place for all_user_place in places if auth.username() ==all_user_place['username']]
    id_place =[id_place for id_place in all_user_place if place_id ==id_place['id']]
    if len(id_place) == 0:
       abort(404)
    if not request.json:
       abort(400)
    if 'details' in request.json and type(request.json['details']) is not unicode:
       abort(400)
    if 'likes' in request.json and type(request.json['likes']) is not unicode:
       abort(400)
    id_place[0]['details'] = request.json.get('details', id_place[0]['details'])
    id_place[0]['likes'] =request.json.get('likes', id_place[0]['likes'])

    return jsonify({'update_place': id_place[0]})

@app.route('/get/user/current_user_details', methods=['GET'])
@auth.login_required
def get_current_user_details():
    user =[user for user in users if auth.username() == user['username']]
    return jsonify({'user_place': user}), 201


@app.route('/post/user/signup', methods=['POST'])
@auth.login_required
def creat_user():
    if not request.json and     not 'user' in request.json:
        abort(400)
    user={
        'username': request.json['username'],
        'password': request.json['password'],
        'age': request.json['age'],
        'city': request.json['city'],
        'bio': request.json['bio']
    }
    users.append(user)
    return jsonify({'user':users}), 201

@app.route('/post/user/addplace', methods=['POST'])
@auth.login_required
def new_place():
    if not request.json and not 'placeName' in request.json:
        abort(400)
    place ={
        'placeName': request.json['placeName'],
        'addedOne': time.strftime("%d/%m/%Y"),
        'details': request.json['details'],
        'likes': request.json['likes'],
        'id': places[-1]['id'] +1,
        'username': auth.username()
    }
    places.append(place)
    return jsonify({'places': places}), 201

@app.route('/post/user/add_comment/<int:comment_id>', methods=['POST'])
@auth.login_required
def add_comment(comment_id):
    if not request.json and not 'text' in request.json:
        abort(400)
    comment =[comment for comment in comments if comment_id ==comment['id']]
    particular_user_comment =[particular_user_comment for particular_user_comment in comment if auth.username() ==particular_user_comment['username']]
    particular_user_comment ={
        'text': request.json['text'],
        'username': auth.username(),
        'id': comment['id'],
        'addedOn': time.strftime("%d/%m/%Y")
    }
    comments.append(particular_user_comment)
    return jsonify({'comment': particular_user_comment})


if __name__ =="__main__":
    app.run()