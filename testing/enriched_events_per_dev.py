# Take in user input to search across existing enriched events.
# Prints device info

# Next, print 5 most recent alert IDs/info

from cbc_sdk import CBCloudAPI
from cbc_sdk.platform import Device
from cbc_sdk.endpoint_standard import EnrichedEvent

#Start by taking input to select a device.
keyword = ""
keyword = input("Please enter a TTP, or other keyword to begin: ")

cbc_api = CBCloudAPI(profile='default')
enriched_search = cbc_api.select(EnrichedEvent)

# Get keyword to filter enriched events
while keyword == "":
    keyword = input("Save the blank searches for the console :) Enter a TTP or other keyword to begin: ")

enriched_search = enriched_search.where(keyword)

if len(enriched_search) == 0:
    print("Welp, that one came up empty.  Try again.")
    exit()


active_devices = []

# get list of devices that reported enriched events
for event in enriched_search:
    if event['device_name'] not in active_devices:
        active_devices.append(event['device_name'])

print("## Devices with matching enriched events ##")
for dev in active_devices:
    print("Device name: {}".format(str(dev)))

# Print list of devices with reported evnts
print("\n## Sample of matching enriched events ##\n")

if len(enriched_search) == 1:
    print("{} results returned".format(len(enriched_search)))

if len(enriched_search) >= 2:
    print("{} results returned".format(len(enriched_search)))
    sample_result_count = 0
    for event in enriched_search:
        while sample_result_count <= 1:
            print("\n")
            print(type(event))
            print(str(event))
            sample_result_count = sample_result_count + 1
            print(sample_result_count)
