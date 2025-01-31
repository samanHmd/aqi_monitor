import requests
import time
import logging
from typing import Tuple, List, Optional

# logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class AQIMonitor:
    def __init__(self, latitude_1: float, longitude_1: float, latitude_2: float, longitude_2: float,
                 sampling_period: int = 5, sampling_rate: int = 1, api_token: str = ''):
       
        #initialize AQIMonitor with necessary parameters

        if not api_token:
            raise ValueError("API token must be provided.")

        self.latitude_1 = latitude_1
        self.longitude_1 = longitude_1
        self.latitude_2 = latitude_2
        self.longitude_2 = longitude_2
        #at least 1 min
        self.sampling_period = max(1, sampling_period)  
        #at least 1 sample per minute
        self.sampling_rate = max(1, sampling_rate)  
        self.api_token = api_token
        self.sampling_status = "IDLE"
        self.data = []

    def _fetch_station_pm25(self, latitude: float, longitude: float) -> Optional[float]:
        
        #this function will fetch PM2.5 value for a specific station using its latitude and longitude.
        #in the output it returns PM2.5 value if available otherwise returns none
        

        url = f"https://api.waqi.info/feed/geo:{latitude};{longitude}/?token={self.api_token}"
        retries = 3  #try agian up to 3 times if request failed

        for attempt in range(retries):
            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()  #for http errors
                data = response.json()

                if "data" in data and "iaqi" in data["data"] and "pm25" in data["data"]["iaqi"]:
                    return data["data"]["iaqi"]["pm25"]["v"]

                logging.warning(f"PM2.5 data not found for {latitude}, {longitude} (Attempt {attempt + 1})")

            except requests.RequestException as e:
                logging.error(f"Error fetching PM2.5 for {latitude}, {longitude} (Attempt {attempt + 1}): {e}")

            time.sleep(2)  #wait before retrying

        return None

    def _get_stations_in_area(self) -> List[Tuple[float, float]]:
        
        #this function will fetch stations coordinates within the specified area.
        #returns a list of tuples containing (latitude,longitude) for all the stations in the area
        
        logging.info("Fetching available AQI monitoring stations...")

        api_url = f"https://api.waqi.info/map/bounds/?token={self.api_token}&latlng={self.latitude_1},{self.longitude_1},{self.latitude_2},{self.longitude_2}"

        try:
            response = requests.get(api_url, timeout=5)
            response.raise_for_status()
            data = response.json()

            if data.get("status") != "ok" or "data" not in data:
                logging.warning("No valid station data found.")
                return []

            stations = [(station["lat"], station["lon"]) for station in data["data"]]

            if stations:
                logging.info(f"Found {len(stations)} stations in the area.")
            else:
                logging.warning("No monitoring stations found within the specified area.")

            return stations

        except requests.RequestException as e:
            logging.error(f"Error fetching AQI stations: {e}")
            return []

    def start_sampling(self):
        
        #this is the main function which starts the sampling process to collect PM2.5 data
        
        self.sampling_status = "RUNNING"
        collected_data = []
        stations = self._get_stations_in_area()

        if not stations:
            logging.error("No stations found within the specified area.")
            self.sampling_status = "FAILED"
            return

        total_samples = self.sampling_period * self.sampling_rate
        interval = 60 / self.sampling_rate

        logging.info(f"Starting sampling for {self.sampling_period} minutes at a rate of {self.sampling_rate} samples per minute.")

        for _ in range(total_samples):

            if self.sampling_status == "STOPPED":  # Stop if user interrupts
                logging.info("Sampling was manually stopped.")
                return
            pm25_values = [self._fetch_station_pm25(lat, lon) for lat, lon in stations if self._fetch_station_pm25(lat, lon) is not None]

            if pm25_values:
                average_pm25 = sum(pm25_values) / len(pm25_values)
                collected_data.append(average_pm25)
                logging.info(f"Collected PM2.5 data: {average_pm25} µg/m³")
            else:
                logging.warning("No PM2.5 data collected in this interval.")

            time.sleep(interval)

        if collected_data:
            self.data = collected_data
            self.sampling_status = "DONE"
            logging.info("Sampling completed successfully.")
        else:
            self.sampling_status = "FAILED"
            logging.error("Sampling failed. No data collected.")

        if self.sampling_status == "STOPPED":  # Stop if user interrupts
            logging.info("Sampling was manually stopped.")
            return

    def get_status(self) -> str:

        #this funciton will show sampling status
        #in the output it will return a string
        return self.sampling_status

    def get_avg_pm25(self) -> Optional[float]:
        
        #this function will calculate and return the average PM2.5 value
        #returns average PM2.5 value 
        if self.sampling_status == "DONE" and self.data:
            return sum(self.data) / len(self.data)
        else:
            logging.warning("Sampling not completed or no data available.")
            return None

    def stop_sampling(self):
        #manually stops the sampling process
        if self.sampling_status == "RUNNING":
            self.sampling_status = "STOPPED"
            logging.info("Sampling process has been manually stopped.")