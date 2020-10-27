FROM python:3.5
ADD update_dns.py /
RUN pip install python-nfsn==1.1.1
CMD [ "python", "./update_dns.py" ]