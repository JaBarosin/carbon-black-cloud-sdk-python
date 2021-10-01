# test file for cbc api ubuntu container

from cbc_sdk.platform import Device
from cbc_sdk import CBCloudAPI

cbc_api = CBCloudAPI(credential_file='/etc/carbonblack/credentials.cbc', profile='default')

get_devs = cbc_api.select(Device).set_target_priorities(["MEDIUM", "HIGH"])

print("Device API search results:")
print("{0: >20} {1: >20} {2: >20} {3: >20} {4: >20}".format("Name", "Id", "Sensor_version", "Status", "Target_priority"))
for device in get_devs:
	try:

       		print("{: >20} {: >20} {: >20} {: >20} {: >20}".format(device.name[0:18], device.id, device.sensor_version, device.status, device.target_priority))

	except TypeError:

		print("TypeError pass. Object: \n Device Name: {} \n Status: {} \n Id: {}".format(device.name, device.status, device.id))
