sh_psr_scratch
==============

A scratch of python scripts for pulsar seaching in Shanghai telescope.

##2014-04-29
Upload 2 files:

1. check_spectrum_slide_button.py   
2. check_timeseries_slide_button.py

Launch:

    python check_timeseries_slide_button.py fname.fits 10 100
    ( 10: the index of channel you want to view;     100: total amount of subint you want to check) 
    
    python check_spectrum_slide_button.py fname.fits 100
    ( 100: index of subint you want to view )

Change chan_index/subint_index
    
    On the plot, use the slide bar to jump to the chan_index/subint_index you want
    
    or use the 'previous'/'next' button to  view the neighbour.
