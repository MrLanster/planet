import os
from django.conf import settings
from PIL import Image
from .models import User
import face_recognition
import json

def check_image_for_profiles(image_name):
    users=User.objects.all()
    dir=os.getcwd()+"\\main\\static\\"
    known_images = {}
    for i in users:
        known_images[i.name]=dir+i.profile
    # Load the known images (the images of people you want to recognize)
    

    # Encode the known images
    known_encodings = []
    for known_image_file in known_images.values():
        known_image = face_recognition.load_image_file(known_image_file)
        known_encoding = face_recognition.face_encodings(known_image)[0]
        known_encodings.append(known_encoding)

    # Load the test image (the image in which you want to recognize faces)
    test_image = face_recognition.load_image_file(dir+image_name)

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
        if name!="Unknown":
            recognized_faces.append(name)

    # Convert the recognized faces list to JSON
    recognized_json = json.dumps(recognized_faces)
    return recognized_json
