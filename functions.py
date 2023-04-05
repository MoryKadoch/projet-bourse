import csv
import datetime

def add_csv_to_mongodb(cours_collection, csv_file):
    with open(csv_file) as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
        cours_collection.insert_many(data)

# range = day|week|month
def get_data_range(cours_collection, range):
    today = datetime.datetime.today()
    start_date = today
    if (range == "day"):
        start_date = today - datetime.timedelta(days=2)
    elif (range == "week"):
        start_date = today - datetime.timedelta(days=8)
    elif (range == "month"):
        start_date = today - datetime.timedelta(days=31)
        
    # get data range sorted in descending order by dates
    return list(cours_collection.find({"Date": {"$gt": str(start_date)}}).sort([('date', -1)]))

def update_stats(stats_collection, cours_collection):
    ranges = ["day", "week", "month"]
    stats = {"cours": cours_collection.name}
    for range in ranges:
        data_range = get_data_range(cours_collection, range)
        current_day_close = float(data_range[0]["Close"])
        last_day_close = float(data_range[-1]["Close"])
        stat = (current_day_close - last_day_close) / last_day_close * 100
        stats[range] = stat

    stats_collection.replace_one(
        {"cours": cours_collection.name},
        stats,
        upsert=True
    )

# TODO index on date