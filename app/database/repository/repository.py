import numpy as np
import pandas as pd

from app.base import cache, db


class Repository(object):

    @cache.memoize(timeout=3600)
    def get_bus_station_to_pandas_(self):
        query = 'SELECT id_bus_station, city_name, state_code, label, associated_ids,population FROM bus_station WHERE enabled = 1'
        city = pd.read_sql(query, db.engine)
        city['associated_ids'].fillna('--', inplace=True)
        city['associated_ids'] = np.where(city['associated_ids'] == '', '--', city['associated_ids'])
        return city
