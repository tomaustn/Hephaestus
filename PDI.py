# Built in libraries
import os
import datetime
import time
from random import randint

# External Libraries
from pyhdf import SD

# The folder 'hdf_files' contains files from NASA's Giovanni sub
# domain, specifically from the AIRS3STD dataset, which
# contains daily global measurements on a variety of different
# infomation.

# The files are stored like so:
# AIRS.2021.01.01.L3.RetStd_IR001.v7.0.4.0.G21002214203.hdf


def get_datset(dataset, date):

    YEAR = 1
    MONTH = 2
    DAY = 3

    # Iterates through the files to find one with a matching date
    for file_name in os.listdir("hdf_files"):

        data = file_name.split(".")
        if data[YEAR] != date.year:
            continue
        if data[MONTH] != date.month:
            continue
        if data[DAY] != date.day:
            continue

        # Iterates through the datasets to find a match
        hdf_file = SD.SD(file_name)
        for name in hdf_file.datasets:
            if name.lower() == dataset.lower():
                return hdf_file.select(name).get()

    raise Exception("unable to find the dataset")


def random_value(dataset):
    shape = dataset.shape()
    value = dataset[randint(0, shape[0]), randint(0, shape[1])]
    return value


class PotentialDanger:

    MIN = 80
    MAX = 126

    @staticmethod
    def index(heatindex, uvrindex, pollutionindex):
        """ Uses weights to determine the Potential Danger Index """
        return (heatindex*4 + uvrindex + pollutionindex*2)/700


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

        return heatIndex / (PotentialDanger.MAX - PotentialDanger.MIN) * 100


if __name__ == '__main__':

    date = datetime.date.fromtimestamp(time.now())
    temperature = random_value(get_datset("temperature", date))
    humidity = random_value(get_datset("humidity", date))

    heatindex = PotentialDanger.heatIndex(temperature, humidity)
