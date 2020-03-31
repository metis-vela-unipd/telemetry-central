#  Copyright (c) 2020 Matteo Carnelos.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from sensors_provider import SensorsProvider
from webapp import Webapp
from colorama import Fore, Style
from logger import Logger

# Start the data provider thread (actually is only the gpsd thread)
provider = SensorsProvider()
provider.start()

# Start the logger thread
logger = Logger(provider)
logger.start()

# Start the web thread
webapp = Webapp(provider, logger)
webapp.start()

# Wait until all the threads have finished initializing (or exit after timeout)
provider.end_setup.wait(timeout=20)
webapp.end_setup.wait(timeout=20)
logger.end_setup.wait(timeout=20)

if not provider.end_setup.isSet() or \
   not webapp.end_setup.isSet() or \
   not logger.end_setup.isSet():
    print(f"{Fore.RED}[main_thread] Something went wrong during threads initialization, quitting...{Fore.RESET}")
    logger.stop_log()
    exit(1)

# Wait all threads to start
print(f"{Style.BRIGHT}[main_thread] Telemetry system started (CTRL+C to stop){Style.RESET_ALL}")

# DEVELOPMENT ONLY
# import logging
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)
# webapp.socket.run(webapp.app, host='0.0.0.0', port=8080, debug=True)

# Watch threads and try recovery when needed, terminate program when KeyboardInterrupt is caught
while True:
    try:
        if not provider.is_alive():
            print(f"{Fore.YELLOW}[main_thread] Provider dead, attempting recovery...{Fore.RESET}")
            provider = SensorsProvider()
            provider.start()
            provider.end_setup.wait(timeout=20)
            if provider.end_setup.isSet():
                webapp.provider = provider.get_sensor('gps')
                print(f"{Fore.GREEN}[main_thread] Done recovery!{Fore.RESET}")
            else:
                print(f"{Fore.RED}[main_thread] Recovery failed, quitting...{Fore.RESET}")
                logger.stop_log()
                exit(1)
    except KeyboardInterrupt:
        print(f"{Fore.RED}[main_thread] KeyboardInterrupt caught, quitting...{Fore.RESET}")
        logger.stop_log()
        break
