# TestingFolder

## Overview

This repository is a collection of Python, Machine Learning, Deep Learning, API development, Flask, FastAPI, MongoDB, and Data Science practice projects.

The repository contains multiple experiments, notebooks, datasets, image processing examples, sorting algorithms, CNN models, authentication APIs, and beginner-to-intermediate backend development projects.

This project works mainly as a learning repository where different technologies and concepts are tested and implemented.

---

# Technologies Used

* Python
* Jupyter Notebook
* NumPy
* Pandas
* Matplotlib
* OpenCV
* TensorFlow / Keras
* CNN (Convolutional Neural Networks)
* Flask
* FastAPI
* MongoDB
* HTML
* Machine Learning
* Deep Learning

---

# Repository Structure

```bash
TestingFolder-main/
│
├── CNN.ipynb
├── facedetection.ipynb
├── numbers_cnn.ipynb
├── type_cnn.ipynb
├── recommendation.ipynb
├── dataset.ipynb
├── gradient.ipynb
├── linkedlist.ipynb
├── cv2.ipynb
├── finger.ipynb
├── backpro.ipynb
├── task_claud.ipynb
│
├── bubble_sort.py
├── bubble_sort2.py
├── insertion_sort.py
├── demo.py
├── python_file.py
│
├── Fastapi/
│   ├── firstapi.py
│   ├── hello.py
│   └── README.md
│
├── apilogin/
│   ├── fast.py
│   ├── flask1.py
│   ├── h.py
│   └── tem.html
│
├── auth_api/
│   ├── login_table.py
│   ├── logindb.py
│   ├── model.py
│   ├── schema.py
│   ├── requirement.txt
│   └── README.md
│
├── flask/
│   ├── First_Flask/
│   ├── flask2/
│   └── marketproject/
│
├── mongodb/
│   ├── flask2.py
│   ├── main2.py
│   └── templates/
│
├── datasets and media files
│   ├── movies.csv
│   ├── TMDB 10000 Movies Dataset.csv
│   ├── netflix_titles_nov_2019.csv
│   ├── insurance_data.csv
│   ├── homeprices_banglore.csv
│   └── image files
│
├── trained models
│   ├── face_classifier.h5
│   └── vehicle_model.h5
│
└── video files
    └── videoplayback.mp4
```

---

# Main Project Areas

## 1. Deep Learning & CNN Projects

The repository contains multiple CNN and Deep Learning notebooks:

* CNN.ipynb
* numbers_cnn.ipynb
* type_cnn.ipynb
* facedetection.ipynb

Features:

* Image classification
* Face detection
* Number recognition
* Vehicle classification
* OpenCV image processing
* TensorFlow/Keras model training

Pretrained model files:

* `vehicle_model.h5`
* `face_classifier.h5`

---

# 2. FastAPI Projects

The `Fastapi` and `apilogin` folders contain backend API experiments.

Features:

* Basic API creation
* Request handling
* Login API concepts
* HTML integration
* Backend testing

Files:

```bash
Fastapi/
apilogin/
```

---

# 3. Authentication API

The `auth_api` folder contains a simple authentication system.

Features:

* Login database handling
* API schemas
* User models
* Database connection
* Authentication workflow

Files:

```bash
auth_api/
```

---

# 4. Flask Projects

The repository includes Flask backend experiments.

Features:

* Routing
* Templates
* Basic web applications
* Backend logic

Folders:

```bash
flask/
```

---

# 5. MongoDB Projects

The `mongodb` folder contains MongoDB integration examples.

Features:

* MongoDB connection
* Flask integration
* Database operations
* Template rendering

---

# 6. Data Science & Analysis

The repository contains datasets and notebooks for analysis.

Datasets:

* Movies dataset
* Netflix dataset
* Bangalore house price dataset
* Insurance dataset
* TMDB dataset

Concepts practiced:

* Data cleaning
* Visualization
* EDA
* Feature analysis
* Dataset handling

---

# 7. Python Programming Practice

Contains basic algorithm and Python logic programs.

Programs:

* Bubble Sort
* Insertion Sort
* Linked List concepts
* Python practice scripts

---

# Installation

## Clone Repository

```bash
git clone https://github.com/suriyaelumalai08/TestingFolder.git
```

## Move into Folder

```bash
cd TestingFolder
```

---

# Install Required Libraries

```bash
pip install numpy pandas matplotlib opencv-python tensorflow flask fastapi uvicorn pymongo scikit-learn
```

---

# Running Jupyter Notebooks

```bash
jupyter notebook
```

Then open any `.ipynb` file.

---

# Running FastAPI Project

Example:

```bash
uvicorn firstapi:app --reload
```

---

# Running Flask Project

```bash
python app.py
```

---

# Learning Goals of this Repository

This repository demonstrates practical learning in:

* Python Programming
* Machine Learning
* Deep Learning
* CNN Models
* Computer Vision
* OpenCV
* Flask Backend Development
* FastAPI Development
* MongoDB Integration
* Data Analysis
* Authentication Systems

---

# Problems in Current Repository Structure

The repository currently mixes:

* datasets
* notebooks
* models
* APIs
* images
* videos
* practice scripts

inside one root folder.

This makes the project look unstructured for recruiters.

A better structure would separate:

```bash
projects/
datasets/
models/
backend/
notebooks/
algorithms/
```

Right now it looks more like a practice dump folder than a production-ready repository.

---

# Recommended Improvements

## Important Improvements

* Add proper folder organization
* Add requirements.txt at root level
* Add comments and documentation
* Add screenshots for projects
* Create separate repositories for major projects
* Add Streamlit or Flask deployment
* Remove unnecessary media files
* Add proper project descriptions

---

# Author

## Suriya Elumalai

BCA Graduate | Python & AI Enthusiast

Skills:

* Python
* Machine Learning
* Deep Learning
* Computer Vision
* NLP Basics
* Flask
* FastAPI
* MongoDB
* Data Analysis

GitHub:

[https://github.com/suriyaelumalai08](https://github.com/suriyaelumalai08)

---

# License

This repository is created for educational and learning purposes.
