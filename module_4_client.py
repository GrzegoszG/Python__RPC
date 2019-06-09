import rpyc

class module_3_client:
    def __init__(self):
        server = rpyc.connect('localhost', 18871)
        server.root.create_table()
        content = self.get_file()
        server.root.save_code(content)
        n_fib = 8
        result = server.root.execute_code(n_fib)
        print('Fibb ['+ str(n_fib) + '] = ' + str(result))
        server.root.compare_code(11)

    def get_file(self):
        content = ''
        with open('code.txt', 'r') as file:
            content = file.readlines()
        return  content


if __name__ == "__main__":
    client = module_3_client()