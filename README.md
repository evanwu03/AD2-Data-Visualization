This script is capable of generating plots for three devices on the AD2 and can generate IV curves. Data visualization is performed by a combination of the `matplotlib` and `pandas` library.
* Oscilloscope (up to three waveforms per plot)
* Vector Network Analyzer
* Impedance Analyzer 
* IV curves

As the class progresses, this script will be updated to include functionality for additional devices used in the class. 
`parameter_requirements.txt` provides a template for setting different attributes for your plot that you provide to the program. 
At the moment, the script uses default values but will be revamped at some point in the future. At the moment, users can provide 
the path to their csv file of the data they want plotted, select the device type, and the directory to save the plot to.  
