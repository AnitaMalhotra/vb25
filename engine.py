#
# V-Ray For Blender
#
# http://chaosgroup.com
#
# Author: Andrei Izrantcev
# E-Mail: andrei.izrantcev@chaosgroup.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# All Rights Reserved. V-Ray(R) is a registered trademark of Chaos Software.
#

import os

import bpy

import _vray_for_blender

from . import utils
from . import render


def Init():
    _vray_for_blender.start(os.path.join(utils.get_vray_exporter_path(), "plugins_desc"))


def Shutdown():
    _vray_for_blender.free()


class VRayRenderer(bpy.types.RenderEngine):
    bl_idname      = 'VRAY_RENDER'
    bl_label       = "V-Ray"
    bl_use_preview =  False

    def render(self, scene):
        render.render(self, scene)


class VRayRendererPreview(bpy.types.RenderEngine):
    bl_idname      = 'VRAY_RENDER_PREVIEW'
    bl_label       = "V-Ray (With Material Preview)"
    bl_use_preview =  True

    def render(self, scene):
        if self.is_preview:
            if scene.render.resolution_x < 64:
                return
            render.render_preview(self, scene)
        else:
            render.render(self, scene)


def GetRegClasses():
    return (
        VRayRenderer,
        VRayRendererPreview,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)
