import urllib.request
from nfsn import Nfsn
import pickle
import yaml

with open(r'creds.yml') as file:
  creds = yaml.load(file, Loader=yaml.FullLoader)

def get_current_a_record(nfsn, domain, name=''):
  rrs = nfsn.dns(domain).listRRs(name=name)
  for rr in rrs:
    if rr['type'] == 'A':
      a_record = rr

  return a_record

def update_a_record(nfsn, domain, a_record, ip_address):
  nfsn.dns(domain).removeRR(
    name=a_record['name'],
    type='A',
    data=a_record['data'],
  )

  nfsn.dns(domain).addRR(
    name=a_record['name'],
    type='A',
    data=ip_address
  )

def external_ip():
  return urllib.request.urlopen('https://ident.me').read().decode('utf8')


current_external_ip = external_ip()

try:
  previous_external_ip = pickle.load(open("external_ip.pickle", "rb"))
except (OSError, IOError) as e:
  pickle.dump(current_external_ip, open("external_ip.pickle", "wb"))
  previous_external_ip = current_external_ip

if previous_external_ip != current_external_ip:
  nfsn = Nfsn(login=creds['login'], api_key=creds['api_key'])

  print("updating current ip address")
  a_record = get_current_a_record(nfsn, creds['domain'])
  update_a_record(nfsn, creds['domain'], a_record, current_external_ip)
else:
  print("current external ip address is the same as previous external ip address")
  print(current_external_ip)

pickle.dump(current_external_ip, open('external_ip.pickle', 'wb'))
# pickle.dump('210.0.2.96', open('external_ip.pickle', 'wb'))
