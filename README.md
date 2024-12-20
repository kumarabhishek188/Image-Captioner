# Real-Time AI Image Captioner

This project, **Real-Time AI Image Captioner**, is a Django-based web application that uses a pre-trained AI model to generate captions for uploaded images in real time. It also provides features such as speech synthesis for captions, tags, and recommendations.

## Features

- **Image Captioning**: Upload an image and generate captions using AI.
- **Speech Synthesis**: Listen to the generated captions.
- **Tags and Recommendations**: Get relevant tags and suggestions based on the image content.

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Django (Python)
- **Database**: SQLite (default, can be replaced with PostgreSQL or MySQL)
- **AI Model**: Pre-trained image captioning model using Keras
- **Styling**: Tailwind CSS

## Requirements

- Python 3.8 or higher
- pip
- Git
- A modern web browser

## Installation

Follow these steps to set up and run the application locally:

### 1. Clone the Repository

```bash
git clone https://github.com/kumarabhishek188/Real-Time-AI-Image-Captioner.git
cd Real-Time-AI-Image-Captioner
```

### 2. Set Up a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Required Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up the Database

Run the following command to apply migrations and set up the database:

```bash
python manage.py migrate
```

### 5. Download the Image Captioning Model

Download and set up the pre-trained image captioning model. Replace the example URL with the actual download instructions for your model:

```bash
wget https://github.com/kumarabhishek188/Real-Time-AI-Image-Captioner-model/releases/download/v1.0/model.pth
```

Ensure the model file is placed in the correct directory as expected by the application.

### 6. Start the Django Development Server

```bash
python manage.py runserver
```

You can now access the application at [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Usage

1. Visit the homepage of the application.
2. Upload an image using the provided form.
3. Click on the **Generate Caption** button.
4. The generated caption will be displayed below the image. Additional features like speech synthesis, tags, and recommendations will also be available.

## Project Structure

```
image-captioner/
├── manage.py
├── image_captioner/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
├── captions/
│   ├── models.py
│   ├── views.py
│   ├── templates/
│   └── ...
├── static/
│   ├── css/
│   ├── js/
│   └── ...
└── requirements.txt
```

## Dependencies

All dependencies are listed in `requirements.txt`. Install them using the following command:

```bash
pip install -r requirements.txt
```

## Contributing

Contributions are welcome! Please fork the repository and create a pull request for any changes.

## Contact

- **LinkedIn**: [Abhishek Kumar](https://www.linkedin.com/in/abhishek-kumar-92157823a/)
- **Email**: [abhishekkumarada12@gmail.com](mailto:abhishekkumarada12@gmail.com)

---

**Happy Coding!** 🎉
