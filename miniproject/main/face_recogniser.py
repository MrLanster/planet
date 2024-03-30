from PIL import Image
import os
import face_recognition
from .models import User

def check_image_for_profiles(image_name):
    image_path = os.path.join(os.path.dirname(__file__), 'static', image_name)

    unknown_image = face_recognition.load_image_file(image_path)

    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

    profiles = User.objects.all()

    matching_profiles = []

    for profile in profiles:
        profile_image_path = os.path.join(os.path.dirname(__file__), 'static', profile.profile)
        profile_image = face_recognition.load_image_file(profile_image_path)
        profile_encoding = face_recognition.face_encodings(profile_image)[0]  

        matches = face_recognition.compare_faces(face_encodings, profile_encoding)

        if True in matches:
            matching_profiles.append(profile.name)  

    return matching_profiles

