# Depression Detection System

This project is a web-based application designed to detect depression using facial expression analysis. The system is built using .NET ASP Core MVC and integrates a Python script to analyze video samples, extracting features such as Action Units (AUs), pose, and gaze, which are then processed by a logistic regression model to determine if a subject is depressed.

## Table of Contents

- [Introduction](#introduction)
- [Demo](#demo)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Model Details](#model-details)
- [Future Work](#future-work)

## Introduction

The Depression Detection System is an innovative tool designed for the early identification of depression through facial expression analysis. It leverages the OpenFace toolkit for feature extraction and a logistic regression model to analyze these features. Users can upload videos, which are then processed to generate a prediction on whether the subject exhibits signs of depression.

## Demo

![Demo Video](https://github.com/user-attachments/assets/e4d50d87-b18d-459d-8313-1ce21799470c)

This video demonstrates the functionality of the Depression Detection System, showing how users can upload video samples and receive predictions on whether the subject is "Depressed" or "Not Depressed."

## Features

- **Video Upload**: Upload video samples for analysis.
- **Feature Extraction**: Utilizes OpenFace to extract Action Units (AUs), pose, and gaze features.
- **Data Preprocessing**: The extracted features undergo preprocessing, including scaling and PCA.
- **Depression Prediction**: A logistic regression model predicts whether the subject in the video is depressed.
- **Result Display**: The prediction result is displayed as either "Depressed" or "Not Depressed".

## Technologies Used

- **Backend**: .NET ASP Core MVC
- **Frontend**: HTML, CSS, JavaScript
- **Machine Learning**: Python, scikit-learn, pandas, OpenFace
- **Modeling**: Logistic Regression
- **Data Processing**: PCA, MinMaxScaler

## Installation

### Prerequisites

- .NET Core SDK
- Python 3.7+
- [OpenFace 2.2.0](https://github.com/TadasBaltrusaitis/OpenFace) (Download and install)
- Git

### Clone the Repository

```bash
git clone https://github.com/yourusername/depression-detection-system.git
cd depression-detection-system
```

### Setting Up OpenFace

1. Download OpenFace from the [official GitHub repository](https://github.com/TadasBaltrusaitis/OpenFace).
2. Extract the contents and place the entire folder into the following directory:

   ```
   Employees_System-master/models/
   ```

   The path should look like this:

   ```
   Employees_System-master/models/OpenFace_2.2.0_win_x64/
   ```

### Setting Up the Backend

1. Navigate to the project directory.
2. Restore the NuGet packages.
3. Build the project.

```bash
dotnet restore
dotnet build
```

### Setting Up the Python Environment

1. Install the required Python packages:

```bash
pip install -r requirements.txt
```

2. Ensure the paths in the Python script (`main.py`) match the locations of your OpenFace installation and video samples.

## Usage

1. Start the web application:

```bash
dotnet run
```

2. Open your browser and navigate to `http://localhost:5000`.
3. Upload a video sample for analysis.
4. The application will process the video, extract relevant features, and display whether the subject is "Depressed" or "Not Depressed".

## Model Details

The logistic regression model was trained on a dataset of facial features extracted using OpenFace. It considers various Action Units (AUs), pose, and gaze features to predict the likelihood of depression.

### Python Script Workflow

1. **Feature Extraction**: Extracts AUs, pose, gaze, and facial landmarks using OpenFace.
2. **Data Preprocessing**: Applies scaling and PCA to reduce dimensionality.
3. **Prediction**: Uses the logistic regression model to classify the subject as "Depressed" or "Not Depressed".

## Future Work

In future iterations, the system will be enhanced with a more robust architecture:

- **Frontend**: The user interface will be redesigned using Angular to improve responsiveness and user experience.
- **Backend**: The backend will be refactored into a .NET ASP API, providing a more scalable and maintainable codebase.
- **Database**: SQL Server will be integrated to manage and store user data and analysis results efficiently.

---
