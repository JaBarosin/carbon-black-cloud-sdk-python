# Take in user input to search across existing devices.
# Prints device info


# Next, print 5 most recent alert IDs/info


from cbc_sdk import CBCloudAPI
from cbc_sdk.platform import Device

#Start by taking input to select a device.

keyword = input("Please enter a device ID, device name, or other keyword to begin: ")


cbc_api = CBCloudAPI(profile='default')
device = cbc_api.select(Device)

if keyword != "":
	device = device.where(keyword)

for dev in device:

	print(dev.name)
