from time import sleep
from datetime import datetime
import psutil
from sys import platform
import csv
import logging


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


def run(interval, output):
    try:
        logging.info("Start gathering statistics...")
        # save in a csv format
        with open(output, "w") as f:
            # prepare header
            header = ['Timestamp', 'CPU usage %']
            if platform.startswith("linux"):
                header.extend(['Resident Set Size', 'Virtual Memory Size', 'File descriptors'])
            else:
                header.extend(['Working Set', 'Private Bytes', 'Open handles'])
            wr = csv.writer(f, delimiter=';')
            wr.writerow(header)
            p = psutil.Process()

            while True:
                data = [datetime.now(), psutil.cpu_percent()]
                if platform.startswith("linux"):
                    data.extend([p.memory_full_info().rss, p.memory_full_info().vms, len(p.open_files())])
                else:
                    data.extend([p.memory_full_info().wset, p.memory_full_info().private, len(p.open_files())])
                wr.writerow(data)
                sleep(interval)

    except KeyboardInterrupt:
        logging.info("Done")


if __name__ == "__main__":
    interval = input('Enter time interval (seconds): ')

    if not interval.isdigit():
        raise ValueError(f'{interval} is not a number')

    output = input('Enter file path: ')
    run(float(interval), output)
