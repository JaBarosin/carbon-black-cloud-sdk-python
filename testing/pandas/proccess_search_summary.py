#!/usr/bin/env python
# *******************************************************
# Copyright (c) VMware, Inc. 2020-2021. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.


# Input process results into pandas DF
"""
Command-line example that retrieves all processes within the last six hours from all active devices.

Uses asynchronous querying to generate the queries for each device's processes so that they run in parallel.
"""

import sys
import logging
import concurrent.futures
from cbc_sdk import CBCloudAPI
from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.platform import Device
from cbc_sdk.platform import Process


log = logging.getLogger(__name__)


def main():
    """Main function for Device Processes script."""
    parser = build_cli_parser()

    args = parser.parse_args()
    # cb = get_cb_cloud_object(args)
    cb = CBCloudAPI(profile='default')

    query = cb.select(Device).set_status(['ACTIVE'])
    devices = list(query)
    dev_ids = []
    unique_procs = []
    total_procs = 0
    query_summary = []
    active_devices = []

    for d1 in devices:
        dev_ids.append(d1.id)

    print("Device count: {}".format(len(devices)))
    if args.verbose:
        print(f"Querying {len(devices)} device(s)...")
    active_queries = set()
    for device in devices:
        query = cb.select(Process).where(f"device_id:{device.id}").set_time_range(window='-1w')
        if args.verbose:
            print(f"Sending query for device ID {device.id}...")
        active_queries.add(query.execute_async())

    if args.verbose:
        print("Done sending queries, waiting for responses...")
    concurrent.futures.wait(active_queries)

    for i, future in enumerate(active_queries):
        result = future.result()

        if len(result) == 0:
            # [query id, length of query]
            query_summary.append([i, len(result)])

        if len(result) >= 1:
            # for diffing what devices were queried with results vs. no results
            active_devices.append(result[0]['device_id'])

            # [query id, device name, device id, length of results list in query]
            query_summary.append([i, result[0]['device_name'], result[0]['device_id'], len(result)])
            # print("### Device name: {} ###".format(result[i]['device_name']))
            for process in result:
                total_procs = total_procs + 1
                # print("\n {0:16} {1:5} {2:60}".format(process['device_name'], process['process_pid'][0], process['process_name']))
                if process['process_name'] not in unique_procs:
                    unique_procs.append(process['process_name'])

    print("# Number of unique Procs in search:")
    print(len(unique_procs))
    # for x in range(len(unique_procs)):
    #     print(unique_procs[x])

    '''
        Print process search summary:
        1. Query info
        2. Num of unique processes
        3. All Devices queried
        4. Num of active devices with process results
        5. Num of devices queried
        6. List devices queried with no process results
    '''
    #
    print("#1{0:10} {1:20} {2:10} {3:6}".format("Query ID", "Device Name", "device id", "# of results"))
    for x in range(len(query_summary)):
        if query_summary[x][1] != 0:
            print("{0:10} {1:20} {2:10} {3:6}".format(query_summary[x][0],
            query_summary[x][1], query_summary[x][2], query_summary[x][3]))
        if query_summary[x][1] == 0:
            print("{0:10} No results".format(int(query_summary[x-1][0])+1))

    print("\n#2 Number of unique Procs in search: ")
    print(len(unique_procs))

    # Prints all devices originally queried
    print("\n#3 --- All devices queried ---")
    for devs in devices:
        print("Device Id: " + str(devs.id))

    # Prints active devs (devices with reslults != 0, and all devs)
    print("\n#4 Num of devices with process reults: \n" + str(len(active_devices)))
    print("\n#5 Num of devices queried: \n" + str(len(dev_ids)))

    # Filter the list of all devices minus active devices to get inactive.
    # Print inactive ID and device name by matching inactive ID to device Name
    # from original devices query list
    print("\n#6 --- Devices in search with no results ---")
    quiet_devs = list(set(dev_ids) - set(active_devices))
    for devs in devices:
        for qdev in quiet_devs:
            if qdev == devs.id:
                print("Device: {}, {}".format(devs.name, qdev))


if __name__ == "__main__":
    sys.exit(main())
