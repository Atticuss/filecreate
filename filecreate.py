import sys,threading,argparse

#use a thread to keep terminal writes from slowing down file write speed
class ProgressBar(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.progress = 0
		self.done = False

	def run(self):
		while not self.done:
			#print(self.progress)
			barLength = 10 # Modify this to change the length of the progress bar
			status = ""
			if isinstance(self.progress, int):
				self.progress = float(self.progress)
			if self.progress >= 1:
				self.progress = 1
				status = "Done...\r\n"
			block = int(round(barLength*self.progress))
			text = "\r[{0}] {1:.2f}%".format( "#"*block + "-"*(barLength-block), self.progress*100)
			sys.stdout.write(text)
			sys.stdout.flush()

parser = argparse.ArgumentParser(description='Generate a file.', prog='filecreate.py', usage='%(prog)s -s <size> -o <outfile> [-d <junkdata>]', formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=65, width=150))
parser.add_argument("-s", "--size", action='store', help="Size of outfile in MB")
parser.add_argument("-o", "--outfile", action='store', help="File to write data to")
parser.add_argument("-d", "--junkdata", action='store', help="Junk data to fill file with (default is: // junk data //)")
args = parser.parse_args()

outfile = args.outfile
size = float(args.size)

if args.junkdata:
	data = args.junkdata.encode()
else:
	data = b"// junk data //\n"

print('[*] Creating %sMB file'%size)

with open(outfile,'wb') as f:
	size *= 1024*1024
	written = 0
	updated = False
	t = ProgressBar()
	t.start()

	try:
		while written < size:
			f.write(data)
			written += len(data)
			t.progress = float(written/size)

		t.done = True
		print('\n[*] Finished.')
	except KeyboardInterrupt:
		t.done = True
		print('\n[*] Cancelled')
