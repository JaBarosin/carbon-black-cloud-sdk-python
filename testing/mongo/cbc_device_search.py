# Take in user input to search across existing devices.
# Prints device info

# Next, print 5 most recent alert IDs/info

from cbc_sdk import CBCloudAPI
from cbc_sdk.platform import *
import json
import pprint

# Start by taking input to select a device.

keyword = input("Please enter a device ID, device name, or other keyword to begin: ")

cbc_api = CBCloudAPI(profile='default')

# add criteria to device search to match keyword
if keyword != "":
    device = cbc_api.select(Device).where(keyword)


cbc_vuln = CBCloudAPI(profile='supervuln')



'''

Print devices

'''
print("num devices found found: " + str(len(device)))
dev_list = []

for dev in device:
    print("\nDevice info: ")
    print(dev.name, dev.id)
    print(type(dev))
    dev_list.append(dev)

    pprint.pprint(vars(dev))


print("\nLength of dev list: " + str(len(dev_list)))
print(vars(dev_list[0]))
print(dev_list[0].name)
print(dev_list[0].id)

##############################
# vuln for ORG SUMMARY assessment clients
org_vulns = cbc_vuln.select(Vulnerability.OrgSummary)
org_results = org_vulns.submit()


'''

Print org vulnerability summary

'''

print("\nOrg Vulns")
print(type(org_results))
print(vars(org_results))
print("\n")
print()



##############################
# vuln assessment clients

# ["CRITICAL", "IMPORTANT", "MODERATE", "LOW"]


all_vulns = cbc_vuln.select(Vulnerability.AssetView)
# ass_vulns_results = asset_vulns.set_severity(severity="LOW", operator="IN")

'''

Print Asset vulnerability summary

'''

print("\nAsset Vulns")
# print(type(endpoint_vulns_results))
# print(vars(endpoint_vulns_results))
# print(len(endpoint_vulns_results))
# print("\n")
# print("\nAsset Vulns unpacking")
# for x1 in range(len(endpoint_vulns_results)):
#     print(type(endpoint_vulns_results[x1]))
#     pprint.pprint(endpoint_vulns_results[x1])

for ass in device:
    print("Device: {}".format(ass.name))
    assname =  str(ass.name)
    dev1 = cbc_api.select(Device).where(name=assname)
    dev2 = [ass1 for ass1 in dev1]

    print(dev2[0])
    # dev1 = dev1.get_vulnerability_summary()
    print(type(dev1))
    print(vars(dev1))


print("\n")

# with open("dev_data.json", 'w+') as f:
#     json.dump(dev_list, f)
