from flask import Flask, render_template
from data import get_raw_data, world_total, top_ten, create_map

app = Flask(__name__)


@app.route('/')
def home():
    utc_date, raw_data, data_url = get_raw_data()
    confirmed, active, deaths, recovered = world_total(raw_data)
    top_tbody = top_ten(raw_data)
    bubble_map = create_map(raw_data)

    return render_template('index.html', utc_date=utc_date, data_url=data_url,
                           confirmed=confirmed, active=active, deaths=deaths, recovered=recovered,
                           top_tbody=top_tbody,
                           bubble_map=bubble_map)


if __name__ == '__main__':
    app.run()
