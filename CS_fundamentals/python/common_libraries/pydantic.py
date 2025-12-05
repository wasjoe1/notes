import pydantic
from typing import Callable
from datetime import datetime
import pandas as pd

# below are model fields, pydantic.Basemodel auto generates the __init__ method based on annotated fields
class DataConfig(pydantic.BaseModel):
    shared_var = "Class variable"

    instance_var: str
    widget: str
    parser: Callable[[sqpc.Path, datetime], pd.DataFrame]

    # if i want, can still call __init__ but its overriding the __init__
    def __init__(self, **data): # **data is a kwargs
        print(data) # returns a dictionary
        print("Custom __init__ logic here")
        super().__init__(**data)  # Let Pydantic handle validation and field setting; data is executed with i.e. __init__(x=1, y=2 ...)
        print("Post-init setup")
    