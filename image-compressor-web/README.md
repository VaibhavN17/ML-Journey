# Image Compressor Web Application

This project is a web application that allows users to upload images and compress them to a specified size using Python and Flask. The application utilizes the Pillow library for image processing.

## Project Structure

```
image-compressor-web
├── src
│   ├── app.py               # Main entry point of the web application
│   ├── compressor.py         # Contains image compression logic
│   └── templates
│       └── index.html       # HTML template for the web page
├── requirements.txt          # Lists project dependencies
└── README.md                 # Documentation for the project
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd image-compressor-web
   ```

2. **Create a virtual environment (optional but recommended):**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies:**
   ```
   pip install -r requirements.txt
   ```

## Usage

1. **Run the application:**
   ```
   python src/app.py
   ```

2. **Open your web browser and navigate to:**
   ```
   http://127.0.0.1:5000
   ```

3. **Upload an image:**
   Use the provided form to select an image file and submit it for compression. The application will process the image and provide a download link for the compressed file.

## Dependencies

- Flask
- Pillow

## License

This project is licensed under the MIT License. See the LICENSE file for details.