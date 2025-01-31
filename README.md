```markdown
# 🌍 AQIMonitor - Air Quality Monitoring in Python

AQIMonitor is a **lightweight and efficient Python module** that fetches and averages **PM2.5 air pollution data** from AQICN's API.  
It allows users to sample air quality data from multiple monitoring stations within a **specified geographical area**.

---

## ✨ Features

✔️ Fetch **real-time PM2.5** data from AQICN API  
✔️ Dynamically retrieve **all monitoring stations** in a given area  
✔️ Supports **custom sampling periods** and **sampling rates**  
✔️ Implements **robust error handling & logging**  
✔️ Includes **unit tests using `pytest`**  

---

## 📥 Installation

To install AQIMonitor, clone the repository and install dependencies:

```
git clone https://github.com/SamanHmd/aqi_monitor.git
cd aqi_monitor
pip install -r requirements.txt
```

Or install it directly from GitHub:

```
pip install git+https://github.com/SamanHmd/aqi_monitor.git
```

---

## 🚀 Quick Start

### 1️⃣ Initialize AQIMonitor

```
from aqi_monitor import AQIMonitor

aqi_monitor = AQIMonitor(
    latitude_1=37.78, longitude_1=-122.45,  
    latitude_2=37.70, longitude_2=-122.35, 
    sampling_period=5,  # Minutes
    sampling_rate=1,  # Samples per minute
    api_token="YOUR_API_TOKEN"  # Replace with a valid AQICN API token
)
```

### 2️⃣ Start Sampling

```
aqi_monitor.start_sampling()
```

### 3️⃣ Check Sampling Status

```
print(aqi_monitor.get_status())  # Expected Output: "RUNNING" → "DONE"
```

### 4️⃣ Get Final PM2.5 Average

```
print(aqi_monitor.get_avg_pm25())  # Example Output: 14.7 µg/m³
```

---

## 🧪 Running Tests

To run unit tests, execute:

```
pytest test_aqi_monitor.py -v
```

---

## ⚠️ Error Handling

AQIMonitor is designed to handle API failures and timeouts gracefully, using:

- 🔄 **Automatic retry logic**
- ⚠️ **Logging warnings for missing data**
- 🛑 **Fallback handling when no stations are found**

---

## 🤝 Contributing

We welcome contributions! To get started:

1️⃣ **Fork** the repository  
2️⃣ **Create** a new feature branch (`git checkout -b feature-branch`)  
3️⃣ **Commit** your changes (`git commit -m "Add new feature"`)  
4️⃣ **Push** to your branch (`git push origin feature-branch`)  
5️⃣ **Submit** a Pull Request ✅  

---

## 📜 License

📝 AQIMonitor is licensed under the **MIT License**. See `LICENSE` for more details.

---

## ⭐ Support the Project
If you find this project useful, **consider giving it a star ⭐ on GitHub**.  
```
