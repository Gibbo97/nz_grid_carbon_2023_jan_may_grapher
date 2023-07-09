import csv
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt, dates as mdates
import datetime

path = '/Users/jack/Documents/grid_carbon/'
files = {'January': '202301_Generation_MD.csv', 'February': '202302_Generation_MD.csv',
         'March': '202303_Generation_MD.csv', 'April': '202304_Generation_MD.csv',
         'May': '202305_Generation_MD.csv'}

x_values = [datetime.datetime.fromtimestamp(1800 * td - 3600*12) for td in range(1, 48)]


def find_plant_carbon_intensity(gen_code, fuel_code):
    zero_carbon_fuels = ['Hydro', 'Wind']
    plant_carbon_table = {'glenbrook_kilns': 0, 'huntly_1_4': 0.9955, 'huntly_e3p': 0.405, 'huntly_p40': 0.405,
                          'whareroa': 0.502,
                          'junctionroad': 0.567, 'kawerau': 0.060, 'norskeskog': 0.060, 'kawerau_new': 0.123,
                          'kinleith': 1.092, 'ngawha': 0.307, 'kapuni': 0.502, 'McKee': 0.567, 'nap': 0.063,
                          'Ngatamariki': 0.064, 'ohaaki': 0.341, 'poihipi': 0.036, 'stratford': 0.573,
                          'southdown': 0,
                          'te_mihi': 0.045, 'te_rapa': 0.573, 'whirinaki': 0.766, 'mokai': 0.052, 'rotokawa': 0.084,
                          'tehuka': 0.055, 'wairakei': 0.021}

    if fuel_code in zero_carbon_fuels:
        return 0
    else:
        return plant_carbon_table[gen_code]


monthly_trading_period_averages = {}

for month in files:
    with open(path + files[month]) as electricity:
        csv_reader = csv.reader(electricity, delimiter=',')

        total_carbon_tp = [0] * 48
        total_kwh_tp = [0] * 48

        for row in csv_reader:
            if row[0] == 'Site_Code':
                continue
            plant_carbon_intensity = find_plant_carbon_intensity(row[3], row[4])

            for tp in range(0, 48):
                trading_period_generation = int(row[tp + 7])
                total_kwh_tp[tp] += trading_period_generation
                total_carbon_tp[tp] += trading_period_generation * plant_carbon_intensity

        grams_carbon_per_kwh_per_tp = []
        for i in range(len(total_carbon_tp) - 1):
            grams_carbon_per_kwh_per_tp.append(total_carbon_tp[i] / total_kwh_tp[i] * 1000)

        monthly_trading_period_averages[month] = grams_carbon_per_kwh_per_tp
    # plotting the points

for month in monthly_trading_period_averages:
    plt.plot(x_values, monthly_trading_period_averages[month], label=month)

plt.xlabel('Trading Period Ended')
plt.ylabel('CO2 g/kwh')
plt.title('New Zealand Electricity Emissions 2023\nMonthly Average By Time of Day')
plt.legend()
plt.xticks(rotation=90)
ax = plt.gca()
formatter = mdates.DateFormatter("%H:%M")
ax.xaxis.set_major_formatter(formatter)


plt.ylim((0, 100))

plt.show()
