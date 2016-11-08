import sys
import collections

def user_input():
	if len(sys.argv) != 5:
		print "Wrong number of arguments!"
		return None
	option, infile, outfile, log = sys.argv[1:]
	return (option, infile, outfile, log)


def read_file(filename):
	with open(filename, 'rt') as f:
		first_line = f.readline().strip().split(',')
		data = []
		for line in f:
			raw = line.strip().split(',')
			processed = [float(item) if index != 4 and item != "?" else "?" for index, item in enumerate(raw)]
			processed.append(raw[-1])
			data.append(processed)
	return {'meta': first_line, 'data': data}

def write_file(filename,data):
	with open(filename, 'wt') as f:
		f.write(",".join(data["meta"])+"\n")
		for row in data["data"]:
			f.write(",".join(str(x) for x in row) + "\n")
	f.close()

def user_option(option):
	if option not in ["summary", "replace", "discretize", "normalize"]:
		return None
	if option == "summary":
		summary()
	elif option == "replace":
		replace()
	elif option == "discretize":
		discretize()
	elif option == "normalize":
		normalize()

def summary(data_dict, logfile):
	attributes = data_dict['meta']
	num_of_samples = data_dict
	with open(logfile, 'wt') as f:
		f.write("# so mau: " + str(len(data_dict['data'])) + "\n")
		f.write("# so thuoc tinh: " + str(len(data_dict['meta'])) + "\n")
		for index, attr in enumerate(attributes):
			if index == len(attributes) - 1:
				_type = "nominal"
			else:
				_type = "numeric"
			print "# thuoc tinh {}: {} {}".format(index, attr, _type)
			f.write("# thuoc tinh {}: {} {}".format(index, attr, _type))

def replace(data_dict, outfile, logfile):
	data_dup = data_dict['data']
	for line in data_dup:
		for index, item in enumerate(line):
			if item == "?":
				line[index] = find_average(data_dict, index)
	with open(logfile, 'wt') as log:
		attributes = data_dict['meta']
		# loop through all columns
		for index, attr in attributes:
			# numeric type
			if index != len(attributes) - 1:
				log.write("# thuoc tinh: {}, {}, {}".format(attr, find_num_missing(data_dict, index), find_average(data_dict, index)))
			else:
				log.write("# thuoc tinh: {}, {}, {}".format(attr, find_num_missing(data_dict, index), find_most_frequent(data_dict, index)))

def discretize():
	pass
def min_max(minc,maxc,value,newmin=0.0,newmac=1.0):
	return (float(value)-minc)/(maxc-minc)
def normalize(data,logfile):
	method = raw_input("Ban hay nhap phuong phap chuan hoa (min-max, z-score): ").strip()
	#method = "z-score"
	log = open(logfile, 'wt')
	if (method == "min-max"):
		numcol = len(data["meta"])-1
		m = [[min(col),max(col)] for col in [[x[i] for x in data["data"] if (x[i]!="?")] for i in range(numcol)]]
		for index1,row in enumerate(data["data"]):
			for index2,col in enumerate(row):
				if index2 < numcol and col != "?":
					value = min_max(m[index2][0],m[index2][1],data["data"][index1][index2])
					data["data"][index1][index2] = value
					log.write("# thuoctinh: %s, %f\n" %(data["meta"][index2],value))
		#print data
		
	if (method == "z-score"):
		for index in range(len(data["meta"])-1):
			value = [x[index] for x in data["data"] if x[index]!="?"]
			ave = sum(value)/len(value)
			var = sum([(x-ave)**2 for x in value])/len(value)
			std_dev = var**0.5
			for i,row in enumerate(data["data"]):
				if data["data"][i][index] != "?":
					value = (row[index] - ave)/std_dev
					data["data"][i][index] = value
					log.write("# thuoctinh: %s, %f\n" %(data["meta"][index],value))		
		#print data
	log.close()
		

def find_average(data_dict, field_index):
	column = [line[field_index] for line in data_dict['data'] if line[field_index] != "?"]
	return sum(column) / len(data_dict['data'])

def find_most_frequent(data_dict, field_index):
	attr_freq = collections.defaultdict(lambda: 1)
	max_attr = {'attr': '', 'freq': 0}
	for data in data_dict['data']:
		if data[field_index] != '?':
			attr_freq[data[field_index]] += 1
	for attr, freq in attr_freq.iteritems():
		if freq > max_attr['freq']:
			max_attr['attr'] = attr
			max_attr['freq'] = freq
	return max_attr['attr']

def find_num_missing(data_dict, field_index):
	how_many = len([line[field_index] for line in data_dict['data'] if line[field_index] == "?"])
	return how_many

if __name__ == "__main__":
	data = read_file("data.dat")
	outfile = "output.txt"
	#print data["data"]
	# print find_most_frequent(data, -1)
	# print find_num_missing(data, -1)
	#replace(data, "lol", "log.txt")
	normalize(data,"log.txt")
	write_file(outfile,data)
