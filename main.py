import streamlit as st
from pymongo import MongoClient
from mongoconnection import MongoConnect
from datetime import date
import time
import requests
#client = MongoClient('mongodb://localhost:27017')  
client= st.experimental_connection('testdb', type=MongoConnect, host=st.secrets['mclient'])

today = date.today()
localtime = time.localtime()
formatted_date = time.strftime("%Y-%m-%d", localtime)
formatted_time = time.strftime("%H:%M:%S", localtime)

api_key = "8a99a67d9f6a03abb8583aadef91a69c"
def get_weather(api_key, city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"  # To get temperature in Celsius
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if data["cod"] == 200:
        weather = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        st.write(f"Weather in {city}: {weather}")
        st.write(f"Temperature: {temperature}°C")
        st.write(f"Humidity: {humidity}%")
        st.write(f"Wind Speed: {wind_speed} m/s")
    else:
        st.write(f"Failed to get weather data for {city}")

with st.sidebar:
    st.subheader("Today's Date : ")
    st.write(formatted_date,"\n")
    
    st.subheader("Today's Time : ")
    st.write(formatted_time,"\n")
    st.subheader("Weather report : ")
    city = st.text_input("### Enter your city name:", "Hyderabad")
    st.write("\n")
    get_weather(api_key, city)

db = client.database('todo_app') 
#collection = client.db['tasks']
collection = client.collection('todo_app','tasks')
 
next_id = 1
def add_task(task):
    next_id = collection.count_documents({}) + 1
    data = {"id": next_id, "task": task}
    client.insert_one('todo_app','tasks',data)

def delete_task(task_id):
    que = {"id": task_id}
    client.delete_one('todo_app','tasks',que)

def show_tasks():
    tasks = client.find('todo_app','tasks')
    if tasks:
        st.subheader("Activities to do")
        i=1
        for task in tasks:
            if task['id']!=i:
                client.update_one('todo_app', 'tasks', {'id': task['id']}, {"$set": { 'id': i }})
            st.write(f" ID: {task['id']},  Task to complete: {task['task']}")
            i+=1
    else:
        st.write("Your todo list is empty.")

def main():
    st.title("Personalized Todo List")
    task = st.text_input("Enter a task:")
    if st.button("Add Task"):
        add_task(task)
    
    show_tasks()

    delete_task_id = st.number_input("Enter the ID of the task to delete:", min_value=1, step=1)
    if st.button("Delete Task"):
        delete_task(delete_task_id)

if __name__ == "__main__":
    main()
