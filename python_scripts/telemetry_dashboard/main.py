from gpsd import Gpsd
from dashboard import Dashboard

# Start the data provider thread (actually is only the gpsd thread)
provider = Gpsd()
provider.start()

# Start the dashboard thread
dashboard = Dashboard(provider)
dashboard.start()

# Watch threads and try recovery when needed, terminate program when KeyboardInterrupt is caught
while True:
    try:
        if not provider.is_alive():
            print("[main_thread] Provider dead, attempting recovery...")
            provider = Gpsd()
            provider.start()
            dashboard.provider = provider
    except KeyboardInterrupt:
        print("[main_thread] KeyboardInterrput caught.")
        break
