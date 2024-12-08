# Disease Detection System Using Symptoms

This project is a simple disease detection system built using Python and the Tkinter GUI library. It uses machine learning (Random Forest Classifier) to predict diseases based on user-reported symptoms. The system takes up to five symptoms as input and outputs a potential disease diagnosis.

## Features

- User-friendly GUI to input symptoms
- Predicts disease based on symptoms using a Random Forest Classifier
- Disease predictions based on pre-trained data
- Simple and interactive design using Tkinter

## Technologies Used

- **Python**: The programming language used for building the system.
- **Tkinter**: For the graphical user interface (GUI).
- **Scikit-learn**: For training the Random Forest Classifier model.
- **Pandas**: For handling and processing the dataset.
- **NumPy**: For numerical operations on the data.

## Files Used

1. **Training.csv**: Contains the training data with symptoms and corresponding diseases.
2. **Testing.csv**: Used to test the model with new data.

## How It Works

1. The user selects five symptoms from a dropdown list on the GUI.
2. The symptoms are fed into the trained Random Forest model.
3. The model predicts the disease based on the input symptoms.
4. The result is displayed on the screen, showing the predicted disease.

## Dependencies

- `Tkinter`: Used for the graphical user interface.
- `pandas`: Used for handling data.
- `numpy`: Used for numerical operations.
- `scikit-learn`: Used for machine learning tasks.

Install dependencies using `pip`:

```bash
pip install pandas numpy scikit-learn
```

## How to Run

1. Clone this repository or download the project files.
2. Make sure you have the necessary dependencies installed.
3. Run the script using Python:

```bash
python disease_detection.py
```

4. Enter the symptoms in the GUI, and the disease prediction will be displayed.

### Example

* **Symptom 1**: Abdominal Pain
* **Symptom 2**: Diarrhoea
* **Symptom 3**: Fever
* **Symptom 4**: Weakness in Limbs
* **Symptom 5**: Chest Pain

Click on "SEARCH" to predict the disease based on the selected symptoms.

## Dataset

The dataset used for training the model includes various symptoms and their corresponding diseases. It is represented in a CSV format with symptoms as columns and the disease as the target variable.

## Future Improvements

* Add more symptoms and diseases to improve prediction accuracy.
* Implement additional machine learning models to compare performance.
* Create a web-based interface for easier access.
* Integrate with healthcare APIs for real-time disease updates.

## Author

* **Harshit Waldia** - Developer

