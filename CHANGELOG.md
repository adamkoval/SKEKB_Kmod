2019-06-07	Adam Koval	adam.koval@cern.ch

	* pathnames.txt: 
	[changed] 
	- output_dir to be the directory into which all output is placed.

	* main directory: 
	[changed] 
	- Moved file_dict.txt into main directory, out of lattice_dir, and
 	adapted all relevant functions/scripts accordingly.
	
	* main directory: 
	[changed] 
	- Renamed run.py -> run_BetaBeatsrc.py
	
	* get_bpm_data.py: 
	[added]
	- Added a line which checks if variable debug=='yes'. If so, variable
	loopend = '2', else variable loopend = 'Length[runs]'. To be passed
	to SAD script.

	* func.py: 
	[added]
	- Added a number of functions (phase(), phasetot(), BPMs_from_sdds()),
	related to checking for async BPMs. Still a work in progress.


2019-06-11	Adam Koval	adam.koval@cern.ch

	* async.py: 
	[changed]
	- Changed the argument parser from optparse (deprecated) to argparse.
	- Changed naming of variables phase_output_dir and async_output_dir to
	pod and aod resp..
	[added]
	- Added abbreviated/short arg options.
	- Comments.

	* run_BetaBeatsrc.py:
	[changed]
	- Changed the argument parser from optparse (deprecated) to argparse.
	- Changed naming of variables phase_output_dir and harmonic_output_dir
	to pod and hod resp..
	[added]
	- Added abbreviated/short arg options.
	- Comments.

	* get_bpm_data.py:
	[fixed]
	- run.sad was not reading in async BPM list specific to each run, but
	was instead looking for a single file called BPMlist.txt in dir lattice/.
	This has been fixed.

	* func.py:
	[added]
	- Added the function get_dict(). 
