"""Vesicle Distance
Author: Mike Ando

Partially modeled off of Wayne Rasband's Path Writer.

This is a script I created for a labmate who wanted to measure the
shortest distances of vesicles from the post-synaptic density(PSD) in
electron microscope images.

This script expects an image with ROIs selected. A point ROI is
expected for the vesicle and a Freehand Line Roi is expected for the
PSD. It uses the scale calibration of the image to output distances in
the appropriate units. It can handle images which have a different scale for the x and y axis. 

This is meant to be run from the Jython Interpreter with

import vesicle_distance
vesicle_distance.analyze()
"""

import ij


def analyze():
    """ This is the main function which does the minimum distance
    analysis"""
    import math

    # Get the ROI manager and current image
    rm = ij.plugin.frame.RoiManager().getInstance()
    imp = ij.WindowManager.getCurrentImage()

    # Set the calibration using the embedded scale information
    cal = imp.getCalibration()

    # Log the title of the image, the calibration, and two column
    # headings of Roi coordinates and Minimum distance
    ij.IJ.log(imp.getTitle())
    ij.IJ.log("The calibration is " + cal.toString())
    ij.IJ.log( "Roi Coordinates \t Minimum Distance")
    
    # Get the list of rois
    rois = rm.getRoisAsArray()

    # Populate the line (PSD) list and point (vesicle) list. Although
    # it takes a line array, it only looks at the first line. 

    line = [roi for roi in rois if roi.isLine()]
    points = [roi for roi in rois if roi.isLine() == False & roi.isArea() == False]

    # Convert the coordinates in the line and point ROIs into scaled
    # coordinates
    calibrated_line = get_roi_points(line[0], cal)
    calibrated_points = [get_roi_points(point, cal)[0] for point in points]
    # Make an even set of points on the line
    psd = get_even(calibrated_line, cal)

    min = []

    # For each point, find the minimum distance to the line
    for point in calibrated_points:
        # Initialize current minimum distance to first point in line
        current_min  = dist(point, psd[0])
        for part in psd:
            current_dist = dist(point, part)
            if current_dist < current_min:
                current_min = current_dist
        min.append( (point, current_min) )

    # Output the results to the log
    for result in min:
        roi_name = str(result[0])
        min_distance = str(result[1])
        ij.IJ.log(roi_name + '\t' + min_distance)

def get_roi_points(roi, cal):
    """ This returns the roi points where the coordinates are in the
    scaled units of the image rather than pixels. """
    # Get the polygon for the roi
    polygon = roi.getFloatPolygon()
    # Extract the x and y points
    x = polygon.xpoints
    y = polygon.ypoints
    # Convert the x and y points using the image calibration
    calibrated_x = map(lambda point: cal.getX(point), x)
    calibrated_y = map(lambda point: cal.getY(point), y)
    # Create a list of x,y pairs
    points = zip(calibrated_x, calibrated_y)
    return points

def deltas(point_list):
    """ This function returns the distance, x-coordinates difference,
    and y-coordinate difference of adjacent points in a list"""
    perimeter = []
    delta_x = []
    delta_y = []
    # Calculate the distance, delta x, and delta y
    for i in range(len(point_list)-1):
        perimeter.append(dist(point_list[i+1],point_list[i]))
        delta_x.append(point_list[i+1][0] - point_list[i][0])
        delta_y.append(point_list[i+1][1] - point_list[i][1])
    return perimeter, delta_x, delta_y

def dist(point1, point2):
    """ Calculates euclidean distance between two points"""
    import math
    delta_x = point1[0] - point2[0]
    delta_y = point1[1] - point2[1]
    square = math.pow(delta_x, 2) + math.pow(delta_y, 2)
    total = math.sqrt(square)
    return total

def get_even(points, cal):
    """Get evenly spaced points (the equivalent distance to one pixel
    apart) along a set of points. This was modeled off of Wayne
    Rasband's Path Writer."""
    delta_dist, delta_x, delta_y = deltas(points)
    xpath = []
    ypath = []
    # Create a subset of points which does not include the endpoint
    points_subset = points[:-1]
    for index, point in enumerate(points_subset):
        # If the points are overlapping, ignore
        if delta_dist[index] == 0:
            continue
        # Determine the calibrated step size in the x and y direction
        xinc = cal.getX(delta_x[index]/delta_dist[index])
        yinc = cal.getY(delta_y[index]/delta_dist[index])
        # Set the first incremented point for the original
        xpos = point[0] + xinc
        ypos = point[1] + yinc
        # Extend the list of points until they reach the distance
        # between the original adjacent ROI points
        while(dist(point, (xpos, ypos)) < delta_dist[index]):
              xpath.append(xpos)
              ypath.append(ypos)
              xpos+=xinc
              ypos+=yinc
    even_points = zip(xpath, ypath)
    return even_points



