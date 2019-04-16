# port-scanner

This Python script will, when function `get_server()` called, scan all IP addresses in the network range and return the one that has port 8080 open. 

This script was made for finding a server on a supposedly private network where few deviced are connected at once (at most 100 for efficiency purposes) but connection can often drop, like in supermarkets, hospitals... Devices need to connect back to the server, whose IP address might have changed in the meantime. 

This script runs on Python 2/3. 
