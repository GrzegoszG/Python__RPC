from rpyc import Service
from rpyc.utils.server import ThreadedServer
import subprocess


class MyService(Service):

    filename = 'test.py'

    def exposed_save_code(self, code : list):
        file = open(self.filename, 'w')
        file.truncate()
        for line in code:
            file.write(line)
        file.close()
        return True

    def exposed_execute_code(self, n : int):
        fib = subprocess.call("python "+self.filename + ' ' + str(n))
        return int(fib)

if __name__ == '__main__':
    s = ThreadedServer(MyService, hostname='localhost', port=18871, protocol_config={"allow_public_attrs" : True})
    s.start()
    