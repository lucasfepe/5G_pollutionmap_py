# 5G Pollution Map API

A **FastAPI-based service** that provides real-time and predictive air pollution data analysis. This project combines pollution measurements with advanced data processing to deliver insights about air quality trends and forecasts.

---

## 🌟 Features

- **Real-time Pollution Data**  
  Fetches current pollution measurements from the OpenAQ API.

- **Multi-pollutant Analysis**  
  Handles multiple pollutants (CO, PM2.5, NO2, O3, etc.)

- **Time Series Processing**
  - Hourly data resampling
  - Linear interpolation for missing values
  - Historical pattern analysis

- **Predictive Analytics**
  - Linear regression-based trend analysis
  - Daily pattern incorporation
  - 5-day pollution forecasts

- **Statistical Analysis**
  - Mean and standard deviation calculations
  - Min/max value tracking
  - Trend direction identification
  - Percentage change analysis

---

## 🛠 Technical Stack

- **Framework**: FastAPI  
- **Data Processing**:
  - `pandas` for time series manipulation and data structuring  
  - `numpy` for numerical computations  
  - `scikit-learn` for linear regression  
- **Data Source**: OpenAQ API  
- **Data Caching**: Local file system  

---

## 📦 Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/5G_pollutionmap_py.git
    cd 5G_pollutionmap_py
    ```

2. **Create and activate a virtual environment**:

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:

    Create a `.env` file with the following:

    ```env
    OPENAQ_API_KEY=your_api_key_here
    ```

---

## 🚀 Usage

1. **Start the server**:

    ```bash
    python main.py
    ```

2. **Access the API endpoints**:

    - Latest pollution data:  
      ```
      /api/v1/latest/{city}
      ```

    - Pollution forecast:  
      ```
      /api/v1/forecast/{city}
      ```

---

## 📡 API Endpoints

### `GET /api/v1/latest/{city}`

Returns the most recent pollution measurements for the specified city.

---

### `GET /api/v1/forecast/{city}`

Returns:
- Historical data analysis
- 5-day pollution predictions
- Statistical trends and patterns

---

## 🔄 Data Processing Pipeline

1. **Data Collection**
   - Fetches data from the OpenAQ API
   - Implements local file caching for performance optimization

2. **Data Processing**
   - Structures raw data into `pandas` DataFrames
   - Organizes multiple pollutants using pivot tables
   - Resamples data to hourly intervals
   - Interpolates missing values

3. **Predictive Analysis**
   - Applies linear regression for trend estimation
   - Incorporates historical daily patterns
   - Generates pollutant-specific forecasts

4. **Statistical Analysis**
   - Calculates key metrics per pollutant
   - Identifies trends and variations
   - Computes percentage changes over time

---

Enjoy exploring air quality trends with predictive power! 🌍📊
