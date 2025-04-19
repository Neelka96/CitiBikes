from .fixer import Fixer
from .func import df_size, iter_subfiles

import pandas as pd
from pathlib import Path
from typing import Literal
from concurrent.futures import ProcessPoolExecutor, as_completed
from os import cpu_count

_cpus = cpu_count()
files = [f for year in range(2013, 2026) for f in iter_subfiles(year)]

def process_file(file: Path, attr: str | list[str], **kwargs) -> pd.DataFrame | list[pd.DataFrame]:
    fix = Fixer(file, low_memory = False)
    fetch = getattr(fix, attr)
    if callable(fetch):
        fetch = fetch(**kwargs)
    return fetch

def unify_temporal_summaries(agg_list: list, dt_field: str):
    return (
        pd
            .concat(agg_list, ignore_index = True)
            .groupby(str(dt_field)).sum()
            .reset_index()
    )

def unify_station_views(agg_list: list):
    return (
        pd
            .concat(agg_list)
            .groupby('station').sum()
            .reset_index()
    )

def concurrent_agg(
        table_name: Literal['temporal_summary', 'view_per_station']
        ,save_file: Path
        ,max_workers: int | None = None
        ,**kwargs
    ) -> pd.DataFrame:
    if max_workers and max_workers > _cpus: raise RuntimeError(f'Max workers cannot be set past CPU count: {_cpus}')
    agg_list = []
    with ProcessPoolExecutor(max_workers = max_workers) as exec:
        futures = {exec.submit(process_file, f, table_name, **kwargs) : f for f in files}
        for future in as_completed(futures):
            agg_list.append(future.result())
    if table_name == 'temporal_summary':
        dt_field = kwargs.get('dt_field', 'start_dt')
        unify_temporal_summaries(agg_list, dt_field)
    elif table_name == 'view_per_station':
        agg_df = unify_station_views(agg_list)
    agg_df.to_csv(save_file, header = True, index = False)
    df_size(agg_df)
    return agg_df

# EOF

if __name__ == '__main__':
    print('Sorry this module is not available for direct execution.')