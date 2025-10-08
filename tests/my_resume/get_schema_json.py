from datetime import datetime

now = datetime.now()
abbreviated_month = now.strftime('%b')
print("Abbreviated month:", abbreviated_month)
print(now.strftime("%b"))  # Month name, e.g., "October"
print(now.strftime("%Y"))  # Full year, e.g., "2025"
