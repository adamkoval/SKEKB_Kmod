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

	* run_BetaBeatsrc.py:
	[changed]
	- Changed the argument parser from optparse (deprecated) to argparse.

	
