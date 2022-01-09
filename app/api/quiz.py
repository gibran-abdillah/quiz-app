from codecs import decode
from datetime import datetime
from flask import request, jsonify, session, url_for
from app.api import api_blueprint as api 
from app.modules.decorators import login_required
from app.modules.utils import generate_code, generate_password, json_decoder, ObjectId
from app.db import quiz, db 
from app import csrf_protect
import csv, io, pymongo, json 

@api.route('/quiz/add-quiz', methods=['POST'])
@login_required
def add_quiz():
    data = request.get_json()
    if data:
        code_generated = generate_code()
        data['code'] = code_generated
        data['author'] = session.get('username')
        data['created_at'] = datetime.utcnow()
        quiz.insert_one(data)
        return jsonify(status='success', url=url_for('quiz.quiz_homepage', code=code_generated, _external=True))
        
    return jsonify(status='fail', message='invalid data')

@api.route('/quiz/getQuestion/<code>')
def getquestion(code):
    check = quiz.find_one({'code':code})
    if check:
        data = check['data'] 
        [x.pop('answer') for x in data if x.get('answer')]
        return jsonify(data)
    return jsonify(status='failed')

@api.route('/quiz/view/<code>')
@login_required
def view_quiz(code):
    check = quiz.find_one({'code':code})
    if check and session.get('username') == check['author']:
        return jsonify( 
            json_decoder(check)
        )
    return jsonify(status='fail')

@api.route('/quiz/edit/<code>', methods=['POST'])
@login_required
def edit_quiz(code):
    data = request.get_json()
    check = quiz.find_one({'code':code})

    if check and (session.get('username') == check['author'] or session.get('type') == 1):
        if not data.get('quiz_title'):
            data['quiz_title'] = 'Unkown title'
        quiz.update_one(check,{'$set':data})
        
    return jsonify(status='success', url=url_for("quiz.quiz_homepage", code=code, _external=True))

@api.route('/quiz/nilai/<code>', methods=['POST'])
def nilai(code):
    check = json_decoder(quiz.find_one({'code':code}))
    json_request = request.get_json()
    if check:

        """
        initial data from quest_0, quest_1, etc.
        we just need to take the integer there as the index of the data by replacing the 'quest_' string
        """
        
        list_id = [int(x.replace('quest_','')) for x in json_request]
        list_answer = json_request.values()
        zipper = zip(list_id, list_answer)
        data_check = check['data']
        list_true = [
                    data_check[x]['question'] 
                    for x, y in zipper 
                    if data_check[x].get('answer') \
                        and data_check[x].get('answer').lower() == y
        ]

        perfect_value = 100 
        per_true = perfect_value/len(data_check)
        fix_value = round(len(list_true) * per_true)
        user = json_decoder(db.users.find_one(
                            {'username':session.get('username', None)}))
        data_value = {
                      'quiz_code':code,
                      'score':fix_value, 
                      'id_result':generate_code(14),
                      'do_at':datetime.utcnow()
                    }
        if user:
            data_value['done_by'] = user['username']
            data_value['name'] = user['full_name']   
            data_value['quiz_title'] = check.get('quiz_title')
            db.score.insert_one(json_decoder(data_value))

        return jsonify(status='success', data=data_value)
    return jsonify(status='fail')

@api.route('/quiz/author/<author>/getScores')
def get_scorest(author):
    """"
    function to get scores quiz that done by other users
    """
    if author == 'logged_in':
        if session.get('username'):
            author = {'$exists':True} if session.get('type') == 1 else session.get('username')
        else:
            return jsonify(status='fail', message='not logged in')
    
    # get quiz code that created by author
    get_code = json_decoder(
        [x.get('code') for x in quiz.find({'author':author})]
    )
    if get_code:
        get_data = [y for y in db.score.find({'quiz_code':{'$in':get_code}})]
        return jsonify(status='success', data=json_decoder(get_data))
    return jsonify(status='failed', data=[])

@api.route('/quiz/my-scores')
def my_scores():
    """"
    function to get scores quiz that we have done
    """
    get_data = json_decoder([x for x in db.score.find({'done_by':session.get('username')})])
    return jsonify(status='success', data=get_data)

@api.route('/quiz/search', methods=['POST'])
def quiz_search():
    data = request.get_json()
    
    # check index for search text
    if not quiz.index_information().get('search_text'):
    
        quiz.create_index([
            ('data.question', pymongo.TEXT), 
            ('quiz_title', pymongo.TEXT), 
            ('code', pymongo.TEXT)], name='search_text')
        print('new index created ..')
    
    query_search = {'$text':{'$search':str(data.get('search'))}}
    result_search = json_decoder([x for x in quiz.find(query_search)])
    if result_search:
        return jsonify(status='success', 
                       data=[url_for('quiz.quiz_homepage', code=x.get('code'), _external=True) for x in result_search])

    return jsonify(status='fail', data=result_search)

@api.route('/quiz/uploadCsv', methods=['POST'])
@login_required
def upload_csv():
    files = request.files.get('csv')

    # validate file name 
    if files and files.filename.split('.')[-1] == 'csv':
        
        content = io.StringIO(files.stream.read().decode('utf-8'))
        csv_dict = csv.DictReader(content)
        list_data = []
        for x in csv_dict:

            # validate content for quizes
            if x.get('question') and x.get('a_option',None) \
                and x.get('b_option') and x.get('answer'):
                list_data.append(x)
            else:
                return jsonify(status='failed', message='invalid format question')

        new_data = {'data':list_data, 
                    'code':generate_code(), 
                    'author':session.get('username','unkown'),
                    'created_at':datetime.utcnow(),
                    'quiz_title':request.form.get('quiz_title','Unkown Title')
                    }

        quiz.insert_one(new_data)
        return jsonify(status='success', code=new_data.get('code'))

    elif files and files.filename.split('.')[-1] == 'json':
        content = io.StringIO(files.stream.read().decode('utf-8'))
        try:
            content_json = json.load(content)
            
            # validate format for quiz 
            for data in content_json:
                if not data.get('question') or not data.get('answer')\
                    or not data.get('a_option') or not data.get('c_option'):
                
                    return jsonify(status='failed', message='invalid quiz format')

            new_data = {
                'data':content_json,
                'code':generate_code(),
                'author':session.get('username'),
                'created_at':datetime.utcnow(),
                'quiz_title':request.form.get('quiz_title', 'Unkown Title')
            }

            quiz.insert_one(new_data)
            return jsonify(status='success', code=new_data.get('code'))

        except Exception as e:
            return jsonify(status='failed', message='invalid json format')
        
        
    return jsonify(status='failed', message='files not found/ invalid file')

