from utils.face_utils import load_and_process_images

if __name__ == "__main__":
    folder_path = "data/raw_photos"
    load_and_process_images(folder_path)
    print("✅ Photos have been grouped into folders by person.") 