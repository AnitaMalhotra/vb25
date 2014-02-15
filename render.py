'''

  V-Ray/Blender

  http://vray.cgdo.ru

  Author: Andrey M. Izrantsev (aka bdancer)
  E-Mail: izrantsev@cgdo.ru

  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  as published by the Free Software Foundation; either version 2
  of the License, or (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.

  All Rights Reserved. V-Ray(R) is a registered trademark of Chaos Software.

'''


''' Python modules  '''
import datetime
import math
import os
import string
import subprocess
import sys
import tempfile
import time
import random

import threading
from threading import Timer


''' Blender modules '''
import bpy
import mathutils

''' vb modules '''
import _vray_for_blender

import vb25
from vb25.lib     import VRayProcess
from vb25.utils   import *
from vb25.plugins import *
from vb25.texture import *
from vb25.nodes   import *
from vb25 import dbg


VERSION = '2.5'


LIGHT_PARAMS= { # TEMP! REMOVE!
	'LightOmni': (
		'enabled',
		#'color_tex',
		'shadows',
		'shadowColor',
		#'shadowColor_tex',
		'shadowBias',
		#'photonSubdivs',
		'causticSubdivs',
		#'diffuseMult',
		'causticMult',
		'cutoffThreshold',
		'affectDiffuse',
		'affectSpecular',
		'bumped_below_surface_check',
		'nsamples',
		'diffuse_contribution',
		'specular_contribution',
		#'units',
		'intensity',
		#'intensity_tex',
		'shadowRadius',
		'areaSpeculars',
		'shadowSubdivs',
		'decay'
	),

	'LightAmbient': (
		'enabled',
		#'color',
		'shadowBias',
		'decay',
		'ambientShade',
	),

	'LightSphere': (
		'enabled',
		#'color_tex',
		'shadows',
		'shadowColor',
		#'shadowColor_tex',
		'shadowBias',
		#'photonSubdivs',
		'causticSubdivs',
		#'diffuseMult',
		'causticMult',
		'cutoffThreshold',
		'affectDiffuse',
		'affectSpecular',
		'bumped_below_surface_check',
		'nsamples',
		'diffuse_contribution',
		'specular_contribution',
		#'units',
		'intensity',
		#'intensity_tex',
		'subdivs',
		'storeWithIrradianceMap',
		'invisible',
		'affectReflections',
		'noDecay',
		'radius',
		'sphere_segments'
	),

	'LightRectangle': (
		'enabled',
		#'color_tex',
		'shadows',
		'shadowColor',
		#'shadowColor_tex',
		'shadowBias',
		#'photonSubdivs',
		'causticSubdivs',
		#'diffuseMult',
		'causticMult',
		'cutoffThreshold',
		'affectDiffuse',
		'affectSpecular',
		'bumped_below_surface_check',
		'nsamples',
		'diffuse_contribution',
		'specular_contribution',
		#'units',
		'intensity',
		#'intensity_tex',
		'subdivs',
		'storeWithIrradianceMap',
		'invisible',
		'affectReflections',
		'doubleSided',
		'noDecay',
	),

	'LightDirectMax': (
		'enabled',
		#'color_tex',
		'shadows',
		'shadowColor',
		#'shadowColor_tex',
		'shadowBias',
		#'photonSubdivs',
		'causticSubdivs',
		#'diffuseMult',
		'causticMult',
		'cutoffThreshold',
		'affectDiffuse',
		'affectSpecular',
		'bumped_below_surface_check',
		'nsamples',
		'diffuse_contribution',
		'specular_contribution',
		'intensity',
		#'intensity_tex',
		'shadowRadius',
		'areaSpeculars',
		'shadowSubdivs',
		'fallsize',
	),

	'SunLight': (
		'turbidity',
		'ozone',
		'water_vapour',
		'intensity_multiplier',
		'size_multiplier',
		#'up_vector',
		'invisible',
		'horiz_illum',
		#'sky_model',
		'shadows',
		#'atmos_shadows',
		'shadowBias',
		'shadow_subdivs',
		'shadow_color',
		#'shadow_color_tex',
		#'photon_radius',
		#'photonSubdivs',
		'causticSubdivs',
		#'diffuseMult',
		'causticMult',
		'enabled'
	),

	'LightIESMax': (
		'enabled',
		'intensity',
		#'color_tex',
		'shadows',
		'shadowColor',
		#'shadowColor_tex',
		'shadowBias',
		#'photonSubdivs',
		'causticSubdivs',
		#'diffuseMult',
		'causticMult',
		'cutoffThreshold',
		'affectDiffuse',
		'affectSpecular',
		'bumped_below_surface_check',
		'nsamples',
		'diffuse_contribution',
		'specular_contribution',
		'shadowSubdivs',
		'ies_file',
		#'filter_color',
		'soft_shadows',
		#'area_speculars'
	),

	'LightDome': (
		'enabled',
		#'color_tex',
		'shadows',
		'shadowColor',
		#'shadowColor_tex',
		'shadowBias',
		#'photonSubdivs',
		'causticSubdivs',
		#'diffuseMult',
		'causticMult',
		'cutoffThreshold',
		'affectDiffuse',
		'affectSpecular',
		'bumped_below_surface_check',
		'nsamples',
		'diffuse_contribution',
		'specular_contribution',
		#'channels',
		#'channels_raw',
		#'channels_diffuse',
		#'channels_specular',
		#'units',
		'intensity',
		#'intensity_tex',
		'subdivs',
		#'storeWithIrradianceMap',
		'invisible',
		'affectReflections',
		#'dome_tex',
		#'use_dome_tex',
		#'tex_resolution',
		#'tex_adaptive',
		'dome_targetRadius',
		'dome_emitRadius',
		'dome_spherical',
		'dome_rayDistance',
		'dome_rayDistanceMode',
	),

	'LightSpot': (
		'enabled',
		#'color_tex',
		'shadows',
		'shadowColor',
		#'shadowColor_tex',
		'shadowBias',
		#'photonSubdivs',
		'causticSubdivs',
		#'diffuseMult',
		'causticMult',
		'cutoffThreshold',
		'affectDiffuse',
		'affectSpecular',
		'bumped_below_surface_check',
		'nsamples',
		'diffuse_contribution',
		'specular_contribution',
		#'units',
		'intensity',
		#'intensity_tex',
		'shadowRadius',
		'areaSpeculars',
		'shadowSubdivs',
		#'coneAngle',
		#'penumbraAngle',
		#'dropOff',
		#'falloffType',
		'decay',
		#'barnDoor',
		#'barnDoorLeft',
		#'barnDoorRight',
		#'barnDoorTop',
		#'barnDoorBottom',
		#'useDecayRegions',
		#'startDistance1',
		#'endDistance1',
		#'startDistance2',
		#'endDistance2',
		#'startDistance3',
		#'endDistance3'
	),
}


'''
  SETTINGS
'''
def write_settings(bus):
	ofile = bus['files']['scene']
	scene = bus['scene']

	VRayScene = scene.vray
	VRayExporter    = VRayScene.exporter
	VRayDR          = VRayScene.VRayDR
	SettingsOutput  = VRayScene.SettingsOutput
	SettingsOptions = VRayScene.SettingsOptions
	Includer        = VRayScene.Includer

	threadCount = scene.render.threads
	if VRayExporter.meshExportThreads:
		threadCount = VRayExporter.meshExportThreads

	PLUGINS['CAMERA']['SettingsCamera'].write(bus)
	PLUGINS['CAMERA']['SettingsMotionBlur'].write(bus)

	for key in PLUGINS['SETTINGS']:
		if key in {'BakeView', 'RenderView'}:
			# Skip some plugins
			continue

		plugin= PLUGINS['SETTINGS'][key]
		if hasattr(plugin, 'write'):
			plugin.write(bus)

	if VRayScene.render_channels_use:
		for render_channel in VRayScene.render_channels:
			if render_channel.use:
				plugin= PLUGINS['RENDERCHANNEL'].get(render_channel.type)
				if plugin:
					try:
						plugin.write(bus, getattr(render_channel,plugin.PLUG), name=render_channel.name)
					except:
						plugin.write(ofile, getattr(render_channel,plugin.PLUG), scene, name=render_channel.name)

	# Preview settings are in different parts of the file,
	# because smth must be set before and smth after.
	if bus['preview']:
		bus['files']['scene'].write("\n// Preview settings")
		bus['files']['scene'].write("\nSettingsDMCSampler {")
		bus['files']['scene'].write("\n\tadaptive_amount= 0.99;")
		bus['files']['scene'].write("\n\tadaptive_threshold= 0.2;")
		bus['files']['scene'].write("\n\tsubdivs_mult= 0.01;")
		bus['files']['scene'].write("\n}\n")
		bus['files']['scene'].write("\nSettingsOptions {")
		bus['files']['scene'].write("\n\tmtl_limitDepth= 1;")
		bus['files']['scene'].write("\n\tmtl_maxDepth= 1;")
		bus['files']['scene'].write("\n\tmtl_transpMaxLevels= 10;")
		bus['files']['scene'].write("\n\tmtl_transpCutoff= 0.1;")
		bus['files']['scene'].write("\n\tmtl_glossy= 1;")
		bus['files']['scene'].write("\n\tmisc_lowThreadPriority= 1;")
		bus['files']['scene'].write("\n}\n")
		bus['files']['scene'].write("\nSettingsImageSampler {")
		bus['files']['scene'].write("\n\ttype= 0;") # Fastest result, but no AA :(
		bus['files']['scene'].write("\n\tfixed_subdivs= 1;")
		bus['files']['scene'].write("\n}\n")

		bus['files']['scene'].write("\nBRDFDiffuse BRDFVRayMtlMAcheckerdark {")
		bus['files']['scene'].write("\n\tcolor=Color(0.1,0.1,0.1);")
		bus['files']['scene'].write("\n}\n")
		bus['files']['scene'].write("\nBRDFDiffuse BRDFVRayMtlMAcheckerlight {")
		bus['files']['scene'].write("\n\tcolor=Color(0.95,0.95,0.95);")
		bus['files']['scene'].write("\n}\n")

	if VRayExporter.draft:
		bus['files']['scene'].write("\n// Draft settings")
		bus['files']['scene'].write("\nSettingsDMCSampler {")
		bus['files']['scene'].write("\n\tadaptive_amount= 0.85;")
		bus['files']['scene'].write("\n\tadaptive_threshold= 0.1;")
		bus['files']['scene'].write("\n\tsubdivs_mult= 0.1;")
		bus['files']['scene'].write("\n}\n")

	for key in bus['filenames']:
		if key in {'output', 'output_filename', 'output_loadfile', 'lightmaps', 'scene', 'DR'}:
			# Skip some files
			continue
		if VRayDR.on and not SettingsOptions.misc_transferAssets:
			if VRayDR.type == 'WW':
				ofile.write("\n#include \"//%s/%s/%s/%s\"" % (HOSTNAME, VRayDR.share_name, bus['filenames']['DR']['sub_dir'], os.path.basename(bus['filenames'][key])))
			else:
				ofile.write("\n#include \"%s\"" % (bus['filenames']['DR']['prefix'] + os.sep + os.path.basename(bus['filenames'][key])))
		else:
			if bus['preview'] and key in {'colorMapping'}:
				if key == 'colorMapping':
					if os.path.exists(bus['filenames'][key]):
						ofile.write("\n#include \"%s\"" % bus['filenames'][key])
				# if key == 'geometry':
				# 	ofile.write("\n#include \"%s\"" % os.path.join(get_vray_exporter_path(), "preview", "preview_geometry.vrscene"))
			else:
				ofile.write("\n#include \"%s\"" % os.path.basename(bus['filenames'][key]))
	ofile.write("\n")

	if Includer.use:
		ofile.write("\n// Include additional *.vrscene files")
		for includeNode in Includer.nodes:
			if includeNode.use == True:
				ofile.write("\n#include \"" + bpy.path.abspath(includeNode.scene) + "\"\t\t // " + includeNode.name)


'''
  MATERIALS & TEXTURES
'''
def write_lamp_textures(bus):
	scene= bus['scene']
	ofile= bus['files']['lights']
	ob=    bus['node']['object']

	VRayScene=    scene.vray
	VRayExporter= VRayScene.exporter

	la= ob.data
	VRayLamp= la.vray

	defaults= {
		'color':       (a(scene,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(la.color)),               0, 'NONE'),
		'intensity':   (a(scene,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple([VRayLamp.intensity]*3)), 0, 'NONE'),
		'shadowColor': (a(scene,"AColor(%.6f,%.6f,%.6f,1.0)"%tuple(VRayLamp.shadowColor)),   0, 'NONE'),
	}

	bus['lamp_textures']= {}

	for i,slot in enumerate(la.texture_slots):
		if slot and slot.texture and slot.texture.type in TEX_TYPES:
			VRaySlot=    slot.texture.vray_slot
			VRayLight=   VRaySlot.VRayLight

			for key in defaults:
				use_slot= False
				factor=   1.0

				if getattr(VRayLight, 'map_'+key):
					use_slot= True
					factor=   getattr(VRayLight, key+'_mult')

				if use_slot:
					if key not in bus['lamp_textures']: # First texture
						bus['lamp_textures'][key]= []
						if factor < 1.0 or VRaySlot.blend_mode != 'NONE' or slot.use_stencil:
							bus['lamp_textures'][key].append(defaults[key])

					bus['mtex']= {}
					bus['mtex']['dome'] = True if la.type == 'HEMI' else False
					bus['mtex']['mapto']=   key
					bus['mtex']['slot']=    slot
					bus['mtex']['texture']= slot.texture
					bus['mtex']['factor']=  factor
					bus['mtex']['name'] = clean_string(get_name(slot.texture, prefix='TE'))

					# Write texture
					if bus['mtex']['name'] in bus['cache']['textures']:
						bus['lamp_textures'][key].append( [stack_write_texture(bus),
														   slot.use_stencil,
														   VRaySlot.blend_mode] )

	if VRayExporter.debug:
		if len(bus['lamp_textures']):
			print_dict(scene, "Lamp \"%s\" texture stack" % la.name, bus['lamp_textures'])

	for key in bus['lamp_textures']:
		if len(bus['lamp_textures'][key]):
			bus['lamp_textures'][key]= write_TexOutput(bus, stack_write_textures(bus, stack_collapse_layers(bus['lamp_textures'][key])), key)

	return bus['lamp_textures']


def	write_material(bus):
	scene= bus['scene']
	ofile= bus['files']['materials']

	ob=    bus['node']['object']
	base=  bus['node'].get('base')

	ma=    bus['material']['material']

	# Linked groups material override feature
	if base and base.dupli_type == 'GROUP':
		base_material_names= []
		for slot in base.material_slots:
			if slot and slot.material:
				base_material_names.append(slot.material.name)
		for base_ma in base_material_names:
			if base_ma.find(ma.name) != -1:
				slot= base.material_slots.get(base_ma)
				ma=   slot.material
				bus['material']['material']= ma

	VRayMaterial= ma.vray

	ma_name= get_name(ma, prefix='MA')

	# Check Toon before cache
	if VRayMaterial.VolumeVRayToon.use:
		bus['effects']['toon']['effects'].append(
			PLUGINS['SETTINGS']['SettingsEnvironment'].write_VolumeVRayToon_from_material(bus)
		)
		append_unique(bus['effects']['toon']['objects'], bus['node']['object'])

	# Write material textures
	write_material_textures(bus)

	# Check if material uses object mapping
	# In this case material is object dependend
	# because mapping is object dependent
	if bus['material']['orco_suffix']:
		ma_name+= bus['material']['orco_suffix']

	if not append_unique(bus['cache']['materials'], ma_name):
		return ma_name

	# Init wrapper / override / etc
	complex_material= []
	for component in (VRayMaterial.Mtl2Sided.use,
					  VRayMaterial.MtlWrapper.use,
					  VRayMaterial.MtlOverride.use,
					  VRayMaterial.MtlRenderStats.use,
					  VRayMaterial.round_edges,
					  VRayMaterial.material_id_number):
		if component:
			complex_material.append("MC%.2d_%s" % (len(complex_material), ma_name))
	complex_material.append(ma_name)
	complex_material.reverse()

	if VRayMaterial.type == 'MtlVRmat':
		PLUGINS['BRDF']['MtlVRmat'].write(bus, name=complex_material[-1])
	else:
		# Write material BRDF
		brdf= PLUGINS['BRDF'][VRayMaterial.type].write(bus)

		# print_dict(scene, "Bus", bus)

		# Add normal mapping if needed
		brdf= PLUGINS['BRDF']['BRDFBump'].write(bus, base_brdf = brdf)

		# Add bump mapping if needed
		brdf= PLUGINS['BRDF']['BRDFBump'].write(bus, base_brdf = brdf, use_bump = True)

		ofile.write("\nMtlSingleBRDF %s {"%(complex_material[-1]))
		ofile.write("\n\tbrdf=%s;" % a(scene, brdf))
		ofile.write("\n\tallow_negative_colors=1;")
		ofile.write("\n}\n")

	if VRayMaterial.Mtl2Sided.use:
		base_material= complex_material.pop()
		ofile.write("\nMtl2Sided %s {"%(complex_material[-1]))
		ofile.write("\n\tfront= %s;"%(base_material))
		back= base_material
		if VRayMaterial.Mtl2Sided.back:
			if VRayMaterial.Mtl2Sided.back in bpy.data.materials:
				back= get_name(bpy.data.materials[VRayMaterial.Mtl2Sided.back], prefix='MA')
		ofile.write("\n\tback= %s;"%(back))

		if VRayMaterial.Mtl2Sided.control == 'SLIDER':
			ofile.write("\n\ttranslucency= %s;" % a(scene, "Color(1.0,1.0,1.0)*%.3f" % VRayMaterial.Mtl2Sided.translucency_slider))
		elif VRayMaterial.Mtl2Sided.control == 'COLOR':
			ofile.write("\n\ttranslucency= %s;" % a(scene, VRayMaterial.Mtl2Sided.translucency_color))
		else:
			if VRayMaterial.Mtl2Sided.translucency_tex:
				translucency_tex = write_subtexture(bus, VRayMaterial.Mtl2Sided.translucency_tex)
				if translucency_tex:
					ofile.write("\n\ttranslucency_tex= %s;" % (translucency_tex))
					ofile.write("\n\ttranslucency_tex_mult= %s;" % a(scene,VRayMaterial.Mtl2Sided.translucency_tex_mult))
			else:
				ofile.write("\n\ttranslucency= %s;" % a(scene, "Color(1.0,1.0,1.0)*%.3f" % VRayMaterial.Mtl2Sided.translucency_slider))

		ofile.write("\n\tforce_1sided= %d;" % VRayMaterial.Mtl2Sided.force_1sided)
		ofile.write("\n}\n")

	if VRayMaterial.MtlWrapper.use:
		base_material= complex_material.pop()
		ofile.write("\nMtlWrapper %s {"%(complex_material[-1]))
		ofile.write("\n\tbase_material= %s;"%(base_material))
		for param in PLUGINS['MATERIAL']['MtlWrapper'].PARAMS:
			ofile.write("\n\t%s= %s;"%(param, a(scene,getattr(VRayMaterial.MtlWrapper,param))))
		ofile.write("\n}\n")

	if VRayMaterial.MtlOverride.use:
		base_mtl= complex_material.pop()
		ofile.write("\nMtlOverride %s {"%(complex_material[-1]))
		ofile.write("\n\tbase_mtl= %s;"%(base_mtl))

		for param in ('gi_mtl','reflect_mtl','refract_mtl','shadow_mtl'):
			override_material= getattr(VRayMaterial.MtlOverride, param)
			if override_material:
				if override_material in bpy.data.materials:
					ofile.write("\n\t%s= %s;"%(param, get_name(bpy.data.materials[override_material], prefix='MA')))

		environment_override= VRayMaterial.MtlOverride.environment_override
		if environment_override:
			if environment_override in bpy.data.textures:
				ofile.write("\n\tenvironment_override= %s;" % get_name(bpy.data.textures[environment_override], prefix='TE'))

		ofile.write("\n\tenvironment_priority= %i;"%(VRayMaterial.MtlOverride.environment_priority))
		ofile.write("\n}\n")

	if VRayMaterial.MtlRenderStats.use:
		base_mtl= complex_material.pop()
		ofile.write("\nMtlRenderStats %s {"%(complex_material[-1]))
		ofile.write("\n\tbase_mtl= %s;"%(base_mtl))
		for param in PLUGINS['MATERIAL']['MtlRenderStats'].PARAMS:
			ofile.write("\n\t%s= %s;"%(param, a(scene,getattr(VRayMaterial.MtlRenderStats,param))))
		ofile.write("\n}\n")

	if VRayMaterial.round_edges:
		base_mtl= complex_material.pop()
		ofile.write("\nMtlRoundEdges %s {" % complex_material[-1])
		ofile.write("\n\tbase_mtl= %s;" % base_mtl)
		ofile.write("\n\tradius= %.3f;" % VRayMaterial.radius)
		ofile.write("\n}\n")

	if VRayMaterial.material_id_number:
		base_mtl= complex_material.pop()
		ofile.write("\nMtlMaterialID %s {" % complex_material[-1])
		ofile.write("\n\tbase_mtl= %s;" % base_mtl)
		ofile.write("\n\tmaterial_id_number= %i;" % VRayMaterial.material_id_number)
		ofile.write("\n\tmaterial_id_color= %s;" % p(VRayMaterial.material_id_color))
		ofile.write("\n}\n")

	return ma_name


def write_lamp(bus):
	LIGHT_PORTAL= {
		'NORMAL':  0,
		'PORTAL':  1,
		'SPORTAL': 2,
	}
	SKY_MODEL= {
		'CIEOVER'  : 2,
		'CIECLEAR' : 1,
		'PREETH'   : 0,
	}
	UNITS= {
		'DEFAULT' : 0,
		'LUMENS'  : 1,
		'LUMM'    : 2,
		'WATTSM'  : 3,
		'WATM'    : 4,
	}

	scene= bus['scene']
	ofile= bus['files']['lights']
	ob=    bus['node']['object']

	lamp= ob.data
	VRayLamp= lamp.vray

	lamp_type= None

	lamp_name=   get_name(ob, prefix='LA')
	lamp_matrix= ob.matrix_world

	if 'dupli' in bus['node'] and 'name' in bus['node']['dupli']:
		lamp_name+=  bus['node']['dupli']['name']
		lamp_matrix= bus['node']['dupli']['matrix']

	if 'particle' in bus['node'] and 'name' in bus['node']['particle']:
		lamp_name+=  bus['node']['particle']['name']
		lamp_matrix= bus['node']['particle']['matrix']

	textures= write_lamp_textures(bus)

	if lamp.type == 'POINT':
		if VRayLamp.omni_type == 'AMBIENT':
			lamp_type= 'LightAmbient'
		else:
			if VRayLamp.radius > 0:
				lamp_type= 'LightSphere'
			else:
				lamp_type= 'LightOmni'
	elif lamp.type == 'SPOT':
		if VRayLamp.spot_type == 'SPOT':
			lamp_type= 'LightSpot'
		else:
			lamp_type= 'LightIESMax'
	elif lamp.type == 'SUN':
		if VRayLamp.direct_type == 'DIRECT':
			lamp_type= 'LightDirectMax'
		else:
			lamp_type= 'SunLight'
	elif lamp.type == 'AREA':
		lamp_type= 'LightRectangle'
	elif lamp.type == 'HEMI':
		lamp_type= 'LightDome'
	else:
		return

	ofile.write("\n%s %s {"%(lamp_type,lamp_name))

	if 'color' in textures:
		if lamp.type == 'SUN' and VRayLamp.direct_type == 'DIRECT':
			ofile.write("\n\tprojector_map= %s;" % textures['color'])

		if lamp.type in {'AREA','HEMI'}:
			ofile.write("\n\ttex_adaptive= %.2f;" % (1.0))
			ofile.write("\n\ttex_resolution= %i;" % (512))

			if lamp.type == 'AREA':
				ofile.write("\n\tuse_rect_tex= 1;")
				ofile.write("\n\trect_tex= %s;" % textures['color'])
			elif lamp.type == 'HEMI':
				ofile.write("\n\tuse_dome_tex= 1;")
				ofile.write("\n\tdome_tex= %s;" % textures['color'])

		if lamp.type not in {'HEMI'}:
			ofile.write("\n\tcolor_tex= %s;" % textures['color'])

	if 'intensity' in textures:
		ofile.write("\n\tintensity_tex= %s;" % a(scene, "%s::out_intensity" % textures['intensity']))

	if 'shadowColor' in textures:
		if lamp.type == 'SUN' and VRayLamp.direct_type == 'DIRECT':
			ofile.write("\n\tshadowColor_tex= %s;" % textures['shadowColor'])
		else:
			ofile.write("\n\tshadow_color_tex= %s;" % textures['shadowColor'])

	if lamp_type == 'SunLight':
		ofile.write("\n\tsky_model= %i;"%(SKY_MODEL[VRayLamp.sky_model]))
		ofile.write("\n\tfilter_color=%s;" % a(scene, "Color(%.6f, %.6f, %.6f)"%(tuple(lamp.color))))
	else:
		if VRayLamp.color_type == 'RGB':
			color= lamp.color
		else:
			color= kelvin_to_rgb(VRayLamp.temperature)
		ofile.write("\n\tcolor= %s;" % a(scene, "Color(%.6f, %.6f, %.6f)"%(tuple(color))))

		if lamp_type not in ('LightIESMax', 'LightAmbient'):
			ofile.write("\n\tunits= %i;"%(UNITS[VRayLamp.units]))

		if lamp_type == 'LightIESMax':
			ofile.write("\n\ties_light_shape= %i;" % (VRayLamp.ies_light_shape if VRayLamp.ies_light_shape else -1))
			ofile.write("\n\ties_light_width= %.3f;" %    (VRayLamp.ies_light_width))
			ofile.write("\n\ties_light_length= %.3f;" %   (VRayLamp.ies_light_width if VRayLamp.ies_light_shape_lock else VRayLamp.ies_light_length))
			ofile.write("\n\ties_light_height= %.3f;" %   (VRayLamp.ies_light_width if VRayLamp.ies_light_shape_lock else VRayLamp.ies_light_height))
			ofile.write("\n\ties_light_diameter= %.3f;" % (VRayLamp.ies_light_diameter))

	if lamp_type == 'LightSpot':
		ofile.write("\n\tconeAngle= %s;" % a(scene,lamp.spot_size))
		ofile.write("\n\tpenumbraAngle= %s;" % a(scene, - lamp.spot_size * lamp.spot_blend))

		ofile.write("\n\tdecay=%s;" % a(scene, VRayLamp.decay))

		ofile.write("\n\tuseDecayRegions=1;")
		ofile.write("\n\tstartDistance1=%s;" % a(scene, 0.0))
		ofile.write("\n\tendDistance1=%s;" % a(scene, lamp.distance-lamp.spot_blend))
		ofile.write("\n\tstartDistance2=%s;" % a(scene, lamp.distance-lamp.spot_blend))
		ofile.write("\n\tendDistance2=%s;" % a(scene, lamp.distance-lamp.spot_blend))
		ofile.write("\n\tstartDistance3=%s;" % a(scene, lamp.distance-lamp.spot_blend))
		ofile.write("\n\tendDistance3=%s;" % a(scene, lamp.distance))

	if lamp_type == 'LightRectangle':
		if lamp.shape == 'RECTANGLE':
			ofile.write("\n\tu_size= %s;"%(a(scene,lamp.size/2)))
			ofile.write("\n\tv_size= %s;"%(a(scene,lamp.size_y/2)))
		else:
			ofile.write("\n\tu_size= %s;"%(a(scene,lamp.size/2)))
			ofile.write("\n\tv_size= %s;"%(a(scene,lamp.size/2)))
		ofile.write("\n\tlightPortal= %i;"%(LIGHT_PORTAL[VRayLamp.lightPortal]))

	for param in LIGHT_PARAMS[lamp_type]:
		if param == 'shadow_subdivs':
			ofile.write("\n\tshadow_subdivs= %s;"%(a(scene,VRayLamp.subdivs)))
		elif param == 'shadowSubdivs':
			ofile.write("\n\tshadowSubdivs= %s;"%(a(scene,VRayLamp.subdivs)))
		elif param == 'shadowRadius' and lamp_type == 'LightDirectMax':
			ofile.write("\n\t%s= %s;" % (param, a(scene,VRayLamp.shadowRadius)))
			ofile.write("\n\tshadowShape=%s;" % VRayLamp.shadowShape)
			ofile.write("\n\tshadowRadius1= %s;" % a(scene,VRayLamp.shadowRadius))
			ofile.write("\n\tshadowRadius2= %s;" % a(scene,VRayLamp.shadowRadius))
		elif param == 'intensity' and lamp_type == 'LightIESMax':
			ofile.write("\n\tpower= %s;"%(a(scene, "%i" % (int(VRayLamp.intensity)))))
		elif param == 'shadow_color':
			ofile.write("\n\tshadow_color= %s;"%(a(scene,VRayLamp.shadowColor)))
		elif param == 'ies_file':
			ofile.write("\n\t%s= \"%s\";"%(param, get_full_filepath(bus,lamp,VRayLamp.ies_file)))
		else:
			ofile.write("\n\t%s= %s;"%(param, a(scene,getattr(VRayLamp,param))))

	ofile.write("\n\ttransform= %s;"%(a(scene,transform(lamp_matrix))))

	# Render Elements
	#
	listRenderElements = {
		'channels_raw'      : [],
		'channels_diffuse'  : [],
		'channels_specular' : [],
	}

	for channel in scene.vray.render_channels:
		if channel.type == 'LIGHTSELECT' and channel.use:
			channelData = channel.RenderChannelLightSelect
			channelName = "LightSelect_%s" % clean_string(channel.name)

			lampList = generateDataList(channelData.lights, 'lamps')

			if lamp in lampList:
				if channelData.type == 'RAW':
					listRenderElements['channels_raw'].append(channelName)
				elif channelData.type == 'DIFFUSE':
					listRenderElements['channels_diffuse'].append(channelName)
				elif channelData.type == 'SPECULAR':
					listRenderElements['channels_specular'].append(channelName)

	for key in listRenderElements:
		renderChannelArray = listRenderElements[key]

		if not len(renderChannelArray):
			continue

		ofile.write("\n\t%s=List(%s);" % (key, ",".join(renderChannelArray)))

	ofile.write("\n}\n")

	# Data for SettingsLightLinker
	#
	if VRayLamp.use_include_exclude:
		bus['lightlinker'][lamp_name] = {}

		if VRayLamp.use_include:
			bus['lightlinker'][lamp_name]['include'] = generate_object_list(VRayLamp.include_objects, VRayLamp.include_groups)

		if VRayLamp.use_exclude:
			bus['lightlinker'][lamp_name]['exclude'] = generate_object_list(VRayLamp.exclude_objects, VRayLamp.exclude_groups)


def writeSceneInclude(bus):
	sceneFile = bus['files']['scene']

	ob = bus['node']['object']

	VRayObject = ob.vray

	if VRayObject.overrideWithScene:
		if VRayObject.sceneFilepath == "" and VRayObject.sceneDirpath == "":
			return

		sceneFile.write("\nSceneInclude %s {" % get_name(ob, prefix='SI'))

		vrsceneFilelist = []

		if VRayObject.sceneFilepath:
			vrsceneFilelist.append(bpy.path.abspath(VRayObject.sceneFilepath))

		if VRayObject.sceneDirpath:
			vrsceneDirpath = bpy.path.abspath(VRayObject.sceneDirpath)

			for dirname, dirnames, filenames in os.walk(vrsceneDirpath):
				for filename in filenames:
					if not filename.endswith(".vrscene"):
						continue
					vrsceneFilelist.append(os.path.join(dirname, filename))
		
		sceneFile.write("\n\tfilepath=\"%s\";" % (";").join(vrsceneFilelist))
		sceneFile.write("\n\tprefix=\"%s\";" % get_name(ob, prefix='SI'))

		sceneFile.write("\n\ttransform=%s;" % transform(ob.matrix_world))
		sceneFile.write("\n\tuse_transform=%s;" % p(VRayObject.sceneUseTransform))
		
		sceneFile.write("\n\treplace=%s;" % p(VRayObject.sceneReplace))
		
		sceneFile.write("\n\tadd_nodes=%s;" % p(VRayObject.sceneAddNodes))
		sceneFile.write("\n\tadd_materials=%s;" % p(VRayObject.sceneAddMaterials))
		sceneFile.write("\n\tadd_lights=%s;" % p(VRayObject.sceneAddLights))
		sceneFile.write("\n\tadd_cameras=%s;" % p(VRayObject.sceneAddCameras))
		sceneFile.write("\n\tadd_environment=%s;" % p(VRayObject.sceneAddEnvironment))
		sceneFile.write("\n}\n")


def write_scene(bus):
	scene= bus['scene']

	VRayScene=       scene.vray

	VRayExporter=    VRayScene.exporter
	SettingsOptions= VRayScene.SettingsOptions

	# Some failsafe defaults
	bus['defaults']= {}
	bus['defaults']['brdf']=     "BRDFNOBRDFISSET"
	bus['defaults']['material']= "MANOMATERIALISSET"
	bus['defaults']['texture']=  "TENOTEXTUREIESSET"
	bus['defaults']['uvwgen']=   "DEFAULTUVWC"
	bus['defaults']['blend']=    "TEDefaultBlend"

	for key in bus['files']:
		if bus['files'][key] is None:
			continue
		bus['files'][key].write("// V-Ray For Blender")
		bus['files'][key].write("\n// %s" % datetime.datetime.now().strftime("%A, %d %B %Y %H:%M"))
		bus['files'][key].write("\n// Filename: %s\n" % os.path.basename(bpy.data.filepath))

	bus['files']['scene'].write("\n// Settings\n")
	bus['files']['nodes'].write("\n// Nodes\n")
	bus['files']['lights'].write("\n// Lights\n")
	bus['files']['camera'].write("\n// Camera\n")
	bus['files']['environment'].write("\n// Environment\n")
	bus['files']['textures'].write("\n// Textures\n")
	bus['files']['materials'].write("\n// Materials\n")

	bus['files']['textures'].write("\n// Useful defaults")
	bus['files']['textures'].write("\nUVWGenChannel %s {" % bus['defaults']['uvwgen'])
	bus['files']['textures'].write("\n\tuvw_channel= 1;")
	bus['files']['textures'].write("\n\tuvw_transform= Transform(Matrix(Vector(1.0,0.0,0.0),Vector(0.0,1.0,0.0),Vector(0.0,0.0,1.0)),Vector(0.0,0.0,0.0));")
	bus['files']['textures'].write("\n}\n")
	bus['files']['textures'].write("\nTexChecker %s {" % bus['defaults']['texture'])
	bus['files']['textures'].write("\n\tuvwgen= %s;" % bus['defaults']['uvwgen'])
	bus['files']['textures'].write("\n}\n")
	bus['files']['textures'].write("\nTexAColor %s {" % bus['defaults']['blend'])
	bus['files']['textures'].write("\n\tuvwgen= %s;" % bus['defaults']['uvwgen'])
	bus['files']['textures'].write("\n\ttexture= AColor(1.0,1.0,1.0,1.0);")
	bus['files']['textures'].write("\n}\n")

	bus['files']['materials'].write("\n// Fail-safe material")
	bus['files']['materials'].write("\nBRDFDiffuse %s {" % bus['defaults']['brdf'])
	bus['files']['materials'].write("\n\tcolor=Color(0.5,0.5,0.5);")
	bus['files']['materials'].write("\n}\n")
	bus['files']['materials'].write("\nMtlSingleBRDF %s {" % bus['defaults']['material'])
	bus['files']['materials'].write("\n\tbrdf= %s;" % bus['defaults']['brdf'])
	bus['files']['materials'].write("\n}\n")

	if bus['preview']:
		bus['files']['lights'].write("\nLightDirectMax LALamp_008 { // PREVIEW")
		bus['files']['lights'].write("\n\tintensity= 1.000000;")
		bus['files']['lights'].write("\n\tcolor= Color(1.000000, 1.000000, 1.000000);")
		bus['files']['lights'].write("\n\tshadows= 0;")
		bus['files']['lights'].write("\n\tcutoffThreshold= 0.01;")
		bus['files']['lights'].write("\n\taffectSpecular= 0;")
		bus['files']['lights'].write("\n\tareaSpeculars= 0;")
		bus['files']['lights'].write("\n\tfallsize= 100.0;")
		bus['files']['lights'].write("\n\ttransform= Transform(")
		bus['files']['lights'].write("\n\t\tMatrix(")
		bus['files']['lights'].write("\n\t\t\tVector(1.000000, 0.000000, -0.000000),")
		bus['files']['lights'].write("\n\t\t\tVector(0.000000, 0.000000, 1.000000),")
		bus['files']['lights'].write("\n\t\t\tVector(0.000000, -1.000000, 0.000000)")
		bus['files']['lights'].write("\n\t\t),")
		bus['files']['lights'].write("\n\t\tVector(1.471056, -14.735638, 3.274598));")
		bus['files']['lights'].write("\n}\n")

		bus['files']['lights'].write("\nLightSpot LALamp_002 { // PREVIEW")
		bus['files']['lights'].write("\n\tintensity= 5.000000;")
		bus['files']['lights'].write("\n\tcolor= Color(1.000000, 1.000000, 1.000000);")
		bus['files']['lights'].write("\n\tconeAngle= 1.3;")
		bus['files']['lights'].write("\n\tpenumbraAngle= -0.4;")
		bus['files']['lights'].write("\n\tshadows= 1;")
		bus['files']['lights'].write("\n\tcutoffThreshold= 0.01;")
		bus['files']['lights'].write("\n\taffectDiffuse= 1;")
		bus['files']['lights'].write("\n\taffectSpecular= 0;")
		bus['files']['lights'].write("\n\tareaSpeculars= 0;")
		bus['files']['lights'].write("\n\tshadowRadius= 0.000000;")
		bus['files']['lights'].write("\n\tshadowSubdivs= 4;")
		bus['files']['lights'].write("\n\tdecay= 1.0;")
		bus['files']['lights'].write("\n\ttransform= Transform(")
		bus['files']['lights'].write("\n\t\tMatrix(")
		bus['files']['lights'].write("\n\t\t\tVector(-0.549843, 0.655945, 0.517116),")
		bus['files']['lights'].write("\n\t\t\tVector(-0.733248, -0.082559, -0.674931),")
		bus['files']['lights'].write("\n\t\t\tVector(-0.400025, -0.750280, 0.526365)")
		bus['files']['lights'].write("\n\t\t),")
		bus['files']['lights'].write("\n\t\tVector(-5.725639, -13.646054, 8.5));")
		bus['files']['lights'].write("\n}\n")

		bus['files']['lights'].write("\nLightOmni LALamp { // PREVIEW")
		bus['files']['lights'].write("\n\tintensity= 50.000000;")
		bus['files']['lights'].write("\n\tcolor= Color(1.000000, 1.000000, 1.000000);")
		bus['files']['lights'].write("\n\tshadows= 0;")
		bus['files']['lights'].write("\n\tcutoffThreshold= 0.01;")
		bus['files']['lights'].write("\n\taffectDiffuse= 1;")
		bus['files']['lights'].write("\n\taffectSpecular= 0;")
		bus['files']['lights'].write("\n\tspecular_contribution= 0.000000;")
		bus['files']['lights'].write("\n\tareaSpeculars= 0;")
		bus['files']['lights'].write("\n\tshadowSubdivs= 4;")
		bus['files']['lights'].write("\n\tdecay= 2.0;")
		bus['files']['lights'].write("\n\ttransform= Transform(")
		bus['files']['lights'].write("\n\t\tMatrix(")
		bus['files']['lights'].write("\n\t\t\tVector(0.499935, 0.789660, 0.355671),")
		bus['files']['lights'].write("\n\t\t\tVector(-0.672205, 0.094855, 0.734263),")
		bus['files']['lights'].write("\n\t\t\tVector(0.546081, -0.606168, 0.578235)")
		bus['files']['lights'].write("\n\t\t),")
		bus['files']['lights'].write("\n\t\tVector(15.685226, -7.460007, 3.0));")
		bus['files']['lights'].write("\n}\n")

		bus['files']['lights'].write("\nLightOmni LALamp_001 { // PREVIEW")
		bus['files']['lights'].write("\n\tintensity= 20.000000;")
		bus['files']['lights'].write("\n\tcolor= Color(1.000000, 1.000000, 1.000000);")
		bus['files']['lights'].write("\n\tshadows= 0;")
		bus['files']['lights'].write("\n\tcutoffThreshold= 0.01;")
		bus['files']['lights'].write("\n\taffectDiffuse= 1;")
		bus['files']['lights'].write("\n\taffectSpecular= 0;")
		bus['files']['lights'].write("\n\tareaSpeculars= 0;")
		bus['files']['lights'].write("\n\tshadowSubdivs= 4;")
		bus['files']['lights'].write("\n\tdecay= 2.0;")
		bus['files']['lights'].write("\n\ttransform= Transform(")
		bus['files']['lights'].write("\n\t\tMatrix(")
		bus['files']['lights'].write("\n\t\t\tVector(0.499935, 0.789660, 0.355671),")
		bus['files']['lights'].write("\n\t\t\tVector(-0.672205, 0.094855, 0.734263),")
		bus['files']['lights'].write("\n\t\t\tVector(0.546081, -0.606168, 0.578235)")
		bus['files']['lights'].write("\n\t\t),")
		bus['files']['lights'].write("\n\t\tVector(-10.500286, -12.464991, 4.0));")
		bus['files']['lights'].write("\n}\n")

	# Processed objects
	bus['objects']= []

	# Effects from material / object settings
	bus['effects']= {}
	bus['effects']['fog']= {}

	bus['effects']['toon']= {}
	bus['effects']['toon']['effects']= []
	bus['effects']['toon']['objects']= []

	# Prepare exclude for effects
	# TODO: Pass this list to C++ expoter
	#
	exclude_list= []
	VRayEffects=  VRayScene.VRayEffects
	if VRayEffects.use:
		for effect in VRayEffects.effects:
			if effect.use:
				if effect.type == 'FOG':
					EnvironmentFog= effect.EnvironmentFog
					fog_objects= generate_object_list(EnvironmentFog.objects, EnvironmentFog.groups)
					for ob in fog_objects:
						if not object_visible(bus, ob):
							continue
						if ob not in exclude_list:
							exclude_list.append(ob)

	def write_frame(bus, firstFrame=True, checkAnimated='NONE'):
		def isMeshLight(ob):
			if ob.type in GEOM_TYPES and ob.vray.LightMesh.use:
				return True
			return False

		def isAnimated(o):
			if firstFrame:
				return True
			if checkAnimated in {'NONE'}:
				return True
			if o.animation_data and o.animation_data.action:
				return True
			elif hasattr(o, 'parent') and o.parent:
				return isAnimated(o.parent)
			return False

		scene = bus['scene']

		VRayScene       = scene.vray
		SettingsOptions = VRayScene.SettingsOptions

		# Cache stores already exported data
		bus['cache'] = {}
		bus['cache']['textures']  = []
		bus['cache']['materials'] = []
		bus['cache']['displace']  = []
		bus['cache']['proxy']     = []
		bus['cache']['bitmap']    = []
		bus['cache']['uvwgen']    = {}

		# Camera
		bus['camera']= scene.camera

		# Fake node; get rid of this...
		bus['node'] = {}

		# Write objects and geometry
		_vray_for_blender.exportScene(bus['exporter'])
		_vray_for_blender.clearCache()

		timerStart = time.clock()

		# Write textures
		def writeTextures(textures):
			for tex in textures:
				if bus['engine'].test_break():
					break
				bus['mtex'] = {
					'name'    : clean_string(get_name(tex, prefix='TE')),
					'texture' : tex,
				}
				if not isAnimated(tex):
					# Material export will take tex from bus['cache']['textures']
					append_unique(bus['cache']['textures'], bus['mtex']['name'])
					continue
				write_texture(bus)

		if not bus['preview']:
			writeTextures(bpy.data.textures)
		else:
			texPreviewOb = scene.objects.get('texture', None)
			if texPreviewOb and texPreviewOb.is_visible(scene):
				# Texture preview
				def getPreviewTexture(ob):
					if not len(ob.material_slots):
						return None,None
					if not ob.material_slots[0].material:
						return None,None
					ma = ob.material_slots[0].material
					if not len(ma.texture_slots):
						return None,None
					slot = ma.texture_slots[0]
					if not slot.texture:
						return None,None
					return ma, slot.texture

				previewMa, previewTex = getPreviewTexture(texPreviewOb)
				if previewTex:
					bus['mtex'] = {
						'name'    : clean_string(get_name(previewTex, prefix='TE')),
						'texture' : previewTex,
					}
					write_texture(bus)

					bus['files']['materials'].write("\n// Texture preview material")
					bus['files']['materials'].write("\nBRDFLight BRDFTexPreview {")
					bus['files']['materials'].write("\n\tcolor=%s;" % get_name(previewTex, prefix='TE'))
					bus['files']['materials'].write("\n\tcolorMultiplier=1.0;")
					bus['files']['materials'].write("\n}\n")
					bus['files']['materials'].write("\nMtlSingleBRDF %s {" % get_name(previewMa, prefix='MA'))
					bus['files']['materials'].write("\n\tbrdf=BRDFTexPreview;")
					bus['files']['materials'].write("\n}\n")
			else:
				# Material preview
				def previewTextures():
					for ob in scene.objects:
						if len(ob.material_slots):
							for ms in ob.material_slots:
								if ms.material:
									for ts in ms.material.texture_slots:
										if ts and ts.texture:
											yield ts.texture
				writeTextures(previewTextures())

		# Write materials
		#
		materials = bpy.data.materials
		if bus['preview']:
			def previewMaterials():
				for ob in scene.objects:
					if len(ob.material_slots):
						for ms in ob.material_slots:
							if ms.material:
								yield ms.material
			materials = previewMaterials()

		bus['node']['object'] = None
		for ma in materials:
			if bus['engine'].test_break():
				break
			if not isAnimated(ma):
				continue

			bus['material'] = {}
			bus['material']['material'] = ma

			if SettingsOptions.mtl_override_on and SettingsOptions.mtl_override:
				if not ma.vray.dontOverride:
					bus['material']['material'] = get_data_by_name(scene, 'materials', SettingsOptions.mtl_override)

			# Normal mapping settings pointer
			bus['material']['normal_slot'] = None

			# Bump mapping settings pointer
			bus['material']['bump_slot']   = None

			# Set if any texture uses object mapping
			bus['material']['orco_suffix'] = ""

			write_material(bus)

		# Write lights
		for ob in bpy.context.scene.objects:
			if bus['engine'].test_break():
				break

			if ob.type not in {'LAMP'} and not isMeshLight(ob):
				continue

			if not object_on_visible_layers(scene, ob) or ob.hide_render:
				if not scene.vray.SettingsOptions.light_doHiddenLights:
					continue

			if not (isAnimated(ob) or isAnimated(ob.data)):
				continue

			if isMeshLight(ob):
				PLUGINS['GEOMETRY']['LightMesh'].write(bus, ob)
			else:
				bus['node'].update({
					'object'   : ob, # Currently processes object
					'visible'  : ob, # Object visibility
					'base'     : ob, # Attributes for particle / dupli export
					'dupli'    : {},
					'particle' : {},
				})
				write_lamp(bus)

		# TODO: Mesh lights

		# Write settings
		if firstFrame:
			write_settings(bus)

		# TODO: Add camera animation detection
		#
		PLUGINS['CAMERA']['CameraPhysical'].write(bus)
		PLUGINS['SETTINGS']['BakeView'].write(bus)
		PLUGINS['SETTINGS']['RenderView'].write(bus)
		PLUGINS['CAMERA']['CameraStereoscopic'].write(bus)

		# SphereFade could be animated
		# We already export SphereFade data in settings export,
		# so skip first frame
		if not firstFrame:
			PLUGINS['SETTINGS']['SettingsEnvironment'].WriteSphereFade(bus)

		debug(scene, "Writing lights, materials and settings in %.2f" % (time.clock() - timerStart))

	timer= time.clock()

	debug(scene, "Writing scene...")

	CHECK_ANIMATED = {
		'NONE'   : 0,
		'SIMPLE' : 1,
		'HASH'   : 2,
		'BOTH'   : 3,
	}

	if bus['preview']:
		bus['exporter'] = _vray_for_blender.init(
			context = bpy.context.as_pointer(),
			engine  = bus['engine'].as_pointer(),
			scene   = scene.as_pointer(),

			exportNodes    = True,
			exportGeometry = True,

			isAnimation   = False,
			checkAnimated = 0,

			objectFile   = bus['files']['nodes'],
			geometryFile = bus['files']['geometry'],
			lightsFile   = bus['files']['lights'],
		)

		write_frame(bus)

		_vray_for_blender.exit(bus['exporter'])

		del bus['exporter']

		return False

	bus['exporter'] = _vray_for_blender.init(
		context = bpy.context.as_pointer(),
		engine  = bus['engine'].as_pointer(),

		exportNodes    = True,
		exportGeometry = VRayExporter.auto_meshes,

		isAnimation   = VRayExporter.animation and VRayExporter.animation_type == 'FULL',
		checkAnimated = CHECK_ANIMATED[VRayExporter.check_animated],

		objectFile   = bus['files']['nodes'],
		geometryFile = bus['files']['geometry'],
		lightsFile   = bus['files']['lights'],
	)

	_vray_for_blender.initCache(VRayExporter.animation, CHECK_ANIMATED[VRayExporter.check_animated])

	if VRayExporter.animation and VRayExporter.animation_type in {'FULL', 'NOTMESHES'}:
		# Store current frame
		selected_frame = scene.frame_current

		f = scene.frame_start
		while(f <= scene.frame_end):
			if bus['engine'] and bus['engine'].test_break():
				return
			scene.frame_set(f)
			bus['check_animated'] = VRayExporter.check_animated
			write_frame(bus, firstFrame=(f==scene.frame_start), checkAnimated=VRayExporter.check_animated)
			f += scene.frame_step

			_vray_for_blender.clearCache()

		# Restore selected frame
		scene.frame_set(selected_frame)

		_vray_for_blender.clearFrames()
	else:
		if VRayExporter.camera_loop:
			if bus['cameras']:
				for i,camera in enumerate(bus['cameras']):
					bus['camera'] = camera
					bus['camera_index'] = i
					VRayExporter.customFrame = i+1
					write_frame(bus)
			else:
				debug(scene, "No cameras selected for \"Camera loop\"!", error= True)
				return True # Error

		else:
			write_frame(bus)

	_vray_for_blender.exit(bus['exporter'])
	del bus['exporter']

	debug(scene, "Writing scene... done {0:<64}".format("[%.2f]"%(time.clock() - timer)))

	if bus['engine'].test_break():
		return True

	return False # No errors


def run(bus):
	scene = bus['scene']

	VRayScene = scene.vray

	VRayExporter    = VRayScene.exporter
	VRayDR          = VRayScene.VRayDR
	RTEngine        = VRayScene.RTEngine
	SettingsOptions = VRayScene.SettingsOptions

	vray_exporter=   get_vray_exporter_path()
	vray_standalone= get_vray_standalone_path(scene)

	resolution_x= int(scene.render.resolution_x * scene.render.resolution_percentage / 100)
	resolution_y= int(scene.render.resolution_y * scene.render.resolution_percentage / 100)

	if vray_standalone is None:
		if bus['engine']:
			bus['engine'].report({'ERROR'}, "V-Ray Standalone not found!")
		return

	params = []
	params.append(vray_standalone)
	params.append('-sceneFile=%s' % Quotes(bus['filenames']['scene']))

	preview_file     = os.path.join(tempfile.gettempdir(), "preview.jpg")
	preview_loadfile = os.path.join(tempfile.gettempdir(), "preview.0000.jpg")
	image_file = os.path.join(bus['filenames']['output'], bus['filenames']['output_filename'])
	load_file  = preview_loadfile if bus['preview'] else os.path.join(bus['filenames']['output'], bus['filenames']['output_loadfile'])

	if not scene.render.threads_mode == 'AUTO':
		params.append('-numThreads=%i' % (scene.render.threads))

	image_to_blender = VRayExporter.auto_save_render and VRayExporter.image_to_blender
	if bus['preview']:
		image_to_blender = False

	if bus['preview']:
		params.append('-imgFile=%s' % Quotes(preview_file))
		params.append('-showProgress=0')
		params.append('-display=0')
		params.append('-autoclose=1')
		params.append('-verboseLevel=0')

	else:
		if RTEngine.enabled:
			DEVICE = {
				'CPU'           : 1,
				'OPENCL_SINGLE' : 3,
				'OPENCL_MULTI'  : 4,
				'CUDA_SINGLE'   : 5,
			}
			params.append('-rtEngine=%i' % DEVICE[RTEngine.use_opencl])
			params.append('-rtTimeOut=%.3f'   % RTEngine.rtTimeOut)
			params.append('-rtNoise=%.3f'     % RTEngine.rtNoise)
			params.append('-rtSampleLevel=%i' % RTEngine.rtSampleLevel)

		params.append('-display=%i' % (VRayExporter.display))
		params.append('-verboseLevel=%s' % (VRayExporter.verboseLevel))

		if scene.render.use_border:
			x0= resolution_x * scene.render.border_min_x
			y0= resolution_y * (1.0 - scene.render.border_max_y)
			x1= resolution_x * scene.render.border_max_x
			y1= resolution_y * (1.0 - scene.render.border_min_y)

			region = 'crop' if scene.render.use_crop_to_border else 'region'
			params.append("-%s=%i;%i;%i;%i" % (region, x0, y0, x1, y1))

		if VRayExporter.use_still_motion_blur:
			params.append("-frames=%d" % scene.frame_end)
		else:
			if VRayExporter.animation:
				params.append("-frames=")
				if VRayExporter.animation_type == 'FRAMEBYFRAME':
					params.append("%d"%(scene.frame_current))
				else:
					params.append("%d-%d,%d"%(scene.frame_start, scene.frame_end, int(scene.frame_step)))
			elif VRayExporter.camera_loop:
				if bus['cameras']:
					params.append("-frames=1-%d,1" % len(bus['cameras']))
			else:
				params.append("-frames=%d" % scene.frame_current)

		if VRayDR.on:
			if len(VRayDR.nodes):
				params.append('-distributed=%s' % ('2' if VRayDR.renderOnlyOnNodes else '1'))
				params.append('-portNumber=%i' % (VRayDR.port))
				params.append('-renderhost=%s' % Quotes(';'.join([n.address for n in VRayDR.nodes if n.use])))
				if VRayDR.transferAssets == '0':
					params.append('-include=%s' % Quotes(bus['filenames']['DR']['shared_dir'] + os.sep))
				else:
					params.append('-transferAssets=%s' % VRayDR.transferAssets)

		if image_to_blender:
			params.append('-imgFile=%s' % Quotes(image_file))
			params.append('-autoclose=1')

	if PLATFORM == "linux":
		if VRayExporter.log_window:
			LOG_TERMINAL = {
				'DEFAULT' : 'xterm',
				'XTERM'   : 'xterm',
				'GNOME'   : 'gnome-terminal',
				'KDE'     : 'konsole',
				'CUSTOM'  : VRayExporter.log_window_term,
			}

			log_window = []
			if VRayExporter.log_window_type in ['DEFAULT', 'XTERM']:
				log_window.append("xterm")
				log_window.append("-T")
				log_window.append("VRAYSTANDALONE")
				log_window.append("-geometry")
				log_window.append("90x10")
				log_window.append("-e")
				log_window.extend(params)
			else:
				log_window.extend(LOG_TERMINAL[VRayExporter.log_window_type].split(" "))
				if VRayExporter.log_window_type == "GNOME":
					log_window.append("-x")
					log_window.append("sh")
					log_window.append("-c")
					log_window.append(" ".join(params))
				else:
					log_window.append("-e")
					log_window.extend(params)
			params = log_window

	if (VRayExporter.autoclose
		or (VRayExporter.animation and VRayExporter.animation_type == 'FRAMEBYFRAME')
		or (VRayExporter.animation and VRayExporter.animation_type == 'FULL' and VRayExporter.use_still_motion_blur)):
		params.append('-autoclose=1')

	engine = bus['engine']

	params.append('-displaySRGB=%i' % (1 if VRayExporter.display_srgb else 2))

	# If this is a background task, wait until render end
	# and no VFB is required
	if bpy.app.background or VRayExporter.wait:
		if bpy.app.background:
			params.append('-display=0')   # Disable VFB
			params.append('-autoclose=1') # Exit on render end
		subprocess.call(params)
		return

	if VRayExporter.use_feedback:
		if scene.render.use_border:
			return

		proc = VRayProcess()
		proc.sceneFile = bus['filenames']['scene']
		proc.imgFile   = image_file
		proc.scene     = scene

		proc.set_params(bus=bus)
		proc.run()

		feedback_image = os.path.join(get_ram_basedir(), "vrayblender_%s_stream.jpg"%(get_username()))

		proc_interrupted = False

		render_result_image = None

		if engine is None:
			return

			# TODO: try finish this
			if RTEngine.enabled:
				render_result_name = "VRay Render"

				if render_result_name not in bpy.data.images:
					bpy.ops.image.new(name=render_result_name, width=resolution_x, height=resolution_y, color=(0.0, 0.0, 0.0, 1.0), alpha=True, generated_type='BLANK', float=False)
					render_result_image.source   = 'FILE'
					render_result_image.filepath = feedback_image

				render_result_image = bpy.data.images[render_result_name]

				def task():
					global proc

					if not proc.is_running():
						return

					err = proc.recieve_image(feedback_image)

					if err is None:
						try:
							render_result_image.reload()

							for window in bpy.context.window_manager.windows:
								for area in window.screen.areas:
									if area.type == 'IMAGE_EDITOR':
										for space in area.spaces:
											if space.type == 'IMAGE_EDITOR':
												if space.image.name == render_result_name:
													area.tag_redraw()
													return
						except:
							return

				def my_timer():
					t = Timer(0.25, my_timer)
					t.start()
					task()

				my_timer()

		else:
			while True:
				time.sleep(0.25)

				if engine.test_break():
					proc_interrupted = True
					debug(None, "Process is interrupted by the user")
					break

				err = proc.recieve_image(feedback_image)
				if VRayExporter.debug:
					debug(None, "Recieve image error: %s"%(err))
				if err is None:
					load_result(engine, resolution_x, resolution_y, feedback_image)

				if proc.exit_ready:
					break

				if VRayExporter.use_progress:
					msg, prog = proc.get_progress()
					if prog is not None and msg is not None:
						engine.update_stats("", "V-Ray: %s %.0f%%"%(msg, prog*100.0))
						engine.update_progress(prog)

				if proc.exit_ready:
					break

			proc.kill()

			# Load final result image to Blender
			if image_to_blender and not proc_interrupted:
				if load_file.endswith('vrimg'):
					# VRayImage (.vrimg) loaing is not supported
					debug(None, "VRayImage loading is not supported. Final image will not be loaded.")
				else:
					debug(None, "Loading final image: %s"%(load_file))
					load_result(engine, resolution_x, resolution_y, load_file)

	else:
		if not VRayExporter.autorun:
			debug(scene, "Command: %s" % ' '.join(params))
			return

		process = subprocess.Popen(params)

		if VRayExporter.animation and (VRayExporter.animation_type == 'FRAMEBYFRAME' or (VRayExporter.animation_type == 'FULL' and VRayExporter.use_still_motion_blur)):
			process.wait()
			return

		if not isinstance(engine, bpy.types.RenderEngine):
			return

		if engine is not None and (bus['preview'] or image_to_blender) and not scene.render.use_border:
			while True:
				if engine.test_break():
					try:
						process.kill()
					except:
						pass
					break

				if process.poll() is not None:
					if not VRayExporter.animation:
						result= engine.begin_result(0, 0, resolution_x, resolution_y)
						layer= result.layers[0]
						layer.load_from_file(load_file)
						engine.end_result(result)
					break

				time.sleep(0.1)


def close_files(bus):
	for key in bus['files']:
		if bus['files'][key] is None:
			continue
		bus['files'][key].write("\n")
		bus['files'][key].close()


def export_and_run(bus):
	err = write_scene(bus)

	close_files(bus)

	if not err:
		run(bus)


def init_bus(engine, scene, preview = False):
	VRayScene=    scene.vray
	VRayExporter= VRayScene.exporter

	# Settings bus
	bus= {}

	# Plugins
	bus['plugins']= PLUGINS

	# Scene
	bus['scene']=   scene

	# Preview
	bus['preview']= preview

	# V-Ray uses UV indexes, Blender uses UV names
	# Here we store UV name->index map
	bus['uvs']= get_uv_layers_map(scene)

	# Output files
	bus['files']=     {}
	bus['filenames']= {}

	bus['lightlinker'] = {}

	bus['check_animated'] = VRayExporter.check_animated
	bus['anim'] = set()

	init_files(bus)

	# Camera loop
	bus['cameras'] = []
	if VRayExporter.camera_loop:
		bus['cameras'] = [ob for ob in scene.objects if ob.type == 'CAMERA' and ob.data.vray.use_camera_loop]

	# Render engine
	bus['engine']= engine

	return bus


def render(engine, scene, preview= None):
	VRayScene    = scene.vray
	VRayExporter = VRayScene.exporter

	if preview:
		export_and_run(init_bus(engine, scene, True))
		return None

	if VRayExporter.use_still_motion_blur:
		# Store current settings
		e_anim_state = VRayExporter.animation
		e_anim_type  = VRayExporter.animation_type
		frame_start = scene.frame_start
		frame_end   = scene.frame_end

		# Run export
		if e_anim_state:
			if e_anim_type not in ['FRAMEBYFRAME']:
				return "\"Still Motion Blur\" feature works only in \"Frame-By-Frame\" animation mode!"

			VRayExporter.animation_type = 'FULL'

			f = frame_start
			while(f <= frame_end):
				scene.frame_start = f - 1
				scene.frame_end   = f

				export_and_run(init_bus(engine, scene))

				f += scene.frame_step

		else:
			VRayExporter.animation = True
			VRayExporter.animation_type = 'FULL'

			scene.frame_start = scene.frame_current - 1
			scene.frame_end   = scene.frame_current

			export_and_run(init_bus(engine, scene))

		# Restore settings
		VRayExporter.animation = e_anim_state
		VRayExporter.animation_type = e_anim_type
		scene.frame_start = frame_start
		scene.frame_end   = frame_end

	else:
		if VRayExporter.animation:
			if VRayExporter.animation_type == 'FRAMEBYFRAME':
				selected_frame = scene.frame_current

				f = scene.frame_start
				while(f <= scene.frame_end):
					if engine and engine.test_break():
						return
					scene.frame_set(f)
					export_and_run(init_bus(engine, scene))
					f += scene.frame_step

				scene.frame_set(selected_frame)
			else:
				export_and_run(init_bus(engine, scene))
		else:
			export_and_run(init_bus(engine, scene))

	return None
