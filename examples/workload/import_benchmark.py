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

"""Example script for configuring CIS Benchmarks"""

import sys
import json
import time
import requests
from collections import Counter
from cbc_sdk.helpers import build_cli_parser


def parse_args():
    """Add benchmarkid and list benchmarks options to args"""
    parser = build_cli_parser("Tune Benchmarks")
    parser.add_argument("--benchmarkid", type=str, default=None, help="Sets the specific benchmark id of interest")
    parser.add_argument("-L", "--listbenchmarks", type=str, default=None, help="Lists available benchmarks")
    org_args = parser.parse_args()
    return org_args


def menu_1():
    menu = """
Select Option:

1. Import CBC template Benchmark (disables FW network related recommendations along with MS Defender related)
2. View/Modify existing Benchmark
3. Exit

    """
    return menu


def menu_2():
    menu = """
Select Option: 

1. List benchmarks
2. List sections
3. List rules
4. List rule status per section
5. Search rules w/ keyword
6. Disable all rules
7. Enable rules with matching keyword
8. Change benchmark status
9. Exit

    """
    return menu


def list_benchmark_rules_summary(cb_args, benchmark_id=None):
    """ Lists a per section view of benchmarks rules status """

    bench_rules = "compliance/assessment/api/v1/orgs/{0}/benchmark_sets/{1}/rules/_search".format(cb_args.orgkey,
                                                                                                  benchmark_id)
    url = "{0}/{1}".format(cb_args.cburl, bench_rules)
    headers = {
        'content-type': 'application/json',
        'X-Auth-Token': cb_args.apitoken
    }

    body = """
           {
               "query": "",
               "rows": 350,
               "criteria": {
                   "section_name": ["All"]
                   },
               "sort": [
                   {
                       "field": "section_name",
                       "order": "ASC"
                   }],
               "start": 0
           }
           """

    response = requests.post(headers=headers, url=url, data=body)
    response = response.json()
    od_response = sorted(response['results'], key=lambda d: d['section_name'])
    c = Counter()

    for k in od_response:
        c[k['enabled']] += 1
        section_rule_counter = []
        if k['section_name'] not in section_rule_counter:
            section_rule_counter.append(k['section_name'])

    enabled_count = c[True]
    disabled_count = c[False]
    print("\nRules for Benchmark ID: {}".format(benchmark_id))
    print("Enabled: ", enabled_count, " Disabled: ", disabled_count)


def get_benchmark_rules_summary(cb_args, benchmark_id=None):
    bench_rules = "compliance/assessment/api/v1/orgs/{0}/benchmark_sets/{1}/rules/_search".format(cb_args.orgkey,
                                                                                                  benchmark_id)
    url = "{0}/{1}".format(cb_args.cburl, bench_rules)
    headers = {
        'content-type': 'application/json',
        'X-Auth-Token': cb_args.apitoken
    }

    body = """
           {
               "query": "",
               "rows": 350,
               "criteria": {
                   "section_name": ["All"]
                   },
               "sort": [
                   {
                       "field": "section_name",
                       "order": "ASC"
                   }],
               "start": 0
           }
           """

    response = requests.post(headers=headers, url=url, data=body)
    response = response.json()

    od_response = sorted(response['results'], key=lambda d: d['section_name'])
    c = Counter()

    for k in od_response:
        c[k['enabled']] += 1
        section_rule_counter = []
        if k['section_name'] not in section_rule_counter:
            section_rule_counter.append(k['section_name'])

    enabled_count = c[True]
    disabled_count = c[False]

    return "{0}/{1}".format(enabled_count, str(len(od_response)))


def get_benchmarks(cb_args):
    """Returns list object of all benchmarks"""

    search_benchmarks_url = "compliance/assessment/api/v1/orgs/{0}/benchmark_sets/_search".format(cb_args.orgkey)
    url = "{0}/{1}".format(cb_args.cburl, search_benchmarks_url)
    headers = {
        'content-type': 'application/json',
        'X-Auth-Token': cb_args.apitoken
    }

    body = """
            {
                "query": "",
                "rows": 350,
                "criteria": {
                    "section_name": ["All"]
                    },
                "sort": [
                    {
                        "field": "section_name",
                        "order": "ASC"
                    }],
                "start": 0
            }
            """

    response = requests.post(headers=headers, url=url, data=body)
    response = response.json()
    lb2 = list(response['results'])

    return lb2


def list_benchmarks(cb_args):
    """Prints list object of all benchmarks"""

    search_benchmarks_url = "compliance/assessment/api/v1/orgs/{0}/benchmark_sets/_search".format(cb_args.orgkey)
    url = "{0}/{1}".format(cb_args.cburl, search_benchmarks_url)
    headers = {
        'content-type': 'application/json',
        'X-Auth-Token': cb_args.apitoken
    }

    body = """
        {
            "query": "",
            "rows": 350,
            "criteria": {
                "section_name": ["All"]
                },
            "sort": [
                {
                    "field": "section_name",
                    "order": "ASC"
                }],
            "start": 0
        }
        """

    response = requests.post(headers=headers, url=url, data=body)
    response = response.json()
    lb2 = list(response['results'])
    print("\n# " + str(response['num_found']) + " Benchmarks for org " + str(cb_args.orgkey) + " #\n")
    for num, bench in enumerate(lb2):
        num += 1
        print("{0:50}\tEnabled: {1:7} Rules: {2:12} \tID: {3}"
              .format(bench['name'],
                      str(bench['enabled']),
                      get_benchmark_rules_summary(cb_args, bench['id']),
                      bench['id']))

    return lb2


def get_benchmark_rules(cb_args, benchmark_id=None):
    """Returns list of all rules in specified benchmark"""

    if benchmark_id is not None:
        bench_id = benchmark_id
    else:
        bench_id = cb_args.benchmarkid

    bench_search = "compliance/assessment/api/v1/orgs/{0}/benchmark_sets/{1}/rules/_search".format(cb_args.orgkey,
                                                                                                   bench_id)
    url = "{0}/{1}".format(cb_args.cburl, bench_search)
    headers = {
        'content-type': 'application/json',
        'X-Auth-Token': cb_args.apitoken
    }

    body = """
       {
           "query": "",
           "rows": 350,
           "criteria": {
               "section_name": ["All"]
               },
           "sort": [
               {
                   "field": "section_name",
                   "order": "ASC"
               }],
           "start": 0
       }
       """

    response = requests.post(headers=headers, url=url, data=body)

    try:
        resp = response.json()
        rules_list = list(resp['results'])

    except ValueError as e:
        print('error type', type(e))

    return rules_list


def list_benchmark_sections(cb_args, benchmark_id=None):
    # Need to organize under parent > child sections to mirror UI
    """ Lists all sections in a benchmark """

    # Checks if other benchmark ID was provided or uses default if none
    if benchmark_id is not None:
        bench_id = benchmark_id
    else:
        bench_id = cb_args.benchmarkid

    bench_search = "compliance/assessment/api/v1/orgs/{0}/benchmark_sets/{1}/sections".format(cb_args.orgkey,
                                                                                              bench_id)

    url = "{0}/{1}".format(cb_args.cburl, bench_search)

    headers = {
        'content-type': 'application/json',
        'X-Auth-Token': cb_args.apitoken,
    }

    body = """
       {
           "query": "",
           "rows": 350,
           "criteria": {
               "section_name": ["All"]
               },
           "sort": [
               {
                   "field": "section_name",
                   "order": "ASC"
               }],
           "start": 0
       }
       """

    response = requests.get(headers=headers, url=url, data=body)
    sections = response.json()

    for i, s in enumerate(sections):
        print(str(i), s['section_name'], s['section_id'], s['parent_id'])


def list_benchmark_status_per_section(cb_args, benchmark_id=None):
    """ Lists the number of rules enabled / total rules per section """

    # Checks if other benchmark ID was provided or uses default if none
    if benchmark_id is not None:
        bench_id = benchmark_id
    else:
        bench_id = cb_args.benchmarkid

    bench_search = "compliance/assessment/api/v1/orgs/{0}/benchmark_sets/{1}/rules/_search".format(cb_args.orgkey,
                                                                                                   bench_id)
    url = "{0}/{1}".format(cb_args.cburl, bench_search)

    headers = {
        'content-type': 'application/json',
        'X-Auth-Token': cb_args.apitoken
    }

    body = """
       {
           "query": "",
           "rows": 350,
           "criteria": {
               "section_name": ["All"]
               },
           "sort": [
               {
                   "field": "section_name",
                   "order": "ASC"
               }],
           "start": 0
       }
       """

    response = requests.post(headers=headers, url=url, data=body)
    c = Counter()

    try:
        resp = response.json()
        print(type(resp))
        rules = list(resp['results'])
        # print(resp['results'])

        for rule in rules:
            c[rule['section_name']] += 1

        for sect in c:
            enabled_count = 0

            for r in rules:
                if r['section_name'] == sect:
                    if r['enabled'] is True:
                        enabled_count += 1

            print("{0:56}\tEnabled: {1} of {2}".format(sect, enabled_count, c[sect]))

    except ValueError as e:
        print('error type', type(e))


def disable_all_rules(cb_args, benchmark_id=None):
    """ Send list of rule IDs and their desired status.

    [
        {
            "rule_id": "<string>",
            "enabled": <bool>
        }
    ]

    """
    if benchmark_id is not None:
        bench_id = benchmark_id
    else:
        bench_id = cb_args.benchmarkid

    bench_search = "compliance/assessment/api/v1/orgs/{0}/benchmark_sets/{1}/rules".format(cb_args.orgkey,
                                                                                           bench_id)
    url = "{0}/{1}".format(cb_args.cburl, bench_search)
    headers = {
        'content-type': 'application/json',
        'X-Auth-Token': cb_args.apitoken
    }

    rules = get_benchmark_rules(cb_args, bench_id)
    body = []

    for r in rules:
        body.append(
            {
                "rule_id": r['id'],
                "enabled": False
            })

    body = json.dumps(body)
    response = requests.put(headers=headers, url=url, data=body)
    print(response.status_code)


def get_rules_by_keyword(cb_args, keyword, benchmark_id=None):
    # Checks if other benchmark ID was provided or uses default if none
    kw = str(keyword)
    rule_list = []

    if benchmark_id is not None:
        bench_id = benchmark_id
    else:
        bench_id = cb_args.benchmarkid

    bench_search = "compliance/assessment/api/v1/orgs/{0}/benchmark_sets/{1}/rules/_search".format(cb_args.orgkey,
                                                                                                   bench_id)

    url = "{0}/{1}".format(cb_args.cburl, bench_search)

    headers = {
        'content-type': 'application/json',
        'X-Auth-Token': cb_args.apitoken
    }

    body = {
        "query": kw,
        "rows": 350,
        "start": 0,
        "criteria": {
            "section_name": [""]
        },
        "sort": [
            {
                "field": "section_name",
                "order": "ASC"
            }
        ]
    }

    body = json.dumps(body)

    response = requests.post(headers=headers, url=url, data=body)
    print(response.status_code)
    print(response)
    rule_search = response.json()

    for rule in rule_search['results']:
        rule_list.append(rule)

    print("\n###", rule_search['num_found'], " Rules found using keyword: ", kw, " ###\n")

    return rule_list


def clone_bench_template(cb_args, bench_name):
    # Gets ID of OOTB CIS Benchmark
    bm = get_benchmarks(cb_args)
    for b in bm:
        if b['name'] == "CIS Compliance - Microsoft Windows Server":
            cis_b = b['id']

    bench_clone = "compliance/assessment/api/v1/orgs/{0}/benchmark_sets/{1}/_clone".format(cb_args.orgkey,
                                                                                           cis_b)

    url = "{0}/{1}".format(cb_args.cburl, bench_clone)
    headers = {
        'content-type': 'application/json',
        'X-Auth-Token': cb_args.apitoken
    }

    body = {
        "benchmark_name": bench_name
    }

    body = json.dumps(body)
    response = requests.post(headers=headers, url=url, data=body)
    print(response.status_code)


def enable_rules_from_list(cb_args, rule_list, benchmark_id=None):
    if benchmark_id is not None:
        bench_id = benchmark_id
    else:
        bench_id = cb_args.benchmarkid

    # rules_to_enable = rule_list
    bench_search = "compliance/assessment/api/v1/orgs/{0}/benchmark_sets/{1}/rules".format(cb_args.orgkey,
                                                                                           bench_id)

    url = "{0}/{1}".format(cb_args.cburl, bench_search)

    headers = {
        'content-type': 'application/json',
        'X-Auth-Token': cb_args.apitoken
    }

    body = []

    for r in rule_list:
        body.append(
            {
                "rule_id": r['id'],
                "enabled": True
            })

    body = json.dumps(body)
    response = requests.put(headers=headers, url=url, data=body)
    print(response.status_code)


def update_benchmark(cb_args, bench_id, action_option):
    if bench_id is not None:
        bench_id = bench_id
    else:
        bench_id = cb_args.benchmarkid

    actions = ["DISABLE", "ENABLE"]
    if action_option in "0":
        action = actions[0]
    elif action_option in "1":
        action = actions[1]

    bench_action = "compliance/assessment/api/v1/orgs/{0}/benchmark_sets/{1}/actions".format(cb_args.orgkey,
                                                                                             bench_id)
    url = "{0}/{1}".format(cb_args.cburl, bench_action)
    headers = {
        'content-type': 'application/json',
        'X-Auth-Token': cb_args.apitoken
    }

    body = {
        "action": action
    }

    body = json.dumps(body)
    response = requests.post(headers=headers, url=url, data=body)

    return response


def main():
    print("\n### CBC CIS Benchmark Import ###\n")
    args = parse_args()

    if args.listbenchmarks == "all":
        list_benchmarks(args)
    if args.benchmarkid:
        print("Selected benchmark: ", args.benchmarkid)

    print(menu_1())
    m1 = input("")

    # Import from template
    if m1 in "1":
        print("Getting ready to import rules to existing benchmark...")
        cbc_custom_b_name = str(input("\nEnter Benchmark Name (example: CBC-custom-benchmark): "))
        clone_bench_template(args, cbc_custom_b_name)
        bms = get_benchmarks(args)

        # gets ID of newly created benchmark
        for b in bms:
            if b['name'] == cbc_custom_b_name:
                bench_id = b['id']

        rules_to_enable = []
        # File of benchmark rules to use as template for which to enable
        with open("cbc-template.json", "r") as f:
            cbc_rule_list = json.load(f)

            # Only need to send the rules to enable - starting from all rules disabled
            for rule in cbc_rule_list:
                if rule['enabled']:
                    rules_to_enable.append(rule)

            print("Creating new Benchmark.")
            disable_all_rules(args, bench_id)

            """
                CBC is on the device; providing AV, managing the HBFW, and monitoring processes.
                
                cbc-template is used to configure a new benchmark so that rules for HBFW profiles, MS Defender, and process auditing are disabled
                
            """
            print("Enabling rules from cbc-template.json")
            enable_rules_from_list(args, rules_to_enable, bench_id)
            print("New Benchmark created: ", "'" + cbc_custom_b_name + "'", bench_id)
            update_benchmark(args, bench_id, "1")
            list_benchmark_rules_summary(args, bench_id)
        exit()

    # Menu 2
    elif m1 in "2":

        bms = list_benchmarks(args)
        if args.benchmarkid:
            user_bench = args.benchmarkid
        else:
            user_bench = str(input("\nInput Benchmark ID:"))

        bench_ids = []
        for bs in bms:
            bench_ids.append(bs['id'])

        if user_bench not in bench_ids:
            print("Please enter the ID of an existing Benchmark of interest to continue.")
            exit()

        elif user_bench in bench_ids:

            print(user_bench)
            while True:
                time.sleep(1)
                print(menu_2())
                option = input("")

                if option in "1":
                    list_benchmarks(args)
                    continue

                if option in "2":
                    list_benchmark_sections(args, user_bench)
                    continue

                if option in "3":
                    rules = get_benchmark_rules(args, user_bench)
                    for rule in rules:
                        rname = str(rule['rule_name'])[0:78]
                        print("{0:78}\tEnabled: {1:7}\t{2:32} {3}".format(
                            (rname),
                            str(rule['enabled']),
                            rule['section_name'],
                            rule['id']))

                    list_benchmark_rules_summary(args, user_bench)
                    continue

                if option in "4":
                    list_benchmark_status_per_section(args, user_bench)
                    list_benchmark_rules_summary(args, user_bench)
                    continue

                if option in "5":
                    """ Gets list of rules (ids) with keyword search """

                    kw = input("Input keyword for search (ex. 'password', 'account': ")
                    if len(kw) > 0:
                        r2 = get_rules_by_keyword(args, kw, user_bench)

                        for r in r2:
                            rname = str(r['rule_name'])[0:78]
                            print("{0:78}\tEnabled: {1:7}\t{2:32} {3}".format(
                                (rname),
                                str(r['enabled']),
                                r['section_name'],
                                r['id']))

                    continue

                if option in "6":
                    """ Disable all rules in benchmark """

                    print("Disabling rules for ", user_bench)
                    disable_all_rules(args, user_bench)
                    list_benchmark_rules_summary(args, user_bench)
                    continue

                if option in "7":
                    """ Enables rules using input list of rules (ids) from keyword search """

                    kw = input("Input keyword for search (ex. 'password', 'account': ")
                    if len(kw) > 0:
                        rule_list = get_rules_by_keyword(args, kw, user_bench)
                        enable_rules_from_list(args, rule_list, user_bench)
                        list_benchmark_rules_summary(args, user_bench)
                    continue

                if option == "8":
                    """ Enable Benchmark """

                    temp_bs = get_benchmarks(args)
                    for b in temp_bs:
                        if b['id'] == user_bench:

                            action = "y"
                            print(b['name'], b['enabled'])

                            while action != "n":
                                action = str(input("Enter 1 to ENABLE or 0 to DISABLE benchmark: "))

                                if len(action) > 0:
                                    pass
                                else:
                                    print("Please enter y/n. ")
                                    continue

                                if action in "1":
                                    print("update benchmark status for id ", user_bench)
                                    bench_update = update_benchmark(args, user_bench, "1")
                                    print(bench_update.status_code)
                                    exit()
                                elif action in "0":
                                    print("Disabling benchmark id ", user_bench)
                                    bench_update = update_benchmark(args, user_bench, "0")
                                    print(bench_update.status_code)
                                    exit()
                                    action = "n"
                                elif action not in ("n", "y"):
                                    print("Whoops. Please enter 0 or 1")
                        continue

                if option == "9" or "exit" or "Exit":
                    exit()

    elif m1 == "3" or "exit" or "Exit":
        exit()

    else:
        print("Please enter a valid selection. ")
        exit()


if __name__ == "__main__":
    sys.exit(main())

