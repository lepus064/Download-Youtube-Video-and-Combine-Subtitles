import os, sys
from glob import glob

def sub2dict(sub_file:str):
	lines = open(sub_file, 'r').readlines()
	started = False
	lang = ""
	time = ""
	content = ""
	allcontent = {}
	for line in lines:
		if(not started and "Language:" in line):
			lang = '[' +line[:-1].split(' ')[-1]+']'
			print(lang)
			started = True
		elif(started):
			if(len(line)<2):
				if(time != ""):
					allcontent[time] = content
				time = ""
				content = ""
			else:
				if(time == ""):
					time = line
				else:
					content += line

	return lang, allcontent

def combine_srt(lang0:str, lang1:str, outname:str):
	l0, lang0dict = sub2dict(lang0)
	# print(l0)
	l1, lang1dict = sub2dict(lang1)
	outfile = open(outname, 'w')
	for time in lang0dict:
		outfile.write(time)
		outfile.write(l0+' ')
		outfile.write(lang0dict[time])
		outfile.write(l1+' ')
		outfile.write(lang1dict[time])
		outfile.write("\n")
	outfile.close()


if __name__ == "__main__":

	os.system("mkdir new")
	os.chdir("new")
	os.system("youtube-dl --all-subs --sub-format srt "+sys.argv[1])

	lang0 = str(sys.argv[2])
	lang1 = str(sys.argv[3])

	lang0 = glob("*."+lang0+".*")[0]
	lang1 = glob("*."+lang1+".*")[0]
	# print(french)
	# sub2dict(french)
	end = lang0.rfind('.')
	end = lang0[:end].rfind('.')
	print(lang0[:end])
	file_name = lang0[:end]+'.srt'
	combine_srt(lang0, lang1, file_name)

	os.chdir("..")
	dir_name = file_name[:-4].replace(" ", '\\ ')
	os.system('mv new '+dir_name)