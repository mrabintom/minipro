import os
import cv2
import numpy as np
import face_recognition
from datetime import datetime, date
from app import app
from backend.models import db, Student, Attendance

# --- Load all students and their photos ---
known_face_encodings = []
known_students = []

with app.app_context():
    students = Student.query.all()
    for student in students:
        if student.photo:
            photo_path = os.path.join("static/images", student.photo)
            if os.path.exists(photo_path):
                image = face_recognition.load_image_file(photo_path)
                encodings = face_recognition.face_encodings(image)
                if encodings:
                    known_face_encodings.append(encodings[0])
                    known_students.append(student)
                    print(f"✅ Loaded encoding for {student.student_id} {student.name}")
                else:
                    print(f"⚠️ No face found in {student.photo}")
            else:
                print(f"⚠️ Photo file not found: {photo_path}")

# --- Open webcam (keep it always on) ---
cap = cv2.VideoCapture(0)

with app.app_context():
    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Failed to capture frame.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect faces
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

            student = None
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    student = known_students[best_match_index]

            if student:
                # ✅ Student recognized → mark attendance
                today = date.today()
                now = datetime.now().time()

                try:
                    existing = Attendance.query.filter_by(student_id=student.student_id, date=today).first()
                    if not existing:
                        new_record = Attendance(
                            student_id=student.student_id,
                            student_name=student.name,
                            date=today,
                            time=now
                        )
                        db.session.add(new_record)
                        db.session.commit()
                        print(f"✅ Attendance marked for {student.name}")
                    else:
                        print(f"ℹ️ Already marked for {student.name}")
                except Exception as e:
                    db.session.rollback()  # prevent session crash
                    print(f"❌ DB Insert Failed: {e}")

                label = f"{student.student_id} {student.name}"
            else:
                # ❌ Unknown face → don’t insert
                label = "Unknown"
                print("❌ Unknown face detected")

            # Draw rectangle and label
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, label, (left, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow("Attendance System", frame)

        # Exit only when pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("👋 Exiting system.")
            break

cap.release()
cv2.destroyAllWindows()
