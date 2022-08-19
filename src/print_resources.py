import pyvisa

resources = pyvisa.ResourceManager("@py")
print(resources.list_resources())
