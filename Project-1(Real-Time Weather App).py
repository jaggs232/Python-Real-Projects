import streamlit as st
import requests
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title="Simple Weather App", page_icon="🌤️")
st.title("🌤️ Simple Weather App")
st.write("Get current weather information for any city in the world!")


API_KEY = "738f43a4d5a178d96f5494fc08defda8"  
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
def get_weather_emoji(weather_description):
    
    weather_lower = weather_description.lower()
    
    if 'clear' in weather_lower:
        return '☀️'
    elif 'cloud' in weather_lower:
        return '☁️'
    elif 'rain' in weather_lower or 'drizzle' in weather_lower:
        return '🌧️'
    elif 'snow' in weather_lower:
        return '❄️'
    elif 'storm' in weather_lower or 'thunder' in weather_lower:
        return '⛈️'
    elif 'mist' in weather_lower or 'fog' in weather_lower:
        return '🌫️'
    else:
        return '🌤️'


def get_weather_data(city_name):
    """
    Get weather data from OpenWeatherMap API
    Returns weather data dictionary or None if error occurs
    """
    try:
        
        params = {
            'q': city_name,           
            'appid': API_KEY,         
            'units': 'metric'         
        }
        
       
        response = requests.get(BASE_URL, params=params)
        
       
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"City '{city_name}' not found. Please check the spelling.")
            return None
            
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to weather service: {e}")
        return None


def display_weather_info(weather_data):
    """Display weather information in a nice format"""
    
    
    city_name = weather_data['name']
    country = weather_data['sys']['country']
    temperature = weather_data['main']['temp']
    feels_like = weather_data['main']['feels_like']
    humidity = weather_data['main']['humidity']
    pressure = weather_data['main']['pressure']
    description = weather_data['weather'][0]['description']
    wind_speed = weather_data['wind'].get('speed', 0)
    
    
    weather_emoji = get_weather_emoji(description)
    
    
    st.success(f"🗺️ Weather for {city_name}, {country}")
    
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
      
        st.markdown(f"<div style='font-size: 100px; text-align: center;'>{weather_emoji}</div>", 
                   unsafe_allow_html=True)
    
    with col2:
        
        st.markdown(f"# {temperature:.1f}°C")
        st.markdown(f"**{description.title()}**")
        st.markdown(f"Feels like {feels_like:.1f}°C")
    
    
    st.subheader("📊 Weather Details")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🌡️ Temperature", f"{temperature:.1f}°C")
        st.metric("💧 Humidity", f"{humidity}%")
    
    with col2:
        st.metric("🌬️ Wind Speed", f"{wind_speed} m/s")
        st.metric("⏱️ Pressure", f"{pressure} hPa")
    
    with col3:
        st.metric("🌡️ Feels Like", f"{feels_like:.1f}°C")
        
        wind_kmh = wind_speed * 3.6
        st.metric("💨 Wind (km/h)", f"{wind_kmh:.1f}")


st.subheader("🔍 Search for Weather")


with st.form("weather_search"):
    col1, col2 = st.columns([3, 1])
    
    with col1:
        city_input = st.text_input(
            "Enter city name:", 
            placeholder="e.g., London, New York, Tokyo, Paris",
            help="Enter the name of any city worldwide"
        )
    
    with col2:
        st.write("")  
        search_clicked = st.form_submit_button("🔍 Get Weather", type="primary")


if search_clicked:
    if not city_input:
        st.warning("⚠️ Please enter a city name!")
    elif API_KEY == "your_api_key_here":
        st.error("🔑 API Key Required!")
        st.info("""
        **To use this app, you need a free API key:**
        1. Go to [OpenWeatherMap](https://openweathermap.org/api)
        2. Sign up for free
        3. Get your API key
        4. Replace 'your_api_key_here' in the code with your actual key
        """)
        st.code("API_KEY = 'your_actual_api_key_here'")
    else:
        
        with st.spinner(f"🌍 Getting weather data for {city_input}..."):
           
            weather_data = get_weather_data(city_input)
            
          
            if weather_data:
                display_weather_info(weather_data)
                
            
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.caption(f"📅 Last updated: {current_time}")


st.subheader("🌍 Popular Cities")
st.write("Click on any city for quick weather check:")

cities_col1, cities_col2, cities_col3, cities_col4 = st.columns(4)

popular_cities = [
    "London", "New York", "Tokyo", "Paris",
    "Sydney", "Dubai", "Mumbai", "Berlin",
    "Singapore", "Toronto", "Barcelona", "Rome"
]

for i, city in enumerate(popular_cities):
    col_index = i % 4
    if col_index == 0:
        current_col = cities_col1
    elif col_index == 1:
        current_col = cities_col2
    elif col_index == 2:
        current_col = cities_col3
    else:
        current_col = cities_col4
    
    with current_col:
        if st.button(f"🏙️ {city}", key=f"city_{i}"):
            if API_KEY != "your_api_key_here":
                with st.spinner(f"Getting weather for {city}..."):
                    weather_data = get_weather_data(city)
                    if weather_data:
                        display_weather_info(weather_data)
                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        st.caption(f"📅 Last updated: {current_time}")
            else:
                st.error("Please add your API key first!")


with st.sidebar:
    st.header("ℹ️ How to Use This App")
    
    st.write("**Steps:**")
    st.write("1. Get a free API key from OpenWeatherMap")
    st.write("2. Enter city name in the search box")
    st.write("3. Click 'Get Weather' button")
    st.write("4. View current weather information")
    
    st.write("---")
    st.write("**Features:**")
    st.write("✅ Current temperature")
    st.write("✅ Weather description")
    st.write("✅ Humidity and pressure")
    st.write("✅ Wind speed")
    st.write("✅ Quick city buttons")
    
    st.write("---")
    st.write("**API Key Setup:**")
    st.info("""
    1. Visit openweathermap.org
    2. Create free account  
    3. Generate API key
    4. Replace in code:
    `API_KEY = "your_key_here"`
    """)
    
    # Show current API key status
    if API_KEY == "your_api_key_here":
        st.error("🔴 API Key Not Set")
    else:
        st.success("🟢 API Key Configured")

# STEP 10: Tips and information
st.markdown("---")
st.subheader("💡 Tips for Better Results")

tip_col1, tip_col2 = st.columns(2)

with tip_col1:
    st.write("**City Name Tips:**")
    st.write("• Use English names")
    st.write("• Try 'City, Country' format")
    st.write("• Example: 'Paris, France'")
    st.write("• Check spelling carefully")

with tip_col2:
    st.write("**Understanding Weather:**")
    st.write("• Temperature in Celsius")
    st.write("• Wind speed in meters/second")
    st.write("• Pressure in hectopascals")
    st.write("• Humidity as percentage")