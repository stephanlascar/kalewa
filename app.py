import datetime
import itertools
import os
from itertools import tee

import pymongo
from flask import Flask, request, render_template

from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv('MONGODB_URI',
                                    'mongodb://heroku_h546tcch:cin7oeuho7elf7lqq3ppqu0g@ds041934.mlab.com:41934/heroku_h546tcch')
mongo = PyMongo(app)


@app.route('/')
def homepage():
    def _pairwise(iterable):
        a, b = tee(iterable)
        next(b, None)
        return zip(a, b)

    def _group(values, date_format):
        results = []
        for date, group in itertools.groupby(values, key=lambda value: value['date'].strftime(date_format)):
            items = list(group)
            results.append(dict(
                date=date,
                hchc=sum([value['hchc'] for value in items]),
                hchp=sum([value['hchp'] for value in items])
            ))

        return results

    results = []
    for previous_value, next_value in _pairwise(mongo.db.teleinfo.find().sort('date', pymongo.ASCENDING)):
        results.append(dict(
            date=next_value['date'],
            hchc=next_value['hchc'] - previous_value['hchc'],
            hchp=next_value['hchp'] - previous_value['hchp']
        ))

    results = _group(results, '%Y-%m-%dT%H:00:00')
    labels = [result['date'] for result in results]
    hchc = [result['hchc'] for result in results]
    hchp = [result['hchp'] for result in results]

    chart_data = dict(
        labels=labels,
        datasets=[
            dict(
                label='hchc',
                backgroundColor='rgb(54, 162, 235)',
                data=hchc
            ), dict(
                label='hchp',
                backgroundColor='rgb(255, 99, 132)',
                data=hchp
            )
        ]
    )

    return render_template('index.html', chart_data=chart_data)


@app.route('/api/v1/teleinfo', methods=['POST'])
def teleinfo():
    date = datetime.datetime.utcnow()
    date = date.replace(minute=0, second=0, microsecond=0)
    mongo.db.teleinfo.update(
        dict(
            date=date
        ), dict(
            hchc=int(request.json['hchc']),
            hchp=int(request.json['hchp']),
            date=date
        ), upsert=True)
    return '', 201


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
