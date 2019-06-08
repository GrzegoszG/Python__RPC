import rpyc

server = rpyc.connect('localhost', 18871)

content = ''
with open('code.txt', 'r') as file:
    content = file.readlines()

server.root.save_code(content)

n_fib = 7

result = server.root.execute_code(n_fib)

print('Fibb ['+ str(n_fib) + '] = ' + str(result))