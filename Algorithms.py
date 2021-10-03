 # DONE heat index
# DONE heat variation
# DONE PM 2.5
# DONE PM 10
# TODO average heat
# TODO estimated heat over time (predicted temperature)
ultravioletRange = 0
previousUltraviolet = 0

class DangerRating:

    # Heat stress defined from a scale of 1-10
    #lists for api
    heatStressRating = list()  # Unused
    heatVariation = list()  # Unused

    PM25 = list()
    PM10 = list()

    rating = list()

    MIN = 80  #bottom floor for danger rating (anything below is 0)
    MAX = 126  #upper floor for danger rating (= or above is 10/10)

    @staticmethod
    def heatIndex(airTemperature, relativeHumidity):
        """ Provides a danger rating based on the heat factor """

        # FORMULA heat index = -42.379 + 2.04901523*T + 10.14333127*RH - .22475541*T*RH - .00683783*T*T - .05481717*RH*RH + .00122874*T*T*RH + .00085282*T*RH*RH - .00000199*T*T*RH*RH
        heatIndex = (
            (-42.379) + (2.049015230) * airTemperature +
            (10.14333127) * relativeHumidity -
            (0.22475541) * airTemperature * relativeHumidity -
            (6.837839 * 10**-3) * airTemperature**2 -
            (5.481717 * 10**-2) * relativeHumidity**2 +
            (1.22874 * 10**-3) * airTemperature**2 * relativeHumidity +
            (8.52820 * 10**-4) * airTemperature * relativeHumidity**2 -
            (1.99 * 10**-6) * airTemperature**2 * relativeHumidity**2
        )  

        # FORMULA correction factor = (13 - RH)/4 * SQRT(17 - ABS(T - 95)/17)
        if airTemperature <= 112 and airTemperature >= 80 and relativeHumidity <= 13:
            heatIndex += -(13 - relativeHumidity) / 4 * (
                (17 - airTemperature - 95) / 17)**0.5
        elif airTemperature <= 87 and airTemperature >= 80 and relativeHumidity > 85:
            heatIndex += (relativeHumidity - 85) * (87 - airTemperature) * 0.02

        if heatIndex <= DangerRating.MIN:
            return 0
        elif heatIndex >= DangerRating.MAX:
            return 10

        return ((heatIndex - 80) * 100) / (DangerRating.MAX -
                                           DangerRating.MIN) / 10

    @staticmethod
    def temperatureChange(firstTemperature, secondTemperature):
        """ Provides the % change between two temperatures """

        return (secondTemperature - firstTemperature) / firstTemperature * 100

    @staticmethod
    def ultravioletRiskFactor():
      if ultravioletRange >= 10 or ultravioletRange < (1.3*(previousUltraviolet)):
        return(ultravioletRange)
        print("Dangerous exposure.")


        if __name__ == '__main__':
            print(DangerRating.heatIndex(90, 60))


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


# Returns temperature changed - change current and previous temp to nasa data list - tbd
def temperatureChange():
    currentTemperature = 10  #scrape this data

    previousTemperature = 20  #scrape this too

    percentageChange = DangerRating.temperatureChange(previousTemperature,
                                                      currentTemperature)

    print(f"Temperature has changed by {percentageChange}% during this period")
