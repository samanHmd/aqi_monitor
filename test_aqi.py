from aqi_monitor import AQIMonitor

#your api_token
API_TOKEN = "921068569609ade79515f3c3f445336a2a3adf59"

#your test coordinates
latitude_1 = 45.69
longitude_1 = -73.54
latitude_2 = 45.37
longitude_2 = -73.74

#sampling parameters
sampling_period = 2  # Collect data for 2 minutes (for testing)
sampling_rate = 1    # 1 sample per minute

#initialize the AQIMonitor module instance
aqi_monitor = AQIMonitor(
    latitude_1, longitude_1, latitude_2, longitude_2, 
    sampling_period, sampling_rate, API_TOKEN
)

#start sampling
print("Starting AQI Monitoring...")
aqi_monitor.start_sampling()

#check the status
print("Sampling Status:", aqi_monitor.get_status())

#get the final PM2.5 average
avg_pm25 = aqi_monitor.get_avg_pm25()

#see the result
if avg_pm25 is not None:
    print(f"Final Average PM2.5: {avg_pm25} µg/m³")
else:
    print("No PM2.5 data available.")
