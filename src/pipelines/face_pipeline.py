import streamlit as st

import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC


from src.database.db import get_all_students

@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()

    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
        )

    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, facerec

def get_face_embeddings(image_np):
    detector, sp, facerec = load_dlib_models()

    faces = detector(image_np, 1)

    encodings = []

    for face in faces:
        shape = sp(image_np, face)
        face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1) # 128 embeddings 
        encodings.append(np.array(face_descriptor))

    return encodings


@st.cache_resource
def get_trained_model():
    student_db = get_all_students()

    if not student_db:
        return None

    X = []
    y = []

    for student in student_db:
        embedding = student.get("face_embedding")

        if embedding is None:
            continue

        X.append(np.array(embedding, dtype=np.float64))
        y.append(student["student_id"])

    if len(X) == 0:
        return None

    clf = SVC(
        kernel="linear",
        probability=True,
        class_weight="balanced"
    )

    # try:
    #     clf.fit(X, y)
    # except ValueError as e:
    #     st.error(f"Model training failed: {e}")
    #     return None

    return {
        # "classifier": clf,
        "X": X,
        "y": y
    }
    

def train_classifier():
    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)

def predict_attendance(class_image_np):
    encodings = get_face_embeddings(class_image_np)

    detected_students = {}

    model_data = get_trained_model()

    if not model_data:
        return detected_students, [], len(encodings)

    X_train = model_data["X"]
    y_train = model_data["y"]

    all_students = sorted(list(set(y_train)))

    RECOGNITION_THRESHOLD = 0.45

    for encoding in encodings:

        best_distance = float("inf")
        best_student_id = None

        for train_embedding, student_id in zip(X_train, y_train):

            distance = np.linalg.norm(
                np.array(encoding) - np.array(train_embedding)
            )

            if distance < best_distance:
                best_distance = distance
                best_student_id = student_id

        # Debug (remove after testing)
        print(
            f"Best Match -> Student: {best_student_id}, Distance: {best_distance:.4f}"
        )

        if best_distance <= RECOGNITION_THRESHOLD:
            detected_students[int(best_student_id)] = True

    return detected_students, all_students, len(encodings)