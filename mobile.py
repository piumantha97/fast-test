from pydantic import BaseModel
# 2. Class which describes Bank Notes measurements
class Mobile(BaseModel):
    Gender: int
    Age: int
    Education: int
    Occupation: int
    District: int
    CameraSatisfaction: int
    MemorySatisfaction: int
    PerformanceSatisfaction: int
    BatterySatisfaction: int
    spend_amount: int
    Education_purpose: int
    Entertaintment_purpose: int
    Gaming_purpose: int
    Occupation_purpose: int
    Photography_purpose: int
    Socializing_purpose: int