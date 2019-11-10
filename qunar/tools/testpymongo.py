import pymongo
stu1 = {'_id': 1, 'score': 99}
stu2 = {'_id': 2, 'score': 98}
stu3 = {'_id': 1, 'score': 97}
client = pymongo.MongoClient(host='47.97.198.174', port=27017)
db = client.testmongodb
collection = db.stu
try:
    collection.insert_one(stu3)
except pymongo.errors.DuplicateKeyError:
    condition = {'_id': stu3['_id']}
    select_result = collection.find_one(condition)
    if stu3['score'] != select_result['score']:
        new_score = select_result['score'] + stu3['score']
        select_result['score'] = new_score
        update_result = collection.update(condition, select_result)
