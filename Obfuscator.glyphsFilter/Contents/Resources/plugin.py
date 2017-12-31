# encoding: utf-8

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

from GlyphsApp import *
from GlyphsApp.plugins import *

class Obfuscator(FilterWithoutDialog):
	
	def settings(self):
		self.menuName = Glyphs.localize({'en': u'Obfuscator', 'de': u'Obfuscator'})
		self.keyboardShortcut = None # keyboard Shortcut

	def filter(self, layer, inEditView, customParameters):

		if len(customParameters) !=0:
			character = customParameters['char']
		else:
			character = 'apple'

		fuente = layer.parent.parent
		layerId = layer.layerId
		glyph = fuente.glyphs[character]
		if glyph is None:
			if inEditView:
				Message("Missing Glyph", "Please add a glyph with the name: \"%s\" or set the correct name in the Filter parameter" % character)
			else:
				print "Obfuscator: Please add a glyph with the name: \"%s\" or set the correct name in the Filter parameter" % character
			return
		layerOrigen = fuente.glyphs[character].layers[layerId]
		LSBOrigen = layerOrigen.LSB
		RSBOrigen = layerOrigen.RSB

		pathsOrigen = []
		for path in layerOrigen.paths:
			pathsOrigen.append(path)
		
		if layer.paths:
			for i in range( len( layer.paths ))[::-1]:
				del layer.paths[i]
		elif layer.components:
			for i in range( len( layer.components ))[::-1]:
				del layer.components[i]

		for newPath in pathsOrigen:
			layer.paths.append(newPath)
		
		layer.LSB = LSBOrigen
		layer.RSB = RSBOrigen
	
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
	