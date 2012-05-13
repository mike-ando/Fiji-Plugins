"""Image Wide Analysis

This script runs through a directory of saved stack files and take the whole image measurement. 

"""

import os
import glob
import ij

roi_manager = ij.plugin.frame.RoiManager().getInstance()
folder = ij.io.DirectoryChooser("Select the montage folder").getDirectory()
os.chdir(folder)
names = glob.glob('PID*_Aligned_*.tif')

for name in names:
    open_path = os.path.join(folder, name)
    implus = ij.ImagePlus(open_path)
    implus.show()
    ij.IJ.run("Select All")
    ij.IJ.run("Add to Manager")
    for slice in range(implus.getStackSize()):
        implus.setSlice(slice+1)
        roi_manager.runCommand("Measure")
    implus.close()
    ij.plugin.frame.RoiManager().getInstance().runCommand("Delete")
