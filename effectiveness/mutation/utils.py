from pathlib import Path
from typing import List

import pandas as pd


def get_projects(path: Path) -> List[str]:
    return pd.read_csv(path)['project'].unique().str.split("/").str[1]
