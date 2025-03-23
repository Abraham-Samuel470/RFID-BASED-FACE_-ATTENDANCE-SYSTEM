import cv2
import face_recognition
import serial
import mysql.connector
import time

# Connect to MySQL
try:
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="attendance_db")
    cursor = conn.cursor()
    print("Connected to MySQL Database")
except mysql.connector.Error as e:
    print(f"MySQL Connection Error: {e}")
    exit()

# Connect to Arduino
try:
    arduino = serial.Serial('COM6', 9600, timeout=2)  # Change 'COM3' to your Arduino port
    time.sleep(2)  # Give time for connection
    print(" Connected to Arduino")
except serial.SerialException as e:
    print(f" Serial Connection Error: {e}")
    exit()

# Load known faces
known_faces = {
    "c3d5382": "Abraham",
    "80381e85": "Sampath"
}
face_encodings = {
    "Abraham": face_recognition.face_encodings(face_recognition.load_image_file("abraham.jpg"))[0],
    "Sampath": face_recognition.face_encodings(face_recognition.load_image_file("Sampath.jpg"))[0]
}

while True:
    if arduino.in_waiting > 0:
        card_id = arduino.readline().decode().strip()
        print(f"RFID Card Scanned: {card_id}")

        if card_id in known_faces:
            name = known_faces[card_id]
            print(f" Card belongs to {name}. Opening camera...")

            # Open Camera
            cap = cv2.VideoCapture(0)
            time.sleep(3)  # Give time to adjust
            ret, frame = cap.read()
            cap.release()

            if not ret:
                print(" Failed to capture image")
                arduino.write(b"Unauthorized\n")
                continue

            # Process image
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            unknown_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            if not unknown_encodings:
                print(" No face detected")
                arduino.write(b"Unauthorized\n")
                continue

            # Compare faces
            best_match = None
            lowest_distance = 0.6  # Lower means better match

            for unknown_encoding in unknown_encodings:
                face_distance = face_recognition.face_distance([face_encodings[name]], unknown_encoding)
                if face_distance[0] < lowest_distance:
                    best_match = name
                    lowest_distance = face_distance[0]

            if best_match:
                print(f" Face match successful for {best_match}")

                # Insert attendance into MySQL
                try:
                    cursor.execute("INSERT INTO Attendance (Name, RFID) VALUES (%s, %s)", (best_match, card_id))
                    conn.commit()
                    print(" Attendance logged in MySQL")
                except mysql.connector.Error as e:
                    print(f" MySQL Insert Error: {e}")

                arduino.write(f"{best_match}\n".encode())
            else:
                print(" Face mismatch! Access Denied.")
                arduino.write(b"Unauthorized\n")
        else:
            print(" Unknown RFID card!")
            arduino.write(b"Unauthorized\n")
