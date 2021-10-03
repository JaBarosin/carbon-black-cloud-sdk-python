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

    for d1 in devices:
        dev_ids.append(d1.id)

    print("Device count: {}".format(len(devices)))
    if args.verbose:
        print(f"Querying {len(devices)} device(s)...")
    active_queries = set()
    for device in devices:
        query = cb.select(Process).where(f"device_id:{device.id}").set_time_range(window='-24h')
        if args.verbose:
            print(f"Sending query for device ID {device.id}...")
        active_queries.add(query.execute_async())

    if args.verbose:
        print("Done sending queries, waiting for responses...")
    concurrent.futures.wait(active_queries)
    print("{0:16} {1:5} {2:60}".format("Device Name", "PID", "Process Name"))
    print("{0:16} {1:5} {2:60}".format("-----------", "---", "------------"))

    unique_procs = []
    total_procs = 0
    query_summary = []
    active_devices = []


    for i, future in enumerate(active_queries):
        result = future.result()

        if len(result) == 0:
            query_summary.append(["### Query number: {} ###".format(i), type(result), len(result)])
            print(result)

        if len(result) >= 1:
            # for diffing what devices were queried with results vs. no results
            active_devices.append(result[0]['device_id'])

            # summary
            query_summary.append(["### Query number: {} ###".format(i), result[0]['device_name'], result[0]['device_id'], type(result), len(result)])
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

    print("# Results Summary:")
    for x in range(len(query_summary)):
        if len(query_summary[x]) != 0:
            print(query_summary[x])

    print("All devices")
    for devs in devices:
        print("Device Id: " + str(devs.id))


    print("active devs: " + str(len(active_devices)))
    print("All devs: " + str(len(dev_ids)))

    print("# Devices in search with no results: ")
    quiet_devs = list(set(dev_ids) - set(active_devices))
    for devs in devices:
        for qdev in quiet_devs:
            if qdev == devs.id:
                print("Device: {}, {}".format(devs.name, qdev))


if __name__ == "__main__":
    sys.exit(main())
