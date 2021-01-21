file = open("data.csv", "r").read()
ch = file.split("\"")
prev = 0
for i in range(1, len(ch), 2):
	c = file.find(ch[i], prev+len(ch[i-1]))
	file = file[:c] + file[c:c+len(ch[i])].replace(",", "π") + file[c+len(ch[i]):]
	prev = file.find(ch[i], 2)
file = file.split('\n')[1:]

objs = {}
# CSV Parser
for obj in file:
	parse = obj.split(",")
	if parse[1] == "Terminator":
		objs[parse[0]] = {"type":parse[1], "to":parse[7], "from":parse[6], "name":parse[10], "extras":[], "payload":parse[10].replace("π", ",").replace("\"", "")}
	else:
		objs[parse[0]] = {"type":parse[1], "to":parse[7], "from":parse[6], "name":parse[10], "extras":[], "payload":None}
for obj in objs:
	if objs[obj]["type"] == "Terminator" and objs[obj]["name"] == "Input":
		for check in objs:
			if objs[check]["type"] == "Line" and objs[check]["to"] == obj:
				connect = objs[objs[check]["from"]]["payload"]
				objs[obj]["payload"] = input(connect)
def updatelinepayloads():
	for obj in objs:
		if objs[obj]["type"] == "Line":
			objs[obj]["payload"] = objs[objs[obj]["from"]]["payload"]
# Line Connections

for obj in objs:
	obj = objs[obj]
	if obj["type"] == "Line":
		objs[obj["to"]]["extras"].append(objs[obj["from"]])
# Payloading operators (e.g Add, Subtract)
for obj in objs:
	if objs[obj]["type"] == "Process" and objs[obj]["name"] == "+":
		try:
			objs[obj]["payload"] = float(objs[obj]["extras"][0]["payload"]) + float(objs[obj]["extras"][1]["payload"])
		except ValueError:
			objs[obj]["payload"] = objs[obj]["extras"][0]["payload"] + objs[obj]["extras"][1]["payload"]
	if objs[obj]["type"] == "Process" and objs[obj]["name"] == "-":
		objs[obj]["payload"] = float(objs[obj]["extras"][0]["payload"]) - float(objs[obj]["extras"][1]["payload"])
	if objs[obj]["type"] == "Process" and objs[obj]["name"] == "x":
		objs[obj]["payload"] = float(objs[obj]["extras"][0]["payload"]) * float(objs[obj]["extras"][1]["payload"])
	if objs[obj]["type"] == "Process" and objs[obj]["name"] == "/":
		objs[obj]["payload"] = float(objs[obj]["extras"][0]["payload"]) / float(objs[obj]["extras"][1]["payload"])
# Line Payload Updating
updatelinepayloads()
for obj in objs:
	if objs[obj]["type"] == "Decision" and objs[obj]["name"] == "=":
		if objs[obj]["extras"][1]["payload"] == objs[obj]["extras"][2]["payload"]:
			objs[obj]["payload"] = objs[obj]["extras"][0]["payload"]
		else:
			try:
				objs[obj]["payload"] = objs[obj]["extras"][3]["payload"]
			except IndexError:
				objs[obj]["payload"] = 0

	if objs[obj]["type"] == "Decision" and objs[obj]["name"] == "!=":
		if objs[obj]["extras"][1]["payload"] != objs[obj]["extras"][2]["payload"]:
			objs[obj]["payload"] = objs[obj]["extras"][0]["payload"]
		else:
			try:
				objs[obj]["payload"] = objs[obj]["extras"][3]["payload"]
			except IndexError:
				objs[obj]["payload"] = 0

	if objs[obj]["type"] == "Decision" and objs[obj]["name"] == ">":
		if objs[obj]["extras"][1]["payload"] > objs[obj]["extras"][2]["payload"]:
			objs[obj]["payload"] = objs[obj]["extras"][0]["payload"]
		else:
			try:
				objs[obj]["payload"] = objs[obj]["extras"][3]["payload"]
			except IndexError:
				objs[obj]["payload"] = 0
	
	if objs[obj]["type"] == "Decision" and objs[obj]["name"] == "<":
		if objs[obj]["extras"][1]["payload"] < objs[obj]["extras"][2]["payload"]:
			objs[obj]["payload"] = objs[obj]["extras"][0]["payload"]
		else:
			try:
				objs[obj]["payload"] = objs[obj]["extras"][3]["payload"]
			except IndexError:
				objs[obj]["payload"] = 0
updatelinepayloads()
for obj in objs:
	if objs[obj]["type"] == "Process" and objs[obj]["name"] == "Output":
		print(objs[obj]["extras"][0]["payload"])
