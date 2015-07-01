import sys,threading

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

outfile = 'test2.txt'
data = b'// nVisium //'
size = 100 #in mb

print('[*] Creating %sMB file'%size)

with open(outfile,'wb') as f:
	size *= 1000*1000
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