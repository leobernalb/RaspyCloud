# create JSON-RPC client
import jsonrpc
server = jsonrpc.ServerProxy(jsonrpc.JsonRpc20(), jsonrpc.TransportTcpIp(addr=("127.0.0.1", 31415)))

# call a remote-procedure (with positional parameters)
result = server.echo("hello world")

# call a remote-procedure (with named/keyword parameters)
found = server.search(last_name='Python')
