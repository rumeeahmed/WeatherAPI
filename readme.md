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

This endpoint will return the weather condition for a given city by specifying the city as `forecast/London`
and will provide the next available forecast.

The units in the data returned can be configured through the optional `unit` query params, the default is 
`standard` which returns data in Kelvin, `metric` which returns data in Celsius and `imperial` which returns
data in Fahrenheit.

A date and datetime can be specified to query the weather, this must follow from 3 hour increment starting 
from 12pm. It will accept a date, a naive datetime and an aware datetime.