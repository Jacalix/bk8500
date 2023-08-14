import csv, datetime, dcload, numpy, re, time

pts = 5 # generate an IV curve of this many points

# get a string of the current readout for voltage, current, and power
def  getVals():

	time = datetime.datetime.now() # get time
	time.strftime('%x %X') 		   # convert time to string
	
	vals = load.GetInputValues() # get voltage, current, and power
	
	# regex stuff
	vals = re.split(r'\t+', vals) # regex split at tab delimeters
	vals = vals[0:3] # get rid of irrelevant bytes
	# regex to keep only decimal values
	for x in xrange(0,3):
		vals[x] = re.sub(r'[^\d.]+', '', vals[x])
	
	# insert the time at the beginning of the list of return values
	vals.insert(0, time)
	
	return vals

port = '/dev/ttyS1' # COM1 in Windows Subsystem for Linux
baudrate = 38400 # Be sure to match this setting in the BK 8500 Config

load = dcload.DCLoad() # construct the DC load object
load.Initialize(port, baudrate) # initialize communication
load.SetRemoteControl() # enable remote control

minVoltage = 0.1 # mininum settable voltage

# press enter once the shutter is open
raw_input('\nPress Enter to continue...\n')

vals = getVals() # get values
openCircuitVoltage = float(vals[1]) # get the voltage string as a float
# generate a linearly-spaced vector of voltage values to set in the loop
V = numpy.linspace(minVoltage, openCircuitVoltage, pts)

with open('test.csv', 'wb') as file: # prepare to write to CSV
	for x in xrange(pts): # for each point
		
		load.SetCVVoltage(V[x]) # set the constant voltage
		
		# press enter once the shutter is open
		raw_input('\nPress Enter to continue...\n')
		
		load.TurnLoadOn() # turn on the load
		time.sleep(1) # wait for stabilization
		vals = getVals() # get the voltage, current, and power
		load.TurnLoadOff() # turn off the load
		
		writer = csv.writer(file, dialect='excel') # instantiate writer
		writer.writerow(vals) # write this row of results