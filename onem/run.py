from opennem import OpenNEMClient

c = OpenNEMClient(base_url='https://api.opennem.org.au/networks')

print(dir(c))

print(c.networks())

