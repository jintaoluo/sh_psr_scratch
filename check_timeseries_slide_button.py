import astropy.io.fits as pyfits
import numpy as np
import pylab as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import sys

#--------------------------------------------------------
print '\n**************************************************************'
print '                  check_timeseries_slide_button.py'
print 'This program is desigined to view an amount of timeseries in a determined channel'
print 'of a PSRFITS file in search mode'
print	'                   By Jintao Luo, jluo@nrao.edu'

print	'        \n                           How To:'
print '       Use the slider to jump to the channel you want.'
print '    Or use previous/next button to go the the neighbouring channel     '
print 'chan_index: the index of the channel you want to view'
print 'nof_subint: the total amount of nof_subint you want to view'


#	check correctness of input parameters
if (len(sys.argv) < 4):
	print "\nusage: python check_time_series_slide_button.py file_name chan_index nof_subint\n"
	sys.exit(0)




#--------------------------------------------------------
#	parse parameters: fname & chan_index & nof_subint
print '\n----------------------------------------------------------------'
print '                      Input information:'
fname = sys.argv[ 1 ]
print '\nfile_name:  ' + fname

chan_index = int(sys.argv[ 2 ])
print '\nindex of freq chan to check:  ' + str(chan_index)

nof_subint = int(sys.argv[ 3 ])
print '\nnumber of subint to check:  ' + str(nof_subint)
print '----------------------------------------------------------------\n'

#----------------------------------------------
# open the psrfits file
hdulist = pyfits.open( fname )

hd_sub = hdulist['subint']
xxxx = hd_sub.data['DATA']

#nof_subint = len(hd_sub.data)

TSUBINT = hd_sub.data['TSUBINT'][0]
tsamp = hd_sub.header['tbin']
CHAN_BW = hd_sub.header['chan_bw']
NCHAN = hd_sub.header['nchan']
NSBLK = hd_sub.header['nsblk']



#----------------------------------------------
# make the initial plot
freq_index = hd_sub.data['dat_freq'][0]
t_index = np.arange( NSBLK * nof_subint ) * tsamp

data_v = np.arange( NSBLK * nof_subint )

for n in range( nof_subint ):		
	#data_v[ n * NSBLK : (n+1) * NSBLK ] = xxxx[ n, :, 0, chan_index, 0]* 1.0
	data_v[ n * NSBLK : (n+1) * NSBLK ] = xxxx[ n, :, 0, chan_index, 0]* 1.0

print 'current chan_index: ' + str(chan_index) + ',    Freq(MHz): ' + str(freq_index[chan_index]) + ',    BW(MHz): ' + str( CHAN_BW )

fig, ax = plt.subplots()
#plt.subplots_adjust(left=0.25, bottom=0.25)
plt.subplots_adjust(left=0.1, bottom=0.25)
l, = plt.plot( t_index, data_v, '-' )
plt.xlabel( 'Time(sec)' )
plt.ylabel( 'Raw Amp' )



#----------------------------------------------
# set up the slider
axcolor = 'lightgoldenrodyellow'
a0 = 5
f0 = 3

axamp  = plt.axes([0.25, 0.15, 0.65, 0.03], axisbg=axcolor)
samp = Slider(axamp, 'Chan_index', 0, NCHAN, valinit=chan_index)

def update(val):
    global chan_index
    amp = samp.val    
    chan_index = int(amp)
    print '\nchan_index: ' + str(chan_index)
    for n in range( nof_subint ):		
    	data_v[ n * NSBLK : (n+1) * NSBLK ] = xxxx[ n, :, 0, chan_index, 0]* 1.0
    ydata=data_v
    l.set_ydata(ydata)
    plt.draw()
    print 'current chan_index: ' + str(chan_index) + ',    Freq(MHz): ' + str(freq_index[chan_index]) + ',    BW(MHz): ' + str( CHAN_BW )
samp.on_changed(update)



#----------------------------------------------
# set up the buttons
class Index:
    ind = 0
    def next(self, event):
        global chan_index
        self.ind = chan_index
        self.ind += 1
        i = self.ind % NCHAN
        chan_index = i
        print '\nchan_index: ' + str(chan_index)
        for n in range( nof_subint ):		
        	data_v[ n * NSBLK : (n+1) * NSBLK ] = xxxx[ n, :, 0, i, 0]* 1.0
        ydata=data_v
        l.set_ydata(ydata)
        plt.draw()
        print 'current chan_index: ' + str(chan_index) + ',    Freq(MHz): ' + str(freq_index[chan_index]) + ',    BW(MHz): ' + str( CHAN_BW )

    def prev(self, event):
        global chan_index
        self.ind = chan_index
        self.ind -= 1
        i = self.ind % NCHAN
        chan_index = i
        print '\nchan_index: ' + str(chan_index)
        for n in range( nof_subint ):		
        	data_v[ n * NSBLK : (n+1) * NSBLK ] = xxxx[ n, :, 0, i, 0]* 1.0
        ydata=data_v
        l.set_ydata(ydata)
        plt.draw()
        print 'current chan_index: ' + str(chan_index) + ',    Freq(MHz): ' + str(freq_index[chan_index]) + ',    BW(MHz): ' + str( CHAN_BW )



callback = Index()
axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
bnext = Button(axnext, 'Next\nChan')
bnext.on_clicked(callback.next)
bprev = Button(axprev, 'Previous\nChan')
bprev.on_clicked(callback.prev)

plt.show()

