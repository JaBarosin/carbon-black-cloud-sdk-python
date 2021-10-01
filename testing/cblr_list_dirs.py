# Test CB Live Response API

# import relevant modules
from cbc_sdk.platform import Device
from cbc_sdk import CBCloudAPI

# create Platform API object
cbc_api = CBCloudAPI(profile='default')

# search for specific devices with Platform Devices API
get_devs = cbc_api.select(Device).sort_by("last_contact_time", direction="DESC")



# execute commands with Live Response API
for device in get_devs:
	print(device.name, device.last_contact_time)
	lr_session = cbc_api.live_response.request_session(device.id)
	list_dir = lr_session.list_directory('C:\\\\')
	for dirs in list_dir:
		print(f"{dirs['attributes'][0]} {dirs['filename']}")
	lr_session.close()
