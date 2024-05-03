import os
from PIL import Image
import sqlite3
import face_recognition
import json


# Function to update the database
def update_database(uid, name, profile_name, filename, tags):
    # Connect to SQLite database
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    # Update the record in the main_uploads table based on the uid
    cursor.execute("UPDATE main_uploads SET tags=? WHERE uid=?", 
                   (tags, uid))
    conn.commit()
    conn.close()

    
def starter(name, profile_name, filename, tags):
    # Connect to SQLite database
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    # Insert a new record into the Uploads table
    cursor.execute("INSERT INTO main_uploads (name, profile_name, filename, tags) VALUES (?, ?, ?, ?)", (name, profile_name, filename, tags))
    conn.commit()
    uid = cursor.lastrowid
    conn.close()
    return uid


def check_image_for_profiles(image_name,name,profile_name,filename):
    uid=starter(name,profile_name,filename,"[Processing Image Please Wait...]")
    # Perform image recognition
    print("starting..")
    # Connect to SQLite database
    # Get the current working directory
    current_directory = os.getcwd()

    # Get the parent directory
    # Move one level up
    os.chdir("..")
    os.chdir("miniproject")
    print(os.getcwd())
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    # Fetch user information from the database
    cursor.execute("SELECT name, profile FROM main_user")
    users = cursor.fetchall()

    # Construct the directory path
    dir = os.path.join(os.getcwd(), "main", "static")

    known_images = {}
    known_encodings = []

    # Encode the known images
    for user_name, profile_name in users:
        profile_path = os.path.join(dir, profile_name)
        if os.path.exists(profile_path):
            known_image = face_recognition.load_image_file(profile_path)
            face_encodings = face_recognition.face_encodings(known_image)
            if face_encodings:
                known_encoding = face_encodings[0]  # Take the first face encoding if found
                known_encodings.append(known_encoding)
                known_images[user_name] = profile_path
            else:
                print(f"No face found in profile image for user: {user_name}")
                continue
        else:
            print(f"Profile image not found for user: {user_name}")
            continue

    # Load the test image
    test_image_path = os.path.join(dir, image_name)
    test_image = face_recognition.load_image_file(test_image_path)

    # Find all the face locations and encodings in the test image
    face_locations = face_recognition.face_locations(test_image, model="cnn")
    face_encodings = face_recognition.face_encodings(test_image, face_locations)

    # Create a list to store the recognized people with their locations
    recognized_faces = []

    # Compare each face encoding found in the test image with the known encodings
    for face_encoding, face_location in zip(face_encodings, face_locations):
        # Compare the face encoding with the known encodings
        matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)

        name = "Unknown"
        for i, match in enumerate(matches):
            if match:
                name = list(known_images.keys())[i]
                break
        if name != "Unknown":
            recognized_faces.append(name)

    # Convert the recognized faces list to JSON
    recognized_json = json.dumps(recognized_faces)

    # Close the database connection
    conn.close()

    update_database(uid,name, profile_name, filename, recognized_json)
    print("completed!")


