import json
import codecs
import sys

import aqwsqm

class TestCase(object):
	def __init__(self, id):
		self.id = id
		file = codecs.open('test.json', 'rU', 'utf-8')
		content = file.read()
		self.data = json.loads(content)

		for jsonObj in self.data:
			if jsonObj['id']==self.id:
				self.data = jsonObj
				break

	def execute(self):
		save_stdout = sys.stdout
		fh = open("test.txt","a")
		sys.stdout = fh

		print "===================="
		print "Testcase: " + self.data["name"]
		print "===================="
		# print "Erwarteter Output: " + self.data["output"]
		print "Output:"

		SQLStmtManager_o = aqwsqm.SQLStmtManager_cl("sql.cfg")

		Query_s = SQLStmtManager_o.GenStatement_px("UpdateInst", self.data["input"])
		
		sys.stdout = save_stdout
		fh.close()

if __name__ == '__main__':
	testCase = TestCase(6)
	testCase.execute()
    
