import re
import pandas as pd
import numpy as np
from pathlib import Path
from collections.abc import Callable
from typing import Union, Literal


def haversine_vectorized(lat1: pd.Series, lng1: pd.Series, lat2: pd.Series, lng2: pd.Series, unit = 'km' | 'mi') -> pd.Series:
    lat1, lng1, lat2, lng2 = map(np.radians, [lat1, lng1, lat2, lng2])
    delta_lat = lat2 - lat1
    delta_lng = lng2 - lng1
    a = (np.sin(delta_lat / 2.0)) ** 2 + np.cos(lat1) * np.cos(lat2) * (np.sin(delta_lng / 2.0)) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    if unit == 'km':
        R = 6371
    elif unit == 'mi':
        R = 3959
    result: pd.Series
    result = R * c
    return result

###################################C##############

def normalize_col(col: str) -> str:
    col = col.strip().lower()
    col = re.sub(r'[.\s\-]+','_', col)
    col = re.sub(r'[^\w_]', '', col)
    return col

#################################################

class Fixer:
    def __init__(self, path: Path, **kwargs):
        self.set_field_vars()
        self.build_alias_map()
        self.load_csv(path, **kwargs)
    
    def set_field_vars(self):
        self.col_map = {
            'membership': {'member_casual', 'usertype', 'user_type'}
            ,'electric': {'rideable_type'}
            ,'start_dt': {'started_at', 'starttime', 'start_time'}
            ,'end_dt': {'ended_at', 'stoptime', 'stop_time'}
            ,'start_station': {'start_station_name'}
            ,'end_station': {'end_station_name'}
            ,'lat1': {'start_station_latitude', 'start_station_lat', 'start_lat'}
            ,'lng1': {'start_station_longitude', 'start_station_lng', 'start_lng'}
            ,'lat2': {'end_station_latitude', 'end_station_lat', 'end_lat'}
            ,'lng2': {'end_station_longitude', 'end_station_lng', 'end_lng'}
        }
        self.fields = list(self.col_map.keys())
        self.membership_map = {
            'casual': False, 'member': True,
            'customer': False, 'subscriber': True
        }
        self.electric_map = {'classic_bike': False, 'electric_bike': True}
        self.bool_maps = {
            'membership': {normalize_col(key) : val 
                        for key, val in self.membership_map.items()},
            'electric': {normalize_col(key) : val 
                        for key, val in self.electric_map.items()}
        }
        return self
    
    def build_alias_map(self):
        self.alias_map = {}
        for canon, variants in self.col_map.items():
            for alias in variants:
                self.alias_map[normalize_col(alias)] = canon
        dups = [key for key, _ in self.alias_map.items() if key in self.fields]
        if dups:
            raise ValueError(f'Aliases shadow canonical names: {alias}')
        return self
    
    def canonicalise(self, col: str) -> str:
        norm = normalize_col(col)
        return self.alias_map.get(norm, norm)

    def apply_bool_maps(self) -> pd.DataFrame:
        for col, mapping in self.bool_maps.items():
            if col not in self.df.columns:
                self.df[col] = False
            else:
                self.df[col] = (
                    self.df[col]
                        .astype(str)
                        .str.strip()
                        .str.lower()
                        .map(mapping)
                )
        return self
    
    def add_vector_dist(self, units: str = 'mi') -> pd.DataFrame:
        cols = ['lat1', 'lng1', 'lat2', 'lng2']
        points = [self.df[col] for col in cols]
        name = f'dist_{units}'
        self.df[name] = haversine_vectorized(*points, unit = units).round(4)
        self.fields.append(name)
        return self
    
    def add_duration_time(self) -> pd.DataFrame:
        cols = ['start_dt', 'end_dt']
        name = 'duration_sec'
        self.df[name] = (self.df[cols[1]] - self.df[cols[0]]).dt.total_seconds()
        self.fields.append(name)
        return self

    def load_csv(self, path: Path, **kwargs) -> pd.DataFrame:
        self.df: pd.DataFrame = pd.read_csv(path, **kwargs)
        self.df.rename(columns = lambda c: self.canonicalise(c), inplace = True)
        self.df['start_dt'] = pd.to_datetime(self.df['start_dt'])
        self.df['end_dt'] = pd.to_datetime(self.df['end_dt'])
        self.apply_bool_maps()
        self.add_vector_dist()
        self.add_duration_time()
        self.df = self.df[self.fields].dropna(how = 'any')
        return self

    def view_per_station(
            self
            ,view: Literal['dist_mi', 'duration_sec'] = None
            ,agg_func: Callable[[pd.Series], Union[int, float]] = pd.Series.sum
        ) -> pd.Series:
        if view is None:
            view = 'dist_mi'
        per_startStation = pd.DataFrame(self.df.groupby('start_station')[view].agg(agg_func))
        per_endStation = pd.DataFrame(self.df.groupby('end_station')[view].agg(agg_func))
        per_station = \
            per_startStation.merge(per_endStation, how = 'outer', left_index = True, right_index = True).fillna(0)
        
        per_station[f'{view}'] = per_station[f'{view}_x'] + per_station[f'{view}_y']
        return_frame = per_station[f'{view}']
        return_frame.index.name = 'station'
        return return_frame.reset_index()

    def temporal_summary(
            self
            ,dt_field: Literal['start_dt', 'end_dt'] = 'start_dt'
            ,freq: Literal['min', 'h', 'D', 'ME', 'YE'] = 'D'
            ,agg_func: Callable[[pd.Series], Union[int, float]] = [pd.Series.sum, pd.Series.mean]
            ,agg_map: dict[str, Callable[[pd.Series], Union[int, float]]] = None
        ) -> pd.DataFrame:
        df = self.df.copy()
        df = df.set_index(dt_field)
        if agg_map is None:
            agg_map = {}
            if 'duration_sec' in df.columns:
                agg_map['duration_sec'] = agg_func
            if any(col.startswith('dist_') for col in df.columns):
                for col in [c for c in df.columns if c.startswith('dist_')]:
                    agg_map[col] = agg_func
            if 'membership' in df.columns:
                agg_map['membership'] = agg_func[0]
            if 'electric' in df.columns:
                agg_map['electric'] = agg_func[0]
            if not agg_map:
                agg_map = {'start_dt': pd.Series.count}
        summary = df.resample(freq).agg(agg_map)
        summary.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in summary.columns.values]
        return summary.reset_index().fillna(0)

# EOF

if __name__ == '__main__':
    print('Sorry this module is not available for direct execution.')