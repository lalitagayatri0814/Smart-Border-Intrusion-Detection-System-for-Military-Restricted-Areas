import time
import random
import pandas as pd
from datetime import datetime

zones = ["Border", "Warehouse", "ControlRoom"]

while True:
    data = {
        "zone": random.choice(zones),
        "motion": round(random.uniform(0, 15), 2),
        "vibration": round(random.uniform(0, 15), 2),
        "timestamp": datetime.now()
    }

    df = pd.DataFrame([data])

    df.to_csv("sensor_data.csv", mode='a', header=not pd.io.common.file_exists("sensor_data.csv"), index=False)

    print("Generated:", data)

    time.sleep(2)    
