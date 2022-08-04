
from pydantic import BaseModel


class DataGeneratorCall(BaseModel):
    xMin: float
    xMax: float
    yMin: float
    yMax: float
    pointsAction: str
    numVals: int
    interp: str
    style: str
    pointValues: list


class DataGeneratorResult(BaseModel):
    data: list
    curveValues: list
