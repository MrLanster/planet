import os
import sys
import sqlite3
from face_recogniser import check_image_for_profiles



if __name__ == "__main__":
    # Parse command-line arguments
    uid= sys.argv[1]
    name = sys.argv[2]
    profile_name = sys.argv[3]
    filename = sys.argv[4]
   
    check_image_for_profiles(filename,name,profile_name,filename)
    # Insert into SQLite database

