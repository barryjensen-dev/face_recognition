# Face Recognition

## Overview

This is a basic face recognition application implemented in Python using the `face_recognition` library. It can identify faces in images and display the recognized names.

## Features

* Recognizes faces in images.
* Compares detected faces against a database of known faces.
* Draws bounding boxes around recognized faces and labels them with names.
* Provides a simple HTML output to display the results.

## Requirements

* Python 3.6 or higher
* Libraries:
    * `face_recognition`
    * `numpy`
    * `Pillow`

## Installation

1.  **Clone the repository (optional):** If you have the code in a Git repository, clone it to your local machine.

2.  **Install the required libraries:**

    ```bash
    pip install -r requirements.txt
    ```

    If you encounter issues, you might need to install `dlib` separately.  Refer to the `face_recognition` installation instructions for your operating system.  You might also need to use `pip3` instead of `pip`.  If you get a "Permission denied" error, try using `sudo pip install` on macOS/Linux or running your command prompt as an administrator on Windows.

## Usage

1.  **Prepare your images:**
    * Place images of known people in the project directory (e.g., `known_person_1.jpg`, `known_person_2.jpg`, etc.).
    * Place the image you want to test in the project directory (e.g., `unknown_person.jpg`).

2.  **Run the Python script:**

    ```bash
    python app.py
    ```

3.  **View the output:**
    * The script will print an HTML page to the console.
    * You can copy this HTML and save it to a file (e.g., `output.html`) and then open it in your web browser.
    * The HTML page will display the image with recognized faces highlighted and labeled.

## Code Overview

###   `app.py`

* **`encode_faces(image_files, names)`**:  Encodes the faces from the provided image files and returns the encodings and names.
* **`recognize_faces(unknown_image_file, known_face_encodings, known_face_names, tolerance=0.6)`**: Recognizes faces in an unknown image by comparing them to known face encodings.  It returns the image with boxes drawn around the recognized faces, the names of the recognized people, and the locations of the faces.
* **`convert_to_jpeg(pil_image)`**: Converts a PIL Image object to a JPEG byte string.
* **`encode_to_base64(image_bytes)`**: Encodes the JPEG byte string to a Base64 string for embedding in HTML.
* **`create_html_response(image_base64, recognized_faces, face_locations)`**:  Generates an HTML page to display the image with the recognition results.
* **`main()`**:  Main function that orchestrates the face recognition process.

##   Example Output

The application generates an HTML page that looks similar to this:

```html
<html>
  <head>
    <title>Face Recognition Output</title>
  </head>
  <body>
    <img src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAAAAAAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAAIAAgDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eH2+o4OEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD3+ooooA//Z" />
    <div>
      <h2>Recognized Faces:</h2>
      <ul>
        <li>Known Person 1 at (100, 150), (200, 250)</li>
        <li>Unknown at (300, 350), (400, 450)</li>
      </ul>
    </div>
  </body>
</html>

Notes
This is a basic implementation and may not be as robust as production-level face recognition systems.

Accuracy can vary depending on image quality, lighting conditions, and pose.

For a real-world application, you would need to implement a database to store known face encodings and a more sophisticated user interface.

Disclaimer
This code is for educational purposes only. Use responsibly and be mindful of privacy considerations when dealing with facial recognition
