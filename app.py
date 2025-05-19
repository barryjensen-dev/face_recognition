import face_recognition
import numpy as np
from PIL import Image, ImageDraw
import os
import io
import base64

def encode_faces(image_files, names):
    """
    Encodes faces from a list of image files.

    Args:
        image_files (list): List of paths to image files.
        names (list): List of corresponding names for the faces in the images.

    Returns:
        tuple: A tuple containing:
            - known_face_encodings (list): List of face encodings.
            - known_face_names (list): List of corresponding names.
    """
    known_face_encodings = []
    known_face_names = []

    for image_file, name in zip(image_files, names):
        try:
            image = face_recognition.load_image_file(image_file)
            encodings = face_recognition.face_encodings(image)
            
            if len(encodings) > 0:
                encoding = encodings[0]  # Use the first encoding if multiple faces are detected
                known_face_encodings.append(encoding)
                known_face_names.append(name)
            else:
                print(f"No face detected in {image_file}. Skipping.") #handle no face
        except Exception as e:
            print(f"Error processing {image_file}: {e}") # handle exceptions

    return known_face_encodings, known_face_names

def recognize_faces(unknown_image_file, known_face_encodings, known_face_names, tolerance=0.6):
    """
    Recognizes faces in an unknown image given a set of known face encodings.

    Args:
        unknown_image_file (str): Path to the image file with unknown faces.
        known_face_encodings (list): List of known face encodings.
        known_face_names (list): List of corresponding names.
        tolerance (float, optional): How much distance between faces to consider it a match. Lower is more strict.

    Returns:
        tuple: A tuple containing:
            -pil_image
            -recognized_faces (list): List of names of recognized people.
            -face_locations: List of face locations
    """
    recognized_faces = []
    face_locations = []
    pil_image = None

    try:
        unknown_image = face_recognition.load_image_file(unknown_image_file)
        face_locations = face_recognition.face_locations(unknown_image)  # Use the updated variable name
        face_encodings = face_recognition.face_encodings(unknown_image, face_locations) # Pass face_locations

        pil_image = Image.fromarray(unknown_image) #moved here
        draw = ImageDraw.Draw(pil_image)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            name = "Unknown"
            if known_face_encodings: #check if known faces exist
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=tolerance)
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
            recognized_faces.append(name)

            # Draw a box around the face
            draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
            # Draw a label below the face
            text_width, text_height = draw.textsize(name)
            draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
            draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255))
    except Exception as e:
        print(f"Error processing unknown image: {e}")
        return None, [], []  # Return None and empty lists in case of error

    return pil_image, recognized_faces, face_locations

def convert_to_jpeg(pil_image):
    """
    Converts a PIL Image to a JPEG byte string.

    Args:
        pil_image (PIL.Image.Image): The PIL Image object.

    Returns:
        bytes: The image as a JPEG byte string, or None on error.
    """
    if pil_image is None:
        return None
    try:
        img_byte_arr = io.BytesIO()
        pil_image.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        return img_byte_arr
    except Exception as e:
        print(f"Error converting to JPEG: {e}")
        return None

def encode_to_base64(image_bytes):
    """
    Encodes an image byte string to a Base64 string.

    Args:
        image_bytes (bytes): The image as a byte string.

    Returns:
        str: The Base64 encoded string, or None on error.
    """
    if image_bytes is None:
        return None
    try:
        base64_encoded = base64.b64encode(image_bytes).decode('utf-8')
        return base64_encoded
    except Exception as e:
        print(f"Error encoding to Base64: {e}")
        return None

def create_html_response(image_base64=None, recognized_faces=None, face_locations=None):
    """
    Creates an HTML response to display the recognized faces.

    Args:
        image_base64 (str, optional): The Base64 encoded image string.
        recognized_faces (list, optional): List of names of recognized people.
        face_locations (list, optional): List of face locations.

    Returns:
        str: An HTML string.
    """
    html_content = "<html><head><title>Face Recognition Output</title></head><body>"
    if image_base64:
        html_content += f"<img src='data:image/jpeg;base64,{image_base64}'/>"
    else:
        html_content += "<p>No image to display.</p>"

    if recognized_faces and face_locations:
        html_content += "<div><h2>Recognized Faces:</h2><ul>"
        for i, (name, (top, right, bottom, left)) in enumerate(zip(recognized_faces, face_locations)):
            html_content += f"<li>{name} at ({left}, {top}), ({right}, {bottom})</li>"
        html_content += "</ul></div>"
    elif recognized_faces:
        html_content += "<div><h2>Recognized Faces:</h2><ul>"
        for name in recognized_faces:
            html_content += f"<li>{name}</li>"
        html_content += "</ul></div>"
    else:
        html_content += "<p>No faces recognized.</p>"
    html_content += "</body></html>"
    return html_content

def main():
    """
    Main function to run the face recognition process.
    """
    # 1. Encode known faces (from image files)
    known_image_files = ["known_person_1.jpg", "known_person_2.jpg", "known_person_3.jpg"] #add known person 3
    known_names = ["Known Person 1", "Known Person 2", "Known Person 3"]
    known_face_encodings, known_face_names = encode_faces(known_image_files, known_names)

    # 2. Load and recognize faces in an unknown image
    unknown_image_file = "unknown_person.jpg"
    pil_image, recognized_faces, face_locations = recognize_faces(unknown_image_file, known_face_encodings, known_face_names)

    # 3. Prepare the result
    image_bytes = convert_to_jpeg(pil_image)
    image_base64 = encode_to_base64(image_bytes) if image_bytes else None
    html_response = create_html_response(image_base64, recognized_faces, face_locations)

    # 4. Print the HTML (or save to a file)
    print(html_response)
    # with open("face_recognition_output.html", "w") as f: #save
    #     f.write(html_response)

if __name__ == "__main__":
    # Create dummy image files if they don't exist
    for img_file in ["known_person_1.jpg", "known_person_2.jpg", "known_person_3.jpg", "unknown_person.jpg"]:
        if not os.path.exists(img_file):
            # Create a blank white image
            img = Image.new('RGB', (100, 100), color = 'white')
            img.save(img_file)
            print(f"Created dummy image: {img_file}")
