import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import datetime
from io import BytesIO

# Function to fetch weather data
def get_weather(city):
    api_key = "c7a29b27adab935ef66c66efbc4989a1"
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    return response.json()

# Function to fetch forecast data
def get_forecast(city):
    api_key = "c7a29b27adab935ef66c66efbc4989a1"
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    return response.json()

# Function to display weather
def show_weather():
    city = city_entry.get()
    if city:
        weather = get_weather(city)
        forecast = get_forecast(city)
        if weather['cod'] == 200:
            temp = weather['main']['temp']
            description = weather['weather'][0]['description']
            wind_speed = weather['wind']['speed']
            icon_code = weather['weather'][0]['icon']
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            icon_response = requests.get(icon_url)
            icon_image = ImageTk.PhotoImage(Image.open(BytesIO(icon_response.content)))
            
            current_weather_label.config(text=f"Temperature: {temp}°C\nDescription: {description}\nWind Speed: {wind_speed} m/s")
            weather_icon_label.config(image=icon_image)
            weather_icon_label.image = icon_image
            
            # Display forecast
            forecast_text = "Hourly Forecast:\n"
            for i in range(0, 40, 8):  # 8 * 3 = 24 hours
                forecast_time = datetime.datetime.fromtimestamp(forecast['list'][i]['dt']).strftime('%Y-%m-%d %H:%M:%S')
                forecast_temp = forecast['list'][i]['main']['temp']
                forecast_desc = forecast['list'][i]['weather'][0]['description']
                forecast_text += f"{forecast_time}: {forecast_temp}°C, {forecast_desc}\n"
            
            forecast_label.config(text=forecast_text)
        else:
            messagebox.showerror("Error", "City not found!")
    else:
        messagebox.showwarning("Input Error", "Please enter a city name")

# Set up the GUI
root = tk.Tk()
root.title("Advanced Weather App")
root.geometry("600x400")

# City entry
tk.Label(root, text="Enter city name:").pack(pady=10)
city_entry = tk.Entry(root)
city_entry.pack(pady=5)

# Show weather button
tk.Button(root, text="Show Weather", command=show_weather).pack(pady=10)

# Current weather display label
current_weather_label = tk.Label(root, text="", font=("Helvetica", 12))
current_weather_label.pack(pady=10)

# Weather icon display label
weather_icon_label = tk.Label(root, image=None)
weather_icon_label.pack(pady=5)

# Forecast display label
forecast_label = tk.Label(root, text="", font=("Helvetica", 10), justify="left")
forecast_label.pack(pady=20)

# Start the main event loop
root.mainloop()
