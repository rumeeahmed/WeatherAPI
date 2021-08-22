# WeatherAPI

This a HTTP service that provides an API to get a weather forecast for a given city, written in `Flask` and
`OpenWeatherMap` as the data source. An API key from this service is required to use this weather service.

---

# Usage

Below are the guidelines to use this service and its endpoints.

### Ping

The `/ping` endpoint is a health check that will return basic information about the application. Below is an
example of a response.

```python
{
    "name": "weatherservice",
    "status": "ok",
    "version": "1.0.0"
}
```

### Forecast