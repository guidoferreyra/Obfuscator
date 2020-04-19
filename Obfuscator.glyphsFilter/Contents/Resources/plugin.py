# encoding: utf-8
from __future__ import division, print_function, unicode_literals

###########################################################################################################
#
#
#	Filter without dialog Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Filter%20without%20Dialog
#
#
###########################################################################################################

import objc
from GlyphsApp import *
from GlyphsApp.plugins import *

class Obfuscator(FilterWithoutDialog):
	
	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': u'Obfuscator',
			'de': u'Verschleiern',
			'es': u'Ofuscar',
			'fr': u'Brouiller',
			'pt': u'Ofuscar',
		})
		self.keyboardShortcut = None # keyboard Shortcut

	@objc.python_method
	def notdefLayer( self ):
		try:
			from Foundation import NSBundle, NSClassFromString, NSDictionary
			bundle = NSBundle.bundleForClass_(NSClassFromString("GSExportInstanceOperation"))
			if bundle:
				path = bundle.pathForResource_ofType_("notDef","plist")
				layerDict = NSDictionary.dictionaryWithContentsOfFile_(path)
				layer = GSLayer.alloc().initWithDict_format_(layerDict,1)
				return layer
			return None
		except Exception as e:
			import traceback
			print(traceback.format_exc())
			self.logToConsole( "notdefLayer: %s" % str(e) )
			return None
			

	@objc.python_method
	def filter(self, layer, inEditView, customParameters):

		if len(customParameters) !=0:
			character = customParameters['char']
		else:
			character = '.notdef'

		fuente = layer.parent.parent
		glyphOrigen = fuente.glyphs[character]
		if glyphOrigen is None:
			if inEditView:
				# brings macro window to front and clears its log:
				Glyphs.clearLog()
				Glyphs.showMacroWindow()
			msg="Could not find a glyph with the name: ‘%s’. Defaulting to built-in .notdef." % character
			print("Filter ‘%s’: %s" % (self.menuName, msg))
			# fallback .notdef:
			layerOrigen = self.notdefLayer()
		else:
			# find origin layer:
			layerOrigen = glyphOrigen.layers[layer.layerId]
			if layerOrigen is None:
				layerOrigen = glyphOrigen.layers[layer.master.id]
		
		if not layerOrigen:
			print("")
		else:
			# delete contents of target layer:
			layer.clear()

			# duplicate shapes into target layer:
			try:
				# GLYPHS 3
				for newShape in layerOrigen.shapes:
					layer.shapes.append(newShape.copy())
			except:
				# GLYPHS 2
				for newPath in layerOrigen.paths:
					layer.paths.append(newPath.copy())
		
			# copy spacing and (group) kerning:
			layer.width = layerOrigen.width
			glyph = layer.parent
			if glyphOrigen:
				glyph.leftKerningGroup = glyphOrigen.leftKerningGroup
				glyph.rightKerningGroup = glyphOrigen.rightKerningGroup
			else:
				glyph.leftKerningGroup = None
			glyph.rightKerningGroup = None
	
	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
	