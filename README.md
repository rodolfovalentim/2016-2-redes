# 2016-2-redes

1.install python 2.7
2.run the script network.py(be shure that the port 12233 is available)
3.A message will appear in the screen, please write IP address (you can open a terminal and type ifconfig(LINUX/MacOS) ipconfig (WINDOWS) to check it)
4.A line with the available commands should appear .All the log messages will be displayed in the screen and sometimes it will become a complete mess, you can hit ENTER to display the options menu in a new line.
	4.1. When you are not in a network or start the program you'll have the following options:
		CREATE	- Will create a new network and you will be the only node. 
		JOIN	- Join it in an existing network, after selecting this option you should inform the IP of a known node in the network that you want to join.
		INFO	- Shows your node info.
		EXIT	- Exit the program.
	4.2. Once in the network the available commands are:
		LOOKUP	- searches for an ID in the network, after selecting this option the ID that you want to search for will be requested.
		INFO	- Shows your node info.
		LIST	- Lists all the nodes in the network
		UPDATE	- Sends a message to the antecessor node for updating its sucessor.(Proof of concept)
		LEAVE	- Leaves the current network
	all the options should be in uppercase and the parameters(jus in JOIN and LOOKUP case) should be inputed when requested.
