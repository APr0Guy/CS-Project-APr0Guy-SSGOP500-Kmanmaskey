import customtkinter as ctk
from PIL import Image #for loading image
# for weather api
import asyncio
import aiohttp

import threading
import os
from datetime import datetime
import time #for setting timer for api fetching request (10 min)

from config import API_KEY #so key is already there

# so all items with weather share these so timer for fetching is global
weather_cache = None
weather_cache_time = 0
weather_cache_updated = None
weather_request_running = False
WEATHER_CACHE_SECONDS = 20 * 60

class Weather(ctk.CTkFrame):
    def __init__(self,parent,compact=False):
        super().__init__(parent)

        self.compact = compact


        self.api_key = API_KEY


        self.place_id = "kathmandu"
        self.configure(fg_color=("#FFFFFF","#30343B"),corner_radius=14)
        self.grid_columnconfigure(0,weight=1)

        # ------------------------ weather heading
        self.heading_frame = ctk.CTkFrame(self,fg_color="transparent")
        self.heading_frame.grid(row=0,column=0,sticky="ew",padx=18,pady=(14,5))
        self.heading_frame.grid_columnconfigure(0,weight=1)

        self.heading_label = ctk.CTkLabel(self.heading_frame,text="Weather",font=("Arial",18,"bold"),text_color=("#1F2937","#F3F4F6"))
        self.heading_label.grid(row=0,column=0,sticky="w")
        self.location_label = ctk.CTkLabel(self.heading_frame,text="⌖  Kathmandu, Nepal",font=("Arial",12),text_color=("#64748B","#A1A1AA"))
        self.location_label.grid(row=0,column=1,padx=8)
        self.refresh_btn = ctk.CTkButton(self.heading_frame,text="Refresh",width=72,height=29,fg_color=("#FC5C3D","#D4AF37"),
            hover_color=("#D9816F","#DDC881"),text_color=("white","#242424"),command=self.start_weather_request)
        self.refresh_btn.grid(row=0,column=2)

        # ------------------------ current weather information
        self.current_weather_frame = ctk.CTkFrame(self,fg_color=("#F1F5F9","#393E45"),corner_radius=12)
        self.current_weather_frame.grid(row=1,column=0,sticky="ew",padx=18,pady=8)
        self.current_weather_frame.grid_columnconfigure(0,weight=1)

        self.current_condition = ctk.CTkLabel(self.current_weather_frame,text="Loading weather...",font=("Arial",15,"bold"),text_color=("#1F2937","#F3F4F6"))
        self.current_condition.grid(row=0,column=0,sticky="w",padx=16,pady=(13,0))
        self.current_temperature = ctk.CTkLabel(self.current_weather_frame,text="--°C",font=("Arial",42,"bold"),text_color=("#FC5C3D","#D4AF37"))
        self.current_temperature.grid(row=1,column=0,sticky="w",padx=16,pady=(0,5))
        self.current_details = ctk.CTkLabel(self.current_weather_frame,text="Feels like --°C     Humidity --%     Wind -- km/h",
            font=("Arial",12),text_color=("#64748B","#A1A1AA"),anchor="w")
        self.current_details.grid(row=2,column=0,sticky="w",padx=16,pady=(0,13))

        # ------------------------ forecast area
        self.forecast_heading = ctk.CTkLabel(self,text="5 Day Forecast",font=("Arial",14,"bold"),text_color=("#1F2937","#F3F4F6"))
        self.forecast_heading.grid(row=2,column=0,sticky="w",padx=18,pady=(8,4))
        self.forecast_frame = ctk.CTkFrame(self,fg_color="transparent")
        self.forecast_frame.grid(row=3,column=0,sticky="ew",padx=14,pady=(0,14))
        self.forecast_frame.grid_columnconfigure((0,1,2,3,4),weight=1,uniform="forecast")

        self.forecast_placeholders = []
        for index in range(5):
            self.forecast_card = ctk.CTkFrame(self.forecast_frame,fg_color=("#F1F5F9","#393E45"),corner_radius=10)
            self.forecast_card.grid(row=0,column=index,sticky="nesw",padx=4,pady=3)
            self.forecast_card.grid_columnconfigure(0,weight=1)
            ctk.CTkLabel(self.forecast_card,text="---",font=("Arial",11,"bold"),text_color=("#64748B","#A1A1AA")).grid(row=0,column=0,pady=(9,2))
            ctk.CTkLabel(self.forecast_card,text="☁",font=("Arial",21),text_color=("#FC5C3D","#D4AF37")).grid(row=1,column=0,pady=2)
            ctk.CTkLabel(self.forecast_card,text="--° / --°",font=("Arial",11,"bold"),text_color=("#1F2937","#F3F4F6")).grid(row=2,column=0,pady=(2,9))
            self.forecast_placeholders.append(self.forecast_card)

        self.status_label = ctk.CTkLabel(self,text="",font=("Arial",11),text_color=("#64748B","#A1A1AA"))
        self.status_label.grid(row=4,column=0,sticky="w",padx=18,pady=(0,8))

        #rma3kf9240bkjdb5lhov98rh9zs4y6nxjnkc9ija || api key for weather
        #https://www.meteosource.com/weather-api-kathmandu

        if not self.api_key:
            self.status_label.configure(text="Set METEOSOURCE_API_KEY to load live weather.")
        else:
            self.after(200,self.start_weather_request)

    #------------------------------------------------ all functions to be used
    #loads weather outside the main tkinter thread so the app does not freeze while waiting for the api
    def start_weather_request(self):
        global weather_cache, weather_cache_time, weather_cache_updated, weather_request_running
        if not self.api_key:
            self.status_label.configure(text="Set METEOSOURCE_API_KEY to load live weather.")
            return

        if weather_cache is not None and time.monotonic() - weather_cache_time < WEATHER_CACHE_SECONDS:
            self.display_weather(weather_cache)
            if weather_cache_updated is not None:
                self.status_label.configure(text=f"Cached weather · Updated {weather_cache_updated.strftime('%I:%M %p')}")
            return

        if weather_request_running:
            self.status_label.configure(text="Weather is already updating...")
            self.refresh_btn.configure(state="disabled")
            self.after(1000,lambda:self.start_weather_request() if self.winfo_exists() else None)
            return

        self.status_label.configure(text="Updating weather...")
        self.refresh_btn.configure(state="disabled")
        weather_request_running = True
        threading.Thread(target=lambda: asyncio.run(self.get_weather()),daemon=True).start()

    #gets the current weather and forecast from Meteosource
    async def get_weather(self):
        global weather_cache, weather_cache_time, weather_cache_updated, weather_request_running
        url = "https://www.meteosource.com/api/v1/free/point"
        params = {"place_id":self.place_id,"sections":"current,daily","timezone":"Asia/Kathmandu","language":"en","units":"metric","key":self.api_key}
        try:
            timeout = aiohttp.ClientTimeout(total=15)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url,params=params) as response:
                    if response.status != 200:
                        error_data = await response.json(content_type=None)
                        raise RuntimeError(error_data.get("detail",f"Weather request failed ({response.status})."))
                    
                    weather_data = await response.json()

            weather_cache = weather_data
            weather_cache_time = time.monotonic()
            weather_cache_updated = datetime.now()
            weather_request_running = False

            self.after(0,lambda:self.display_weather(weather_data))

        except Exception as error:
            weather_request_running = False
            error_text = str(error)
            self.after(0,lambda:self.display_weather_error(error_text))

    #shows the weather information returned by the api
    def display_weather(self,weather_data):
        if not self.winfo_exists():
            return
        current = weather_data.get("current",{})
        temperature = current.get("temperature","--")
        feels_like = current.get("feels_like","--")
        humidity = current.get("humidity","--")
        wind = current.get("wind",{})
        wind_speed = wind.get("speed","--") if isinstance(wind,dict) else wind
        summary = current.get("summary",current.get("icon","Current conditions"))

        summary_text = str(summary).lower()
        if "thunder" in summary_text or "storm" in summary_text:
            current_symbol = "⛈"
        elif "rain" in summary_text or "drizzle" in summary_text or "shower" in summary_text:
            current_symbol = "🌧"
        elif "snow" in summary_text:
            current_symbol = "❄"
        elif "fog" in summary_text or "mist" in summary_text:
            current_symbol = "🌫"
        elif "clear" in summary_text or "sun" in summary_text:
            current_symbol = "☀"
        elif "cloud" in summary_text or "overcast" in summary_text:
            current_symbol = "☁"
        else:
            current_symbol = "🌤"
        self.current_condition.configure(text=f"{current_symbol}  {summary}")
        self.current_temperature.configure(text=f"{temperature}°C")
        self.current_details.configure(text=f"Feels like {feels_like}°C     Humidity {humidity}%     Wind {wind_speed} km/h")

        for widget in self.forecast_frame.winfo_children():
            widget.destroy()
        daily_data = weather_data.get("daily",{}).get("data",[])
        for index,day_data in enumerate(daily_data[:5]):
            self.forecast_frame.grid_columnconfigure(index,weight=1,uniform="forecast")
            forecast_card = ctk.CTkFrame(self.forecast_frame,fg_color=("#F1F5F9","#393E45"),corner_radius=10)
            forecast_card.grid(row=0,column=index,sticky="nesw",padx=4,pady=3)
            forecast_card.grid_columnconfigure(0,weight=1)
            day_text = day_data.get("day",day_data.get("date","Day"))
            try:
                day_text = datetime.strptime(day_text[:10],"%Y-%m-%d").strftime("%a")
            except (ValueError,TypeError):
                day_text = str(day_text)[:3]
            all_day = day_data.get("all_day",{})
            low = all_day.get("temperature_min",day_data.get("temperature_min","--"))
            high = all_day.get("temperature_max",day_data.get("temperature_max","--"))
            day_summary = day_data.get("weather",day_data.get("summary","Cloudy"))
            ctk.CTkLabel(forecast_card,text=day_text,font=("Arial",11,"bold"),text_color=("#64748B","#A1A1AA")).grid(row=0,column=0,pady=(9,2))
            forecast_summary = str(day_summary).lower()
            if "thunder" in forecast_summary or "storm" in forecast_summary:
                forecast_symbol = "⛈"
            elif "rain" in forecast_summary or "drizzle" in forecast_summary or "shower" in forecast_summary:
                forecast_symbol = "🌧"
            elif "snow" in forecast_summary:
                forecast_symbol = "❄"
            elif "fog" in forecast_summary or "mist" in forecast_summary:
                forecast_symbol = "🌫"
            elif "clear" in forecast_summary or "sun" in forecast_summary:
                forecast_symbol = "☀"
            elif "cloud" in forecast_summary or "overcast" in forecast_summary:
                forecast_symbol = "☁"
            else:
                forecast_symbol = "🌤"
            ctk.CTkLabel(forecast_card,text=forecast_symbol,font=("Arial",21),text_color=("#FC5C3D","#D4AF37")).grid(row=1,column=0,pady=2)
            ctk.CTkLabel(forecast_card,text=f"{high}° / {low}°",font=("Arial",11,"bold"),text_color=("#1F2937","#F3F4F6")).grid(row=2,column=0,pady=(2,9))

        updated_at = datetime.now().strftime("Updated %I:%M %p")
        self.status_label.configure(text=updated_at)
        self.refresh_btn.configure(state="normal")

    #shows any connection or api error without closing the rest of the app
    def display_weather_error(self,error):
        if not self.winfo_exists():
            return
        self.current_condition.configure(text="Weather unavailable")
        self.status_label.configure(text=f"{error[:120]}")
        self.refresh_btn.configure(state="normal")
