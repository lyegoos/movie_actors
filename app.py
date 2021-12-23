from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.mydb


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')


# API 역할을 하는 부분
@app.route('/api/list', methods=['GET'])
def show_stars():
    movie_actor = list(db.mystar.find({}, {'_id': False}).sort('like', -1))
    return jsonify({'movie_actors': movie_actor})


@app.route('/api/like', methods=['POST'])
def like_star():
    name_receive = request.form['name_give']

    target_actor = db.mystar.find_one({'name': name_receive})
    current_like = target_actor['like']
    new_like = current_like + 1

    db.mystar.update_one({'name':name_receive}, {'$set': {'like': new_like}})

    return jsonify({'msg': '+1 했습니다'})


@app.route('/api/delete', methods=['POST'])
def delete_star():
    sample_receive = request.form['sample_give']
    print(sample_receive)
    return jsonify({'msg': 'delete connected!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)