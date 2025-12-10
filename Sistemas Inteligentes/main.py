import pandas as pd
from passporteye import read_mrz
from datetime import datetime

mrz = read_mrz("passport.jpeg")
data = mrz.to_dict()

# features para decision tree
features = {}

features["country"] = data.get("country")


# datas convertidas
def parse_dt(d):
    if not d:
        return None
    return datetime.strptime(d, "%y%m%d").date()

dob = parse_dt(data.get("date_of_birth"))
exp = parse_dt(data.get("expiration_date"))

if dob:
    features["age"] = datetime.now().year - dob.year

if exp:
    features["days_to_expire"] = (exp - datetime.now().date()).days

# nome (estatísticas básicas)
lastname = data.get("surname", "")
firstname = data.get("given_names", "")

features["len_lastname"] = len(lastname)
features["len_firstname"] = len(firstname)
features["firstname_words"] = len(firstname.split())

print(features)
