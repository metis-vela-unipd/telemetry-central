import json
import signal
from pathlib import Path

from colorama import Fore, Style

from loggers import get_logger
from net import get_gateway
from providers import get_provider


def sigint_handler(sig, frame):
    for module in modules.values(): module.stop()
    print(f"{Fore.RED}[{__name__}] KeyboardInterrupt caught, quitting...{Fore.RESET}")
    exit(0)


modules = {}
with open(f'{Path.home()}/.telemetry/settings.json') as json_file:
    settings = json.load(json_file)

for provider in settings['providers']:
    try:
        id = provider['id']
        source_type = provider['source_type']
        sources = provider['sources']
        modules[id] = get_provider(source_type, sources, id)
        print(f"[{id}] Setup completed")
    except Exception as e:
        print(repr(e))
        if provider['essential']: raise e

for gateway in settings['net']:
    try:
        id = gateway['id']
        source = modules[gateway['source']]
        tx_rate = gateway['tx_rate']
        filters = gateway['filters']
        modules[id] = get_gateway(source, id, tx_rate, filters)
        print(f"[{id}] Setup completed")
    except Exception as e:
        print(repr(e))
        if gateway['essential']: raise e

for logger in settings['loggers']:
    try:
        id = logger['id']
        source = modules[logger['source']]
        log_rate = logger['log_rate']
        filters = logger['filters']
        modules[id] = get_logger(source, id, log_rate, filters)
        print(f"[{id}] Setup completed")
    except Exception as e:
        print(repr(e))
        if logger['essential']: raise e

print(f"{Style.BRIGHT}[main_thread] Telemetry system started (CTRL+C to stop){Style.RESET_ALL}")

signal.signal(signal.SIGINT, sigint_handler)

signal.pause()
