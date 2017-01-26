from jsonrpc2 import JsonRpc
rpc = JsonRpc()


def subtract(minuend, subtrahend):
    return minuend - subtrahend
def update(*args):
    pass
def foobar():
    pass


rpc['subtract'] = subtract
rpc['update'] = update
rpc['foobar'] = foobar

print(rpc({"jsonrpc": "2.0", "method": "subtract", "params": [42, 23], "id": 1}))
#print(rpc({"jsonrpc": "2.0", "method": "subtract", "params": [23, 42], "id": 2}))
#print(rpc({"jsonrpc": "2.0", "method": "subtract", "params": {"subtrahend": 23, "minuend": 42}, "id": 3}))
#print(rpc({"jsonrpc": "2.0", "method": "subtract", "params": {"minuend": 42, "subtrahend": 23}, "id": 4}))
