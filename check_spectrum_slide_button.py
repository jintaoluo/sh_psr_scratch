import astropy.io.fits as pyfits
import numpy as np
import pylab as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import sys

#--------------------------------------------------------
print '\n**************************************************************'
print '                  check_spectrum_slide_button.py'
print 'This program is desigined to view spectrum of PSRFITS file in search mode'
print	'                   By Jintao Luo, jluo@nrao.edu'

print	'        \n                           How To:'
print '       Use the slider to jump to the Subint_index you want.'
print '    Or use previous/next button to go the the neighbouring subint_index     '

#	check correctness of input parameters
if (len(sys.argv) < 3):
	print "\nusage: python check_spectrum_slide_button.py file_name, input_subt_int_index\n"
	sys.exit(0)

#--------------------------------------------------------
#	parse parameters: fname & chan_index

print '\n----------------------------------------------------------------'
print '                      Input information:'
fname = sys.argv[ 1 ]
print 'file_name:  ' + fname

input_subt_int_index = int(sys.argv[ 2 ])
print 'index of freq chan to check:  ' + str(input_subt_int_index)
print '----------------------------------------------------------------\n'



#----------------------------------------------
# open the psrfits file
hdulist = pyfits.open( fname )

hd_sub = hdulist['subint']
xxxx = hd_sub.data['DATA']

nof_subint = len(hd_sub.data)

TSUBINT = hd_sub.data['TSUBINT'][0]
tsamp = hd_sub.header['tbin']
CHAN_BW = hd_sub.header['chan_bw']
NCHAN = hd_sub.header['nchan']
NSBLK = hd_sub.header['nsblk']



#----------------------------------------------
# make the initial plot
freq_index = hd_sub.data['dat_freq'][0]

data_v = np.arange( NCHAN )
data_v = xxxx[ 0, 0, 0, :, 0 ] #  xxxx.shape : (158, 8192, 4, 1024, 1) ( nof_subint, NSBLK, npol, nchan, 1 )
ax = plt.subplot( 111 )
plt.subplots_adjust(left=0.1, bottom=0.25)
l, = plt.plot( freq_index, data_v )
plt.xlabel( 'Freq(MHz)' )
plt.ylabel( 'Raw Amp' )

#----------------------------------------------
# set up the slider
axcolor = 'lightgoldenrodyellow'
a0 = 5
f0 = 3

axamp  = plt.axes([0.25, 0.15, 0.65, 0.03], axisbg=axcolor)
samp = Slider(axamp, 'Subint_index', 0, NSBLK*nof_subint, valinit=10)

subint_index = input_subt_int_index

def update(val):
    global subint_index
    amp = samp.val    
    subint_index = int(amp)
    print '\nsubint_index: ' + str(subint_index)   
    main_index = int(subint_index / NSBLK)
    sub_index = subint_index % NSBLK
    data_v = xxxx[ main_index, sub_index, 0, :, 0 ]
    ydata=data_v
    l.set_ydata(ydata)
    plt.draw()
    print 'current subint_index: ' + str(subint_index) 
samp.on_changed(update)



#----------------------------------------------
# set up the buttons
class Index:
    ind = 0
    def next(self, event):
        global subint_index
        self.ind = subint_index
        self.ind += 1
        i = self.ind % (NSBLK * nof_subint)
        subint_index = i
        print '\nsubint_index: ' + str(subint_index)
        main_index = int(subint_index / NSBLK)
        sub_index = subint_index % NSBLK
        data_v = xxxx[ main_index, sub_index, 0, :, 0 ]
        ydata=data_v
        l.set_ydata(ydata)
        plt.draw()
        print 'current subint_index: ' + str(subint_index) 

    def prev(self, event):
        global subint_index
        self.ind = subint_index
        self.ind -= 1
        i = self.ind % (NSBLK * nof_subint)
        subint_index = i
        print '\nsubint_index: ' + str(subint_index)
        main_index = int(subint_index / NSBLK)
        sub_index = subint_index % NSBLK
        data_v = xxxx[ main_index, sub_index, 0, :, 0 ]
        ydata=data_v
        l.set_ydata(ydata)
        plt.draw()
        print 'current subint_index: ' + str(subint_index) 



callback = Index()
axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
bnext = Button(axnext, 'Next \nsub_int')
bnext.on_clicked(callback.next)
bprev = Button(axprev, 'Previous \nsub_int')
bprev.on_clicked(callback.prev)




plt.show()


