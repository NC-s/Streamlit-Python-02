# Streamlit-Python-02
# Task
```
# Main Task
Task 1 - Project Overview and Demo
Task 2 - Turn Simple Python Scripts into Web Apps
Task 3 - Load the Twitter US Airline Sentiment Data
Task 4 - Display Tweets in the Sidebar
Task 5 - Plot Interactive Bar Plots and Pie Charts
Task 6 - Plotting Location Data on an Interactive Map
Task 7 - Plot Number of Tweets by Sentiment for Each Airline
Task 8 - Word Cloud for Positive, Neutral, and Negative Tweets
# Sub Task
Task 1 - Generate requirement.txt
Task 2 - Use Venv for development
```

# Example
![alt text](https://github.com/NC-s/Streamlit-Python-02/blob/main/pic/example_1.png?raw=true)
![alt text](https://github.com/NC-s/Streamlit-Python-02/blob/main/pic/example_2.png?raw=true)

# Advantage of Streamlit
## Question:
In the following code-snippet, a dataset is loaded into a pandas dataframe and the NA values are dropped when the load_data() is called. The load_data() function is called twice: first after the function definition and the second time after missing values are counted. How many times do you think the entire dataset is loaded into a pandas dataframe using the read_csv() function?
```
@st.cache(persist=True)
def load_data():
    data = pd.read_csv('dataset.csv')
    data.dropna(inplace=True)
    return data

df = load_data()
count_missing_vals = df.isnull().sum()
df = load_data()
```
## Answer
Only Once
