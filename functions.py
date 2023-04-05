import csv
import datetime
import pymongo

client = pymongo.MongoClient('mongodb+srv://root:KDjt96Njs72Lp4c0@cluster0.3txvxzn.mongodb.net/test')
db = client['projet-bourse']

def add_csv_to_mongodb(db, cours, csv_file):
    db[cours].drop()
    db[cours].create_index([("Date", pymongo.DESCENDING)])

    with open(csv_file) as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
        db[cours].insert_many(data)

# range = day|week|month
def get_data_range(db, cours, range):
    today = datetime.datetime.today()
    start_date = today
    if (range == "day"):
        start_date = today - datetime.timedelta(days=2)
    elif (range == "week"):
        start_date = today - datetime.timedelta(days=8)
    elif (range == "month"):
        start_date = today - datetime.timedelta(days=31)
        
    # get data range sorted in descending order by dates
    return list(db[cours].find({"Date": {"$gt": str(start_date)}}).sort([('date', -1)]))

def update_stats(db, cours):
    ranges = ["day", "week", "month"]
    stats = {"cours": db[cours].name}
    for range in ranges:
        data_range = get_data_range(db, cours, range)
        current_day_close = float(data_range[0]["Close"])
        last_day_close = float(data_range[-1]["Close"])
        stat = (current_day_close - last_day_close) / last_day_close * 100
        stats[range] = stat

    db["stats"].replace_one(
        {"cours": db[cours].name},
        stats,
        upsert=True
    )

def delete_collection(db, cours):
    db[cours].drop()
    db["stats"].delete_one({"cours": cours})
