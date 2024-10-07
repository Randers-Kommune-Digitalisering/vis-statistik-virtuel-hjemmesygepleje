import pandas as pd

from enum import Enum
from datetime import timedelta


class Role(Enum):
    EMPLOYEE = "EMPLOYEE"
    RESIDENT = "RESIDENT"


def only_employee_to_resident(dataframe):
    if isinstance(dataframe, pd.DataFrame):
        df = dataframe
        return df[(df['caller_role'].str.upper() == Role.EMPLOYEE.value) & (df['callee_role'].str.upper() != Role.RESIDENT.value)]
    else:
        raise ValueError('Not a pandas DataFrame')


def only_answered_calls(dataframe):
    if isinstance(dataframe, pd.DataFrame):
        df = dataframe
        return df[df['duration'] > timedelta(seconds=0)]
    else:
        raise ValueError('Not a pandas DataFrame')