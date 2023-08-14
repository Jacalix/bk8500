import sys, dcload
err = sys.stderr.write

def TalkToLoad(load, port, baudrate):
    '''load is either a COM object or a DCLoad object.  They have the 
    same interface, so this code works with either.
 
    port is the COM port on your PC that is connected to the DC load.
    baudrate is a supported baud rate of the DC load.
    '''
    def test(cmd, results):
        if results:
            print cmd, "failed:"
            print "  ", results
            exit(1)
        else:
            print cmd
    load.Initialize(port, baudrate) # Open a serial connection
    print "Time from DC Load =", load.TimeNow()
    test("Set to remote control", load.SetRemoteControl())
    test("Set max current to 3 A", load.SetMaxCurrent(3))
    test("Set CC current to 0.2 A", load.SetCCCurrent(0.2))
    print "Settings:"
    print "  Mode                =", load.GetMode()
    print "  Max voltage         =", load.GetMaxVoltage()
    print "  Max current         =", load.GetMaxCurrent()
    print "  Max power           =", load.GetMaxPower()
    print "  CC current          =", load.GetCCCurrent()
    print "  CV voltage          =", load.GetCVVoltage()
    print "  CW power            =", load.GetCWPower()
    print "  CR resistance       =", load.GetCRResistance()
    print "  Load on timer time  =", load.GetLoadOnTimer()
    print "  Load on timer state =", load.GetLoadOnTimerState()
    print "  Trigger source      =", load.GetTriggerSource()
    print "  Function            =", load.GetFunction()
    print "  Input values:" 
    values = load.GetInputValues()
    for value in values.split("\t"): print "    ", value
    print "  Product info:"
    values = load.GetProductInformation()
    for value in values.split("\t"): print "    ", value
    test("Set to local control", load.SetLocalControl())

def main():
    port = '/dev/ttyS4' # COM1 in Windows Subsystem for Linux
    baudrate = 38400 # Be sure to match this setting in the BK 8500 Config
    load = dcload.DCLoad()
    TalkToLoad(load, port, baudrate)
    return 0

main()
