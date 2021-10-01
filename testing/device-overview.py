# Provide recent alerts and device info for a single devices

from cbc_sdk import CBCloudAPI
from cbc_sdk.platform import Device

# Create cloudAPI Object with profile

cbc_api = CBCloudAPI(profile='default')

#Start by taking input to select a device.

keyword = input("Please enter a device ID, device name, or other keyword to begin: ")

device = cbc_api.select(Device)

if keyword != "":
	device = device.where(keyword)

for i, dev in enumerate(device):
	print(i, dev.name)
