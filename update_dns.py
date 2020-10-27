import urllib.request
from nfsn import Nfsn
import pickle
import datetime
import os


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
  nfsn = Nfsn(login=os.environ.get('LOGIN'), api_key=os.environ.get('API_KEY'))

  print("{ts} updating ip from {old_ip} to {new_ip}".format(ts=datetime.datetime.now(), new_ip=current_external_ip, old_ip=previous_external_ip))
  a_record = get_current_a_record(nfsn, os.environ.get('DOMAIN'))
  update_a_record(nfsn, os.environ.get('DOMAIN'), a_record, current_external_ip)
else:
  print("{ts} ip has not changed from {ip}".format(ts=datetime.datetime.now(), ip=current_external_ip))

pickle.dump(current_external_ip, open('external_ip.pickle', 'wb'))
