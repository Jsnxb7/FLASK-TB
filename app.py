from flask import Flask, request, jsonify, render_template, send_file, redirect, url_for
from gtts import gTTS
import time
import json
from pymongo import MongoClient
import os, re
import requests
import matplotlib as plt


app = Flask(__name__)

headers = {"Authorization": "Bearer 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"}


@app.route('/', methods=['GET', 'POST'])
def login():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['user_data']
    collection = db['user_data']

    if request.method == 'POST':
        entered_username = request.form['username']
        entered_password = request.form['password']

        # Query the MongoDB collection to find a matching user
        user_data = collection.find_one({
            'username': entered_username,
            'password': entered_password
        })

        if user_data:
            # Extract name and post from user_data
            name = user_data['name']
            post = user_data['post']
            collectionname = user_data['collectionname']

            return redirect(url_for('landing', name=name, post=post, collectionname=collectionname))

        return jsonify({'error': 'Invalid username or password'})

    return render_template('login.html')

@app.route('/landing')
def landing():
    name = request.args.get('name')
    post = request.args.get('post')
    collectionname = request.args.get('collectionname')

    serial_number = get_next_serial_number(collectionname)
    
    return render_template('landing.html', name=name, post=post, collectionname=collectionname, serial_number=serial_number)

@app.route('/Japanese')
def Japanese():
    name = request.args.get('name')
    post = request.args.get('post')
    collectionname = request.args.get('collectionname')
    
    return render_template('1jp.html', name=name, post=post, collectionname=collectionname)

@app.route('/Hindi')
def Hindi():
    name = request.args.get('name')
    post = request.args.get('post')
    collectionname = request.args.get('collectionname')

    return render_template('1hi.html', name=name, post=post, collectionname=collectionname)
     
@app.route('/signup1', methods=['POST'])
def update():

    client = MongoClient('mongodb://localhost:27017/')  
    db = client['user_data']
    user_collection = db['user_data'] 

    # Extract user data from the form
    name = request.form['name']
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    post = request.form['post']
    
    # Create a new collection for the user based on the username
    user_specific_collection_name = f"user_{username}"
    user_specific_collection = db[user_specific_collection_name]
    
        # Data to insert into the user_data collection
    user_data = {
        'name': name,
        'username': username,
        'email': email,
        'password': password,
        'post': post,
        'collectionname': user_specific_collection_name
    }
    
    # Insert the new user data into the user_data collection
    user_collection.insert_one(user_data)
    
    # Optionally, you can insert initial data into the user's specific collection
    initial_data = {
        'name': name,
        'post': post,
        'email': email,
        'total': 3000
    }
    user_specific_collection.insert_one(initial_data)
    
    return redirect(url_for('login'))


@app.route('/signup')
def sign_up():
    return render_template('signup.html')

def get_next_serial_number(collectionname):
    
    client = MongoClient('mongodb://localhost:27017/')
    db = client['user_data']
    collection = db[collectionname]

    try:
        # Get the count of documents in the MongoDB collection
        data_count = collection.count_documents({})
        return data_count + 1
    except Exception as e:
        print(f"An error occurred: {e}")
        return 1
    

def translatejp(text):
    API_URLS = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-tatoeba-en-ja"
    payload = {"inputs": text}
    response = requests.post(API_URLS, headers=headers, json=payload)
    translation = response.json()
    return translation[0]['translation_text']
    
@app.route('/translatjp', methods=['POST'])
def translatjp():
    data = request.get_json()
    name = data.get('name')
    post = data.get('post')
    text = data.get('text')
    
    if not name or not post:
        return jsonify({'error': 'Name and post are required'}), 410
    
    client = MongoClient('mongodb://localhost:27017/')
    db = client['user_data']
    
    # Retrieve user data to get collectionname
    user_data = db['user_data'].find_one({'name': name, 'post': post})
    if not user_data or 'collectionname' not in user_data:
        return jsonify({'error': 'User data not found or collection name missing'}), 404
    
    collectionname = user_data['collectionname']
    collection = db[collectionname]

    twt = request.get_json()
    tex = twt.get('text')
    
    # Translate text using the Hugging Face model
    translation = translatejp(tex)
    
    # Tokenize the original text
    token_count = len(tex) * 3
    
    # Get the next serial number
    serial_number = get_next_serial_number(collectionname)
    
    output_data = {
        "serial_number": serial_number,
        "original_text": tex,
        "translated_text": translation,
        "token_count": token_count,
        "language": "Japanese"
    }
    
    try:
        # Insert the new translation data into the MongoDB collection
        collection.insert_one(output_data)
        print("Translation data saved successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Calculate the total token count
    total_token_count = 0
    try:
        all_documents = collection.find({})
        for doc in all_documents:
            total_token_count += doc.get('token_count', 0)
    except Exception as e:
        print(f"An error occurred while calculating total token count: {e}")
    
    print(f"Current token count: {token_count}")
    print(f"Total token count: {total_token_count}")
    print(translation)

    return jsonify({"serial_number": serial_number, "translated_text": translation, "token_count": token_count, "total_token_count": total_token_count}), 200

def translatehi(text):
    API_URLS ="https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-hi"
    payload = {"inputs": text}
    response = requests.post(API_URLS, headers=headers, json=payload)
    translation = response.json()
    return translation[0]['translation_text']

@app.route('/translathi', methods=['POST'])

def translathi():
    data = request.get_json()
    name = data.get('name')
    post = data.get('post')
    text = data.get('text')
    
    if not name or not post:
        return jsonify({'error': 'Name and post are required'}), 510
    
    client = MongoClient('mongodb://localhost:27017/')
    db = client['user_data']
    
    # Retrieve user data to get collectionname
    user_data = db['user_data'].find_one({'name': name, 'post': post})
    if not user_data or 'collectionname' not in user_data:
        return jsonify({'error': 'User data not found or collection name missing'}), 504
    
    collectionname = user_data['collectionname']
    collection = db[collectionname]

    twt = request.get_json()
    tex = twt.get('text')
    
    # Translate text using the Hugging Face model
    translation = translatehi(tex)
    
    # Tokenize the original text
    token_count = len(tex) * 3
    
    # Get the next serial number
    serial_number = get_next_serial_number(collectionname)
    
    output_data = {
        "serial_number": serial_number,
        "original_text": tex,
        "translated_text": translation,
        "token_count": token_count,
        "language": "Hindi"
    }
    
    try:
        # Insert the new translation data into the MongoDB collection
        collection.insert_one(output_data)
        print("Translation data saved successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Calculate the total token count
    total_token_count = 0
    try:
        all_documents = collection.find({})
        for doc in all_documents:
            total_token_count += doc.get('token_count', 0)
    except Exception as e:
        print(f"An error occurred while calculating total token count: {e}")
    
    print(f"Current token count: {token_count}")
    print(f"Total token count: {total_token_count}")
    print(translation)

    return jsonify({"serial_number": serial_number, "translated_text": translation, "token_count": token_count, "total_token_count": total_token_count}), 200

@app.route('/speechjp', methods=['POST'])
def speechjp():

    data = request.get_json()
    name = data.get('name')
    post = data.get('post')
    serial_number = data.get('serial_number')

    if not name or not post or not serial_number:
        return jsonify({'error': 'Name, post, and serial number are required'}), 511

    client = MongoClient('mongodb://localhost:27017/')
    db = client['user_data']

    # Retrieve the collectionname from the user_data collection
    user_data = db['user_data'].find_one({'name': name, 'post': post})
    if not user_data or 'collectionname' not in user_data:
        return jsonify({'error': 'User data not found or collection name missing'}), 514

    collectionname = user_data['collectionname']
    collection = db[collectionname]

    print(serial_number)

    # Find the entry with the specified serial number in MongoDB
    entry = collection.find_one({"serial_number": serial_number})
    if entry is None:
        return jsonify({"error": f"Translation with serial number {serial_number} not found"}), 704

    # Use the translated text for text-to-speech
    text_to_speech_text = entry["translated_text"]

    # Generate a unique filename using a timestamp
    timestamp = str(int(time.time()))
    audio_filename = f"static/{timestamp}.mp3"

    # Convert text to speech and save with the unique filename
    tts = gTTS(text=text_to_speech_text, lang="ja")
    tts.save(audio_filename)
    print("Audio filename:", audio_filename)

    # Create the audio URL with the unique filename
    audio_url = f'/{audio_filename}'

    return jsonify(audio_url=audio_url), 200

@app.route('/speechhi', methods=['POST'])
def speechhi():

    data = request.get_json()
    name = data.get('name')
    post = data.get('post')
    serial_number = data.get('serial_number')

    if not name or not post or not serial_number:
        return jsonify({'error': 'Name, post, and serial number are required'}), 411

    client = MongoClient('mongodb://localhost:27017/')
    db = client['user_data']

    # Retrieve the collectionname from the user_data collection
    user_data = db['user_data'].find_one({'name': name, 'post': post})
    if not user_data or 'collectionname' not in user_data:
        return jsonify({'error': 'User data not found or collection name missing'}), 414

    collectionname = user_data['collectionname']
    collection = db[collectionname]

    print(serial_number)

    # Find the entry with the specified serial number in MongoDB
    entry = collection.find_one({"serial_number": serial_number})
    if entry is None:
        return jsonify({"error": f"Translation with serial number {serial_number} not found"}), 804

    # Use the translated text for text-to-speech
    text_to_speech_text = entry["translated_text"]

    # Generate a unique filename using a timestamp
    timestamp = str(int(time.time()))
    audio_filename = f"static/{timestamp}.mp3"

    # Convert text to speech and save with the unique filename
    tts = gTTS(text=text_to_speech_text, lang="hi")
    tts.save(audio_filename)
    print("Audio filename:", audio_filename)

    # Create the audio URL with the unique filename
    audio_url = f'/{audio_filename}'

    return jsonify(audio_url=audio_url), 200


@app.route('/output/<filename>')
def serve_audio(filename):
    path_to_file = f"static/{filename}"
    print(path_to_file)

    return send_file(
        path_to_file,
        mimetype="audio/mp3",
        as_attachment=True,
        attachment_filename=filename
    )

@app.route('/profile')
def profile():
    name = request.args.get('name')
    post = request.args.get('post')

    return render_template('profile.html', name=name, post=post)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
