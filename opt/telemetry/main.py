from gpsd import Gpsd
from dashboard import Dashboard

# Start the data provider thread (actually is only the gpsd thread)
provider = Gpsd()
provider.start()

# Start the dashboard thread
dashboard = Dashboard(provider)
dashboard.start()

# Wait until all the threads have finished initializing (or exit after timeout)
provider.end_setup.wait(timeout=20)
dashboard.end_setup.wait(timeout=20)

if not provider.end_setup.isSet() or not dashboard.end_setup.isSet():
    print("[main_thread] Something went wrong during threads initialization, quitting...")
    exit()

# Wait all threads to start
print("[main_thread] Telemetry system started")

# Watch threads and try recovery when needed, terminate program when KeyboardInterrupt is caught
while True:
    try:
        if not provider.is_alive():
            print("[main_thread] Provider dead, attempting recovery...")
            provider = Gpsd()
            provider.start()
            provider.end_setup.wait(timeout=20)
            if provider.end_setup.isSet():
                dashboard.provider = provider
                print("[main_thread] Done recovery")
            else:
                print("[main_thread] Recovery failed, quitting...")
                exit()
    except KeyboardInterrupt:
        print("[main_thread] KeyboardInterrput caught, quitting...")
        break
