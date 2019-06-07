2019-06-07	Adam Koval	adam.koval@cern.ch

	* pathnames.txt: output_dir to be the directory into which all output is placed.

	* main directory: Moved file_dict.txt into main directory, out of lattice_dir,
	changed all relevant functions/scripts accordingly.
	
	* main directory: Renamed run.py -> run_BetaBeatsrc.py
	
	* get_bpm_data.py: Added a line which checks if variable debug=='yes', if so,
	variable loopend = '2', else variable loopend = 'Length[runs]'. To be passed
	to SAD script.

	* func.py: Added a number of functions relating to other scripts used by the
	package. Still a work in progress.
