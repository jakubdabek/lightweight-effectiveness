from pathlib import Path
from typing import List

import pandas as pd


def get_projects(path: Path) -> List[str]:
    return pd.read_csv(path)['project'].str.split("/").str[1].unique().tolist()
