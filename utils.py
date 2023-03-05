import csv
import json
import os
import time

import django

from Homework31_Django_Validators_Tests.settings import US_CSV, ADS_CSV, LOC_CSV, \
    CAT_CSV, LOC_JSON, US_JSON, ADS_JSON, CAT_JSON, BASE_DIR
from django.contrib.auth.hashers import make_password


# ----------------------------------------------------------------
# setup env settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Homework31_Django_Validators_Tests.settings')
django.setup()


# ----------------------------------------------------------------
# convert csv to json function
def convert_csv_json(csv_file, json_file, model):
    """
    Function to convert csv files to json files
    :param csv_file: csv file
    :param json_file: json file
    :param model: model
    :return: None
    """
    data_list: list = []

    with open(csv_file, encoding="utf-8") as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            if 'location_id' in row:
                row['locations'] = [int(row['location_id'])]
                del row['location_id']
            if 'password' in row:
                row['password'] = make_password(row['password'])
            if row.get('is_published') is not None:
                if row['is_published'] == 'TRUE':
                    row["is_published"] = True
                else:
                    row["is_published"] = False

            data_dict: dict = {"model": model, "pk": row["id"], "fields": row}
            data_list.append(data_dict)
    with open(json_file, "w", encoding="utf-8") as json_file:
        json_file.write(json.dumps(data_list, indent=4, ensure_ascii=False))


# ----------------------------------------------------------------
# call function to convert datasets to fixtures
convert_csv_json(LOC_CSV, LOC_JSON, 'locations.location')
convert_csv_json(US_CSV, US_JSON, 'authentication.user')
convert_csv_json(ADS_CSV, ADS_JSON, "ads.advertisement")
convert_csv_json(CAT_CSV, CAT_JSON, "ads.category")


# ----------------------------------------------------------------
# run postgres container
time.sleep(2)
print(f'----------------------------------------------------------------\n'
      f'STARTING POSTGRES CONTAINER...\n'
      f'----------------------------------------------------------------')
time.sleep(2)
os.system('docker run --name Homework31_Django_Validators_Tests_postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres')


# ----------------------------------------------------------------
# migrations
time.sleep(2)
print('----------------------------------------------------------------\n'
      'MIGRATIONS...\n'
      '----------------------------------------------------------------')
time.sleep(2)
os.system(f'cd {BASE_DIR} && ./manage.py makemigrations')
os.system(f'cd {BASE_DIR} && ./manage.py migrate')


# ----------------------------------------------------------------
# load data to database
time.sleep(2)
print(f'----------------------------------------------------------------\n'
      f'LOADING DATA TO DATABASE...\n'
      f'----------------------------------------------------------------')
time.sleep(2)
os.system(f'cd {BASE_DIR} '
          f'&& ./manage.py loaddata fixtures/category.json'
          f'&& ./manage.py loaddata fixtures/location.json'
          f'&& ./manage.py loaddata fixtures/user.json'
          f'&& ./manage.py loaddata fixtures/ad.json'
          )


# ----------------------------------------------------------------
# run server
time.sleep(2)
print(f'----------------------------------------------------------------\n'
      f'RUNNING SERVER...\n'
      f'----------------------------------------------------------------')
time.sleep(2)
os.system(f'cd {BASE_DIR} && ./manage.py runserver')
