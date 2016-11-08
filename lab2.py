import sys
import collections
from pprint import pprint

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
			processed = [float(item) if is_number(item) else item for index, item in enumerate(raw)]
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
	# TODO: write to outfile
	data_dup = unshared_copy(data_dict)
	fill_ins = {}
	# Generate the fill-in values for missing fields
	for column_index in range(len(data_dup['meta'])):
		if "?" in [line[column_index] for line in data_dict['data']]:
			if column_index == len(data_dup['meta']) - 1:
				fill_ins[column_index] = find_most_frequent(data_dup, column_index)
			else:
				fill_ins[column_index] = find_average(data_dup, column_index)

	# Log to logfile
	with open(logfile, 'wt') as log:
		attributes = data_dict['meta']
		# loop through all columns
		for index, attr in enumerate(attributes):
			# numeric type
			num_of_missings = find_num_missing(data_dict, index)
			if num_of_missings != 0:
				print fill_ins[index]
				log.write("# thuoc tinh: {}, {}, {} \n".format(attr, num_of_missings, fill_ins[index]))

	# Replace missing values
	for line in data_dup['data']:
		#  each line in dataset
		for index, item in enumerate(line):
			# If a field is missing
			if item == "?":
				# that field is the nominal field
				line[index] = fill_ins[index]
				
	return data_dup


def discretize():
	pass

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

# Helpers
def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

def find_average(data_dict, field_index):
	column = [line[field_index] for line in data_dict['data'] if line[field_index] != "?"]
	return sum(column) / len(data_dict['data'])

def find_most_frequent(data_dict, field_index):
	column = [line[field_index] for line in data_dict['data'] if line[field_index] != "?"]
	distinct_items = set(column)
	item_with_counts = {item: column.count(item) for item in distinct_items}
	return max(item_with_counts.iterkeys(), key= (lambda key: item_with_counts[key]))

def find_num_missing(data_dict, field_index):
	how_many = len([line[field_index] for line in data_dict['data'] if line[field_index] == "?"])
	return how_many

def min_max(minc,maxc,value,newmin=0.0,newmac=1.0):
	return (float(value)-minc)/(maxc-minc)

def unshared_copy(inList):
    if isinstance(inList, list):
        return list( map(unshared_copy, inList) )
    return inList

if __name__ == "__main__":
	data = read_file("small.dat")
	outfile = "output.txt"
	# pprint(data["data"])
	# print find_most_frequent(data, -1)
	# print find_num_missing(data, -1)
	replace(data, "lol", "log.txt")
	# normalize(data,"log.txt")
	# write_file(outfile,data)
