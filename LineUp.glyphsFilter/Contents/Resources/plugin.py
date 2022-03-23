# encoding: utf-8

###########################################################################################################
#
#
#	Filter without dialog plug-in
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Filter%20without%20Dialog
#
#
###########################################################################################################

from __future__ import division, print_function, unicode_literals
import objc, math
from GlyphsApp import *
from GlyphsApp.plugins import *
from AppKit import NSAffineTransform, NSAffineTransformStruct

def transform(shiftX=0.0, shiftY=0.0, rotate=0.0, skew=0.0, scale=1.0):
	"""
	Returns an NSAffineTransform object for transforming layers.
	Apply an NSAffineTransform t object like this:
		Layer.transform_checkForSelection_doComponents_(t,False,True)
	Access its transformation matrix like this:
		tMatrix = t.transformStruct() # returns the 6-float tuple
	Apply the matrix tuple like this:
		Layer.applyTransform(tMatrix)
		Component.applyTransform(tMatrix)
		Path.applyTransform(tMatrix)
	Chain multiple NSAffineTransform objects t1, t2 like this:
		t1.appendTransform_(t2)
	"""
	myTransform = NSAffineTransform.transform()
	if rotate:
		myTransform.rotateByDegrees_(rotate)
	if scale != 1.0:
		myTransform.scaleBy_(scale)
	if not (shiftX == 0.0 and shiftY == 0.0):
		myTransform.translateXBy_yBy_(shiftX,shiftY)
	if skew:
		skewStruct = NSAffineTransformStruct()
		skewStruct.m11 = 1.0
		skewStruct.m22 = 1.0
		skewStruct.m21 = math.tan(math.radians(skew))
		skewTransform = NSAffineTransform.transform()
		skewTransform.setTransformStruct_(skewStruct)
		myTransform.appendTransform_(skewTransform)
	return myTransform

def calculateAngle( firstPoint, secondPoint ):
	"""
	Returns the angle (in degrees) of the straight line between firstPoint and secondPoint,
	0 degrees being the second point to the right of first point.
	firstPoint, secondPoint: must be NSPoint or GSNode
	"""
	xDiff = secondPoint.x - firstPoint.x
	yDiff = secondPoint.y - firstPoint.y
	return math.degrees(math.atan2(yDiff,xDiff))

class LineUp(FilterWithoutDialog):
	
	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': 'Line Up Selection',
			'de': 'Punkte auffädeln',
			# 'fr': 'Mon filtre',
			'es': 'Formar línea',
			'pt': 'Formar linha',
			'jp': '直︀線︀化︀',
			'ko': '직선화',
			'zh': '📐选中点直线对齐',
			})

	@objc.python_method
	def filter(self, layer, inEditView, customParameters):
		if inEditView and layer.selection:
			points = [item for item in layer.selection if type(item) in (GSNode, GSAnchor)]
			if len(points) > 2:
				if layer.selectionBounds.size.width > layer.selectionBounds.size.height:
					points = sorted( points, key = lambda thisListItem: thisListItem.x )
				else:
					points = sorted( points, key = lambda thisListItem: thisListItem.y )
	
				firstPoint = points[0]
				lastPoint = points[-1]
				angle = calculateAngle( firstPoint, lastPoint )
				rotation = transform(rotate=-angle).transformStruct()
				layer.applyTransform(rotation)
				alignX = firstPoint.x == lastPoint.x

				for point in points[1:-1]:
					if alignX:
						point.x = firstPoint.x
					else:
						point.y = firstPoint.y
		
				rotationBack = transform(rotate=angle).transformStruct()
				layer.applyTransform(rotationBack)

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
