# SKEKB_Kmod
A collection of scripts used for analysis of SuperKEKB turn-by-turn data.

# Basic info
1) This package makes use of the Beta-Beat.src package created by the OMC group at CERN. Please first clone this package into your working directory and direct the SKEKB_Kmod package towards it by editing the pathnames.txt file.
Beta-Beat.src package repo: https://github.com/pylhc/Beta-Beat.src
2) Make sure to edit the pathnames.txt file before running the code. Include your own paths to everything.
3) Run get_bpm_data.py. 
	Output directories of interest are:
	- harmonic_output
	- phase_output
	Output files of interest are:
	- simulationModulation.txt
	- twiss_moni.dat
	- twiss_all.dat
