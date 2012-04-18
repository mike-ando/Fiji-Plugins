""" Apply threshold:

This script expects a stack of two images. The first image is the
morphology image and the second image is the reporter image. The stack
must be the currently selected image when this script is run.

This script creates a mask from a morphology image to generate a
ROI. It then applies the ROI to a reporter image and measures the
result.

This script does not modify the original image.

"""

def analyze():
    import ij

    #Clear ROI

    roi_manager = ij.plugin.frame.RoiManager().getInstance()
    if roi_manager.getCount() > 0:
        roi_manager.runCommand("Select All")
        roi_manager.runCommand("Delete")

    # Get Image

    w = ij.WindowManager
    stack = w.getCurrentImage()

    # Create new image of morphology slice

    stack.setSlice(1)
    morph_ip = stack.getProcessor()
    morph = ij.ImagePlus("Morphology", morph_ip)
    morph.show()

    # Background subtract
    ij.IJ.selectWindow("Morphology")
    ij.IJ.run("Subtract Background...", "rolling=50 sliding")

    # Apply Threshold
    ij.IJ.selectWindow("Morphology")
    ij.IJ.run("Threshold...")
    ij.IJ.run("Convert to Mask")

    # Create ROI
    ij.IJ.selectWindow("Morphology")
    ij.IJ.run("Create Selection")

    # Save selection to ROI
    ij.IJ.run("Add to Manager")
    morph.changes = False
    morph.close()

    # Apply ROI to reporter slice
    stack.setSlice(2)

    # Measure
    roi_manager.runCommand("Measure")


