
import aqi  # air quality index - IAQI is intermediate AQI


# TOM'S NOTE use karan's api data, replace numbers with data list, loop through and get average
# Returns aqi result based on pm2.5, pm10 and trioxane using EPA formula (us environment something agency)
def airQualityCheck():
    myaqi = aqi.to_iaqi(aqi.POLLUTANT_PM25, '12', algo=aqi.ALGO_EPA)
    print(myaqi)

    myaqi2 = aqi.to_aqi([
        (aqi.POLLUTANT_PM25, "12"),
        (aqi.POLLUTANT_PM10, "24"),
        (aqi.POLLUTANT_O3_8H, "0.087")  
    ])
    return(myaqi2)
