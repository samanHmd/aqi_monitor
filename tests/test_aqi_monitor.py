import pytest
import requests_mock
from aqi_monitor import AQIMonitor

# api_token
API_TOKEN = "your_fake_api_token"

#test coordinates 
LAT1, LON1 = 37.78, -122.45  
LAT2, LON2 = 37.70, -122.35  

#mock station response
MOCKED_STATIONS_RESPONSE = {
    "status": "ok",
    "data": [
        {"lat": 37.75, "lon": -122.42, "uid": 1},
        {"lat": 37.76, "lon": -122.41, "uid": 2},
        {"lat": 37.74, "lon": -122.43, "uid": 3}
    ]
}

#mocked PM2.5 data response
MOCKED_PM25_RESPONSE = {
    "status": "ok",
    "data": {
        "aqi": 55,
        "iaqi": {"pm25": {"v": 12.4}}
    }
}


#test nitialization _ edge cases
def test_aqi_monitor_initialization():
    #this function will test valid and invalid initializations 
    
    # valid case
    monitor = AQIMonitor(LAT1, LON1, LAT2, LON2, sampling_period=5, sampling_rate=1, api_token=API_TOKEN)
    assert monitor.sampling_status == "IDLE"

    # invalid API token
    with pytest.raises(ValueError):
        AQIMonitor(LAT1, LON1, LAT2, LON2, api_token="") 

    # minimum value check
    monitor = AQIMonitor(LAT1, LON1, LAT2, LON2, sampling_period=0, sampling_rate=0, api_token=API_TOKEN)
    assert monitor.sampling_period == 1  # should be at least 1
    assert monitor.sampling_rate == 1  # should be at least 1


#test station retrieval _ mocking API
@pytest.fixture
def mock_stations_api():
    #this function will check mock API response for fetching stations
    with requests_mock.Mocker() as mock:
        mock.get(f"https://api.waqi.info/map/bounds/?token={API_TOKEN}&latlng={LAT1},{LON1},{LAT2},{LON2}", json=MOCKED_STATIONS_RESPONSE)
        yield mock


def test_get_stations_in_area(mock_stations_api):
    #this functin tests retrieving stations using mocked API
    monitor = AQIMonitor(LAT1, LON1, LAT2, LON2, api_token=API_TOKEN)
    stations = monitor._get_stations_in_area()
    
    assert len(stations) == 3  # should match mock data
    assert stations == [(37.75, -122.42), (37.76, -122.41), (37.74, -122.43)]


#test PM2.5 data retrieval _ mocking API
@pytest.fixture
def mock_pm25_api():
    #mock API response for fetching PM2.5 data
    with requests_mock.Mocker() as mock:
        for station in MOCKED_STATIONS_RESPONSE["data"]:
            mock.get(f"https://api.waqi.info/feed/geo:{station['lat']};{station['lon']}/?token={API_TOKEN}", json=MOCKED_PM25_RESPONSE)
        yield mock


def test_fetch_station_pm25(mock_pm25_api):
    t#est PM2.5 retrieval with mock API
    monitor = AQIMonitor(LAT1, LON1, LAT2, LON2, api_token=API_TOKEN)
    pm25 = monitor._fetch_station_pm25(37.75, -122.42)
    
    assert pm25 == 12.4  # Should match mock data


#test handling API errors and timeouts
@pytest.fixture
def mock_api_error():
    #mock API response for failure cases
    with requests_mock.Mocker() as mock:
        mock.get(f"https://api.waqi.info/map/bounds/?token={API_TOKEN}&latlng={LAT1},{LON1},{LAT2},{LON2}", status_code=500)
        yield mock


def test_get_stations_api_error(mock_api_error):
    #test station retrieval failure
    monitor = AQIMonitor(LAT1, LON1, LAT2, LON2, api_token=API_TOKEN)
    stations = monitor._get_stations_in_area()
    
    assert stations == []  # Should return empty list on failure


#test full Sampling process
@pytest.fixture
def mock_full_api():
    #mock both station retrieval and PM2.5 fetching APIs
    with requests_mock.Mocker() as mock:
        #mck station retrieval
        mock.get(f"https://api.waqi.info/map/bounds/?token={API_TOKEN}&latlng={LAT1},{LON1},{LAT2},{LON2}", json=MOCKED_STATIONS_RESPONSE)

        #mock PM2.5 data for each station
        for station in MOCKED_STATIONS_RESPONSE["data"]:
            mock.get(f"https://api.waqi.info/feed/geo:{station['lat']};{station['lon']}/?token={API_TOKEN}", json=MOCKED_PM25_RESPONSE)

        yield mock


def test_start_sampling(mock_full_api):
    #test the full sampling process
    monitor = AQIMonitor(LAT1, LON1, LAT2, LON2, sampling_period=1, sampling_rate=1, api_token=API_TOKEN)
    
    monitor.start_sampling()
    
    assert monitor.get_status() == "DONE"
    assert monitor.get_avg_pm25() == 12.4  # Expected PM2.5 average

