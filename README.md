# Configuring Data Links and Dependencies for Car Market Adviser App

Before running the Car Market Adviser App, follow these steps to set up and configure the necessary components:

## 1. Update Data Links

After extracting the app files, manually update the data links in each page script located in path like :

**Path:** `C:\Users\NAME\Downloads\AnalyticsApp-main\pages`

- **analysis.py**
- **Home.py**
- **home1.py**
- **home2.py**

Look for the data set loading line :

df = pd.read_csv("PATH")

Replace "PATH" with the correct path to the clean_data.csv file. Typically, it will be in a path resembling:

"C:\Users\NAME\Downloads\Car_Market_Adviser\data"

2. Update Model Path
In the Prediction.py script, find the line where the model is loaded:

model = joblib.load("PATH")
Change "PATH" to the correct path where the model is extracted. This path should look like:

"C:\Users\NAME\Downloads\Car_Market_Adviser\models"

3. Install Required Libraries
Navigate to the directory where main.py script exists:

Path: "C:\Users\NAME\Downloads\Car_Market_Adviser\"

Open the Command Prompt (CMD) in this directory:

python -m venv myenv
myenv\Scripts\activate
pip install -r requirements.txt

4. Run the App
After installing the required libraries, run the main script:
python main.py

You will see a link like:

Dash is running on http://127.0.0.1:8050/

Click on the link, and it will prompt you to open the app in your browser. Enjoy using our Car Market Adviser App! Thank you.
