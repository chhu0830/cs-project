import requests
import sys

server = 'http://140.113.66.98:8080'

def create_application(app_name):
    url = server + '/~/in-cse'
    headers={
        'X-M2M-Origin': 'admin:admin',
        'Content-Type': 'application/xml;ty=2',
        'X-M2M-NM': app_name
    }
    data='<om2m:ae xmlns:om2m="http://www.onem2m.org/xml/protocols">\
              <api>app-sensor</api>\
              <lbl>Tpye/sensor Category/temperature Location/home</lbl>\
              <rr>false</rr>\
          </om2m:ae>'
    print(requests.post(url, headers=headers, data=data))

def create_container(app_name, con_name):
    url = server + '/~/in-cse/in-name/' + app_name
    headers={
        'X-M2M-Origin': 'admin:admin',
        'Content-Type': 'application/xml;ty=3',
        'X-M2M-NM': con_name
    }
    data='<om2m:cnt xmlns:om2m="http://www.onem2m.org/xml/protocols">\
          </om2m:cnt>'
    print(requests.post(url, headers=headers, data=data))

def create_contain_instance(app_name, con_name, con_ins_data):
    url = server + '/~/in-cse/in-name/' + app_name + '/' +  con_name
    headers={
        'X-M2M-Origin': 'admin:admin',
        'Content-Type': 'application/xml;ty=4',
    }
    data='<om2m:cin xmlns:om2m="http://www.onem2m.org/xml/protocols">\
              <cnf>message</cnf>\
              <con>\
                  %s\
              </con>\
          </om2m:cin>' % con_ins_data
    print(requests.post(url, headers=headers, data=data))


if __name__ == '__main__':
    print('usage: python3 om2m.py 2 <application>')
    print('usage: python3 om2m.py 3 <application> <container>')
    print('usage: python3 om2m.py 4 <application> <container> <data>')
    if sys.argv[1] == '2':
        create_application(sys.argv[2])
    elif sys.argv[1] == '3':
        create_container(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == '4':
        create_contain_instance(sys.argv[2], sys.argv[3], sys.argv[4])
