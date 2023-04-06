import csv
import datetime
import pymongo
import pandas as pd
from datetime import timezone
import datetime

client = pymongo.MongoClient('mongodb+srv://root:KDjt96Njs72Lp4c0@cluster0.3txvxzn.mongodb.net/test')
db = client['projet-bourse']

def add_csv_to_mongodb(cours, csv_file):
    db[cours].drop()
    db[cours].create_index([("Date", pymongo.ASCENDING)])

    with open(csv_file) as file:
        reader = csv.DictReader(file)
        data = []
        for row in reader:
            format_string = '%Y-%m-%d %H:%M:%S%z'
            date = datetime.datetime.strptime(row["Date"], format_string).replace(tzinfo=datetime.timezone.utc)
            row["Date"] = date
            data.append(row)
        db[cours].insert_many(data)

# range = day|week|month|year
def get_data_range(cours, range):
    today = datetime.datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    start_date = today
    if (range == "day"):
        start_date = today - datetime.timedelta(days=2 + 1)
        print(start_date)
    elif (range == "week"):
        start_date = today - datetime.timedelta(days=8 + 1)
    elif (range == "month"):
        start_date = today - datetime.timedelta(days=32 + 1)
    elif (range == "year"):
        start_date = today - datetime.timedelta(days=366 + 1)

    # get data range sorted in descending order by dates
    return list(db[cours].find({"Date": {"$gt": start_date}}).sort([('Date', -1)]))

def get_data(cours):
    return pd.DataFrame(db[cours].find().sort([('Date', 1)]))

def update_stats(cours, name):
    ranges = ["day", "week", "month", "year"]
    stats = {"cours": cours, "name": name}
    # TODO faire ci-dessous en mongodb
    for range in ranges:
        data_range = get_data_range(cours, range)
        current_day_close = float(data_range[0]["Close"])
        last_day_close = float(data_range[-1]["Close"])
        stat = round(current_day_close - last_day_close, 4)
        stat_percentage = round((current_day_close - last_day_close) / last_day_close * 100, 4)
        stats[range] = stat
        stats[range + "_percent"] = stat_percentage

    db["stats"].replace_one(
        {"cours": cours},
        stats,
        upsert=True
    )

def delete_collection(cours):
    db[cours].drop()
    db["stats"].delete_one({"cours": cours})

def get_stats():
    return pd.DataFrame(db["stats"].find())
