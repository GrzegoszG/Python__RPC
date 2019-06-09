from rpyc import Service
from rpyc.utils.server import ThreadedServer
import subprocess
from dbmanager import DbManager
import difflib

class Module3Server(Service):

    filename = 'test.py'
    db = DbManager('localhost', 'root', '', 'testowa')

    def exposed_create_table(self):
        self.db = DbManager('localhost', 'root', '', 'testowa')
        self.db.executesql("CREATE TABLE IF NOT EXISTS programs (id integer PRIMARY KEY AUTO_INCREMENT, program_name VARCHAR(128) NOT NULL, code_text VARCHAR(4096) NOT NULL, date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        self.db.executesql("CREATE TABLE IF NOT EXISTS programs_diffs (id integer PRIMARY KEY AUTO_INCREMENT, program1_id integer NOT NULL, program2_id integer NOT NULL, similarity float NOT NULL DEFAULT 0, diff VARCHAR(4096) NULL)")

    def exposed_save_code(self, code : list):
        file = open(self.filename, 'w')
        file.truncate()
        code_text = ''
        for line in code:
            file.write(line)
            code_text += line
        self.save_into_db(code_text)
        file.close()
        return True

    def save_into_db(self, code : str):
        sql = "INSERT INTO programs (program_name, code_text) VALUES (\'" + self.filename + "\',\'" + code + "\')"
        self.db.executesql(sql)
        self.db.commit_changes()

    def exposed_execute_code(self, n : int):
        fib = subprocess.call("python "+self.filename + ' ' + str(n))
        return int(fib)

    def exposed_compare_code(self, n : int):
        sql = "SELECT * FROM programs"
        self.db.executesql(sql)
        rows = self.db.get_result()
        row = next((x for x in rows if x['id'] == n), None)
        if row == None:
            return 
        code = str(row['code_text'])
        for r in rows:
            r_id = int(r['id'])
            if r_id == n:
                continue
            
            code2 = str(r['code_text'])
            c1 = code.splitlines(False)
            c2 = code2.splitlines(False)
            diff = difflib.unified_diff(c1, c2)
            match = difflib.SequenceMatcher(None, code, code2)
            m = match.ratio()
            str_diff = ''
            sql = ''
            print('=========')
            print('ID = '+str(r['id']))
            print('Similarity = '+str(m))
            for line in diff:
                print (line)
                str_diff += line
            sql = "INSERT INTO programs_diffs (program1_id, program2_id, similarity, diff) VALUES ("+str(n)+","+str(r_id)+","+str(m)+",\'"+str_diff+"\')"
            self.db.executesql(sql)
            self.db.commit_changes()
            print('')


if __name__ == '__main__':
    s = ThreadedServer(Module3Server, hostname='localhost', port=18871, protocol_config={"allow_public_attrs" : True})
    s.start()
    