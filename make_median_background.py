import ij
import background as b
import os
import glob

timepoint_start = 11
timepoint_end = 11
path = "/Users/work/Desktop/Current_Desktop/Imaging/20120930_MitoHalf/RFP"

for timepoint in range(timepoint_start, timepoint_end+1):
	name_search = "PID*T" + str(timepoint) + "_*.tif"

	os.chdir(path)
	names = glob.glob(name_search)

	print "Opening files for timepoint " + str(timepoint)
	loi = [ImagePlus(os.path.join(path ,name)) for name in names]

	print "Finding Median"
	illuminated_background = b.make_illuminated(loi)
	background_name = "T" + str(timepoint) + "_background.tif"
	background_path = os.path.join(path, background_name)
	ij.IJ.save(illuminated_background, background_path)
	