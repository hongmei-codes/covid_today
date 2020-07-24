import pandas as pd
import folium  # to generate map
from datetime import datetime, timedelta


def get_raw_data():
    """
    This function gets daily covid-19 data from JHU
    :return: utc_date, raw_data and data_url
    """
    # get utc date
    utc_datetime = datetime.utcnow()
    utc_date = utc_datetime.strftime('%m-%d-%Y')

    # construct url
    data_url = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{utc_date}.csv'

    # try except url
    try:
        # run this code
        raw_data = pd.read_csv(data_url)
    except Exception as e:
        # run the following if there is an error
        utc_date = (utc_datetime - timedelta(days=1)).strftime('%m-%d-%Y')
        data_url = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{utc_date}.csv'
        raw_data = pd.read_csv(data_url)
    else:
        # no error? run this
        raw_data = pd.read_csv(data_url)

    # return utc_date, dataframe and url
    return utc_date, raw_data, data_url


def world_total(original_df):
    """
    This function sums up cases of confirmed, active, deaths, recovered
    all over the world.

    :param original_df: raw, unprocessed pandas dataframe
    :return: confirmed, active, deaths, recovered. all int
    """
    all_sum = original_df.sum()

    confirmed = int(all_sum['Confirmed'])
    active = int(all_sum['Active'])
    deaths = int(all_sum['Deaths'])
    recovered = int(all_sum['Recovered'])

    return confirmed, active, deaths, recovered


def top_ten(original_df):
    """
    Takes raw data and returns a list of top ten countries by confirmed cases
    :param original_df: raw, unprocessed pandas dataframe
    :return: pandas dataframe of top ten countries by confirmed cases
    """
    top_ten_table = original_df.groupby('Country_Region')\
        .sum()[['Confirmed']]\
        .sort_values(by=['Confirmed'], ascending=False)\
        .nlargest(10, 'Confirmed').to_html()

    tbody_start_index = top_ten_table.index('</thead>') + 8
    html_table_body = top_ten_table[tbody_start_index:]

    return html_table_body


def add_bubble(bubble_map, data):
    """
    Adds bubbles to map object based on data passed in.
    :param bubble_map: this is a folium Map object
    :param data: this is a list of [location name, latitude, longitude, confirmed cases]
    :returns: does not return anything
    """
    folium.Circle(location=[data[1], data[2]],
                  radius=float(data[3]) * 1,
                  popup=f'{data[0]}\nConfirmed cases: {data[3]}',
                  color='#3186cc', fill=True, fill_color='#3186cc').add_to(bubble_map)


def create_map(original_df):
    """
    This function creates a dataframe with required columns from original_df (raw data).
    The new dataframe will be used to create a bubble map chart.
    :param original_df: a pandas dataframe of raw data
    :return: folium map object
    """

    # get required data
    new_df = original_df[['Combined_Key', 'Lat', 'Long_', 'Confirmed']].dropna()

    # create folium map object
    bubble_map = folium.Map(tiles='Stamen toner')
    new_df.apply(lambda x: add_bubble(bubble_map, x), axis=1)
    html_bubble_map = bubble_map._repr_html_()

    return html_bubble_map


# if __name__ == '__main__':
#     df = pd.read_csv('covid.csv')
#     print(top_ten(df))