import pandas as pd
from pathlib import Path

from lib import func

class Fixer:
    def __init__(self, path: Path, **kwargs):
        self.set_field_vars()
        self.build_alias_map()
        self.load_csv(path, **kwargs)
    
    def set_field_vars(self):
        self.col_map = {
            # 'ride_id': {'bikeid', 'bike_id'},
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
            'membership': {func.normalize_col(key) : val 
                        for key, val in self.membership_map.items()},
            'electric': {func.normalize_col(key) : val 
                        for key, val in self.electric_map.items()}
        }
        return self
    
    def build_alias_map(self):
        self.alias_map = {}
        for canon, variants in self.col_map.items():
            for alias in variants:
                self.alias_map[func.normalize_col(alias)] = canon
        dups = [key for key, _ in self.alias_map.items() if key in self.fields]
        if dups:
            raise ValueError(f'Aliases shadow canonical names: {alias}')
        return self
    
    def canonicalise(self, col: str) -> str:
        norm = func.normalize_col(col)
        return self.alias_map.get(norm, norm)

    def apply_bool_maps(self, df: pd.DataFrame) -> pd.DataFrame:
        for col, mapping in self.bool_maps.items():
            if col not in df.columns:
                df[col] = False
            else:
                df[col] = (
                    df[col]
                        .astype(str)
                        .str.strip()
                        .str.lower()
                        .map(mapping)
                )
        return df
    
    def add_vector_dist(self, df: pd.DataFrame, units: str = 'mi') -> pd.DataFrame:
        cols = ['lat1', 'lng1', 'lat2', 'lng2']
        points = [df[col] for col in cols]
        name = f'vector_dist_{units}'
        df[name] = func.haversine_vectorized(*points, unit = units).round(4)
        return df, name
    
    def add_duration_time(self, df: pd.DataFrame) -> pd.DataFrame:
        cols = ['start_dt', 'end_dt']
        name = 'duration_sec'
        df[name] = (df[cols[1]] - df[cols[0]]).dt.total_seconds()
        return df, name

    def load_csv(self, path: Path, **kwargs) -> pd.DataFrame:
        df: pd.DataFrame = pd.read_csv(path, **kwargs)
        df.rename(columns = lambda c: self.canonicalise(c), inplace = True)
        df['start_dt'] = pd.to_datetime(df['start_dt'])
        df['end_dt'] = pd.to_datetime(df['end_dt'])
        df = self.apply_bool_maps(df)
        df, dist_field = self.add_vector_dist(df)
        df, dur_field = self.add_duration_time(df)
        self.fields.append(dist_field)
        self.fields.append(dur_field)
        self.df = df[self.fields]
        return self


# EOF

if __name__ == '__main__':
    print('Sorry this module is not available for direct execution.')