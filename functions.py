import csv
import datetime

def add_csv_to_mongodb(cours_collection, csv_file):
    with open(csv_file) as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]

    cours_collection.insert_many(data)

# range = day|week|month
def get_data_range(cours_collection, range):
    today = datetime.date.today()
    before_date = today
    if (range == "day"):
        before_date = today - datetime.timedelta(days=1)
    elif (range == "week"):
        before_date = today - datetime.timedelta(days=7)
    elif (range == "month"):
        before_date = today - datetime.timedelta(days=30)
        
    # get data range sorted in descending order by dates
    return list(cours_collection.find({"date": {"$gt": before_date}}).sort([('date', -1)]))

def update_stats(stats_collection, cours_collection):
    ranges = ["day", "week", "month"]
    stats = {"cours": cours_collection.name}
    for index, range in enumerate(ranges):
        data_range = get_data_range(cours_collection, range)
        stat = (data_range[0].Close - data_range[-1].Close) / data_range[-1].close * 100
        stats[range] = stat

    stats_collection.replace_one(
        {"$filter": cours_collection.name},
        stats
    )

# TODO index on date