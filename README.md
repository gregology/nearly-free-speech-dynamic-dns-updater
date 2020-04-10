# Nearly free speech dynamic dns updater

## Installation

Requires Python 3.5

`git clone https://github.com/gregology/nearly-free-speech-dynamic-dns-updater.git`

`pip install -r requirements.txt`

`cp creds.yml.example creds.yml`

update `creds.yml`

`python update_dns.py`

### Cron job

Running every 5 mins

`*/5 * * * * cd /home/user/nearly-free-speech-dynamic-dns-updater/ && python3.5 update_dns.py >> /home/user/dynamicdns.log 2>&1`
