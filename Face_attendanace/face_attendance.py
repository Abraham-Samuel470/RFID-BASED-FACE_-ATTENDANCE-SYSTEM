import cv2
import face_recognition
import serial
import mysql.connector
import datetime

# Connect to MySQL
try:
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="attendance_db")
    cursor = conn.cursor()
    print("Connected to MySQL Server!")
except mysql.connector.Error as err:
    print(f"MySQL Connection Error: {err}")

# Connect to Arduino
try:
    arduino = serial.Serial('COM6', 9600, timeout=2)  # Change 'COM6' to your Arduino port
    print("Connected to Arduino! Waiting for RFID...")
except Exception as e:
    print(f"Arduino Connection Error: {e}")

# Known RFID & Face Data
known_faces = {
    "c3d5382": {"name": "M.DHINAKARAN", "roll_no": "22351-EC-030"},
    "80381e85": {"name": "CH. SAI DINESH", "roll_no": "21351-EC-031"},
    "a399362": {"name": "T.MURALI", "roll_no": "22351-EC-059"},
    "83143129": {"name": "SK.NAGULMEERA", "roll_no": "21351-EC-053"},
}

face_encodings = {
    "M.DHINAKARAN": face_recognition.face_encodings(face_recognition.load_image_file("Dhinakaran.jpg"))[0],
    "CH. SAI DINESH": face_recognition.face_encodings(face_recognition.load_image_file("Dinesh.jpg"))[0],
    "T.MURALI": face_recognition.face_encodings(face_recognition.load_image_file("T.Murali.jpg"))[0],
    "SK.NAGULMEERA": face_recognition.face_encodings(face_recognition.load_image_file("Sk.Nagulmeera.jpg"))[0],
}

while True:
    print("\nPlease scan your RFID card...")
    card_id = arduino.readline().decode().strip().lower()

    if not card_id:
        continue  # Ignore empty scans

    print(f"Scanned RFID Card ID: {card_id}")

    if card_id in known_faces:
        person = known_faces[card_id]
        name = person["name"]
        roll_no = person["roll_no"]

        # Open Camera and Keep it Running Until a Face is Detected
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Camera error!")
            continue

        face_detected = False

        while not face_detected:
            ret, frame = cap.read()
            if not ret:
                print("Camera error!")
                break

            # Display the camera feed
            cv2.imshow("Face Recognition - Show Your Face", frame)
            cv2.waitKey(1)  # Allow frame updates

            # Face Recognition
            unknown_encoding = face_recognition.face_encodings(frame)

            if unknown_encoding and face_recognition.compare_faces([face_encodings[name]], unknown_encoding[0])[0]:
                face_detected = True
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Store Attendance in MySQL
                cursor.execute("INSERT INTO Attendance (Name, RollNo, Timestamp) VALUES (%s, %s, %s)", 
                               (name, roll_no, timestamp))
                conn.commit()

                print(f"Attendance recorded for {name} ({roll_no}) at {timestamp}")
                arduino.write(f"{name}, {roll_no}".encode())

            else:
                print("Face does not match!")

        cap.release()
        cv2.destroyAllWindows()  # Close camera window

    else:
        print("Unregistered RFID card detected!")
        arduino.write("Unauthorized".encode())
