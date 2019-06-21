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
	[changed]
	- Changed name of output_dir to main_output_dir, all through the script.

	* func.py:
	[added]
	- The function get_dict().
	- The function get_dict_colormap().
	- The function get_data_column().
	[changed]
	- Name of get_dict() for get_dict_schematic().

	* pathnames.txt:
	[changed]
	- Changed name of output_dir to main_output_dir

	* checkBPMs_schematic.py:
	[added]
	- Wrote the main portion of the script which will display the BPM fix schematic.
	- sys.exit() command at the end.
	[changed]
	- Changed references to func get_dict to get_dict_schematic, in accordance with
	change within func.py.
	- Changed name to checkBPMs_schematic.py.
	- Changed some definitions.

	* checkBPMs_colormap.py:
	[added]
	- Main script.


2019-06-12	Adam Koval	adam.koval@cern.ch

	* checkBPMs_schematic.py:
	[changed]
	- Formatting.

	* checkBPMs_colormap.py:
	[changed]
	- Formatting.

	* get_bpm_data.py:
	[added]
	- checkBPMs_colormap/schematic.py functionality. (UNFINISHED)


2019-06-13	Adam Koval	adam.koval@cern.ch

	* checkBPMs_schematic.py:
	[changed]
	- Destination for output .png figures.
	[fixed]
	- async_output_dir definition to not include the main_output_dir, 
	as this was already compensated for in get_bpm_data.py
	[added]
	- Script completion message at the end.
	- Argument option to display plot.

	* checkBPMs_colormap.py:
	[changed]
	- Destination for output .png figures.
	[fixed]
	- phase_output_dir definition to not include the main_output_dir, 
	as this was already compensated for in get_bpm_data.py.
	- Trying to obtain DELTAPHASEX even for y-axis.
	[added]
	- Script completion message at the end.
	- Argument option to display plot.

	* get_bpm_data.py:
	[added]
	- checkBPMs_colormap/schematic.py functionality (BEFORE DEBUG).
	- checkBPMs_colormap/schematic.py after the fix has been applied.
	[fixed]
	- Incorrect argument passed to checkBPMs_schematic.py for async_output_dir.

	* run_BetaBeatsrc.py:
	[fixed]
	- add_option to add_argument, in accordance with argparse.

	* func.py:
	[fixed]
	- no "numpy as np" import.


2019-06-14	Adam Koval	adam.koval@cern.ch

	* get_bpm_data.py:
	[changed]
	- Debug option is not an argument --debug/-db when running the script
	from console.

	* main dir:
	[changed]
	- Removed pathnames.txt from git repo, and left only pathnames_sample.txt.
	The user should copy pathnames_sample.txt to pathnames.txt and edit it.


2019-06-20	Adam Koval	adam.koval@cern.ch

	* pathnames.txt:
	[changed]
	- Removed lattice_file and lattice_dir and absorbed them into lattice_path
	variable instead.
	- Removed phase_output_dir and harmonic_output_dir.
	- Renamed data_input_dir to input_data_dir.
	[added]
	- file_dict variable.

	* get_bpm_data.py:
	[changed]
	- Changed definition of phase_output_dir and harmonic_output_dir as per changes to pathnames.txt.
	- Renamed data_input_dir to input_data_dir.
	[added]
	- file_dict variabele.

	* .gitignore:
	[added]
	- Ignoring of any naming of output and temp dirs, as well as pathnames.txt file.

	* func.py:
	[changed]
	- look_for_dict() func now takes argument of file_dict variable.


2019-06-21	Adam Koval	adam.koval@cern.ch

	* get_bpm_data.py:
	[added]
	- pathnames is now an input argument, to allow for use of different
	pathnames files.

	* func.py:
	[added]
	- read_pathnames() function now takes input argument of pathnames.
