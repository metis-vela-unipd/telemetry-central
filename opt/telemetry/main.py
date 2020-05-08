from provider import SensorProvider
from colorama import Fore, Style
from logger import Logger
from lora import LoraTransceiver


# Start the sensors provider thread
provider = SensorProvider()
provider.start()

# Start the logger thread
logger = Logger(provider)
logger.start()

# Start the lora transceiver thread
lora = LoraTransceiver(provider)
lora.start()

# Wait until all the threads have finished initializing (or exit after timeout)
provider.end_setup.wait(timeout=20)
logger.end_setup.wait(timeout=20)
lora.end_setup.wait(timeout=20)

if not provider.end_setup.isSet() or not logger.end_setup.isSet() or not lora.end_setup.isSet():
    print(f"{Fore.RED}[main_thread] Something went wrong during threads initialization, quitting...{Fore.RESET}")
    exit(1)

# Wait all threads to start
print(f"{Style.BRIGHT}[main_thread] Telemetry system started (CTRL+C to stop){Style.RESET_ALL}")

while True:
    try: pass
    except KeyboardInterrupt:
        print(f"{Fore.RED}[main_thread] KeyboardInterrupt caught, quitting...{Fore.RESET}")
        exit(0)
