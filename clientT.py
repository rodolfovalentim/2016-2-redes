from node import *

default_port = 12233

def join():
    contact_ip = raw_input('IP of your contact in the network: ')

    while(True):
        ip_sucessor = node.lookup(node.key, (contact_ip, default_port))

        while(ip_sucessor == None):
            pass

        if(not node.join(ip_sucessor[2])):
            node.get_new_key()
            continue
        if(not node.update()):
            node.get_new_key()
            continue
        break

ip = raw_input('Your IP: ')
node = Node(ip)
node.listener()
join()
