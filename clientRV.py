from node import *

def join():
    contact_ip = raw_input('IP of your contact in the network: ')

    while(True):
        _, _, ip_sucessor = node.lookup(node.key, (contact_ip, default_port))
        if(not node.join(ip_sucessor)):
            node.get_new_key()
            continue
        if(not node.update()):
            node.get_new_key()
            continue
        break

ip = raw_input('Your IP: ')
node = Node(ip)
join()
