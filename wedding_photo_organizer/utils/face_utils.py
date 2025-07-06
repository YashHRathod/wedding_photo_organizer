import os
import cv2
from mtcnn.mtcnn import MTCNN
from deepface import DeepFace
import numpy as np
from sklearn.metrics.pairwise import cosine_distances

def load_and_process_images(folder, threshold=0.8):
    print("🚀 Starting face detection and grouping with similarity threshold...")

    detector = MTCNN()
    embeddings = []
    image_paths = []
    grouped = []

    for fname in os.listdir(folder):
        path = os.path.join(folder, fname)
        print(f"\n📸 Processing: {fname}")
        img = cv2.imread(path)
        if img is None:
            print("❌ Couldn't load image.")
            continue

        faces = detector.detect_faces(img)
        if not faces:
            print("😕 No faces detected.")
            continue

        for face in faces:
            x, y, w, h = face["box"]
            face_crop = img[y:y+h, x:x+w]
            try:
                print("🧠 Computing embedding...")
                embedding_obj = DeepFace.represent(face_crop, model_name="Facenet", enforce_detection=True)[0]
                embedding = np.array(embedding_obj["embedding"])

                # Compare to existing groups
                assigned = False
                for group_id, rep_embedding in enumerate(embeddings):
                    dist = cosine_distances([embedding], [rep_embedding])[0][0]
                    if dist < threshold:
                        grouped[group_id].append(path)
                        assigned = True
                        break

                if not assigned:
                    embeddings.append(embedding)
                    grouped.append([path])
                print("✅ Face assigned to group.")

            except Exception as e:
                print(f"⚠️ Failed to process face: {e}")

    # Save grouped images
    print(f"\n📁 Saving grouped images to output folder...")
    os.makedirs("output/grouped_faces", exist_ok=True)
    for i, group in enumerate(grouped):
        out_dir = f"output/grouped_faces/person_{i}"
        os.makedirs(out_dir, exist_ok=True)
        for img_path in group:
            filename = os.path.basename(img_path)
            cv2.imwrite(os.path.join(out_dir, filename), cv2.imread(img_path))

    print("✅ Grouping complete.")
