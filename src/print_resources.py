import pyvisa

resources = pyvisa.ResourceManager()
print(resources.list_resources())
