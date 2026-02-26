import pathway as pw

schema = pw.schema_from_csv("sensor_data.csv")

table = pw.io.csv.read("sensor_data.csv", schema=schema)

result = table.select(
    timestamp=pw.this.timestamp,
    motion=pw.this.motion,
    vibration=pw.this.vibration,
    anomaly=(pw.this.motion > 10) | (pw.this.vibration > 10)
)

pw.io.csv.write(result, "output.csv")

pw.run()
