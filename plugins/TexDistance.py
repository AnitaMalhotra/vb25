#
# V-Ray/Blender
#
# http://www.chaosgroup.com
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

import bpy

from vb25    import utils
from vb25.ui import ui


TYPE = 'TEXTURE'
ID   = 'TexDistance'
NAME = 'Distance'
PLUG = 'TexDistance'
DESC = "The Distance texture is a V-Ray specific procedural texture that returns a different color based on a points distance to an object(s) specified in a selection list"
PID  =  40

PARAMS = (
)


class TexDistance(bpy.types.PropertyGroup):
    distance = bpy.props.FloatProperty(
        name        = "Distance",
        description = "",
        min         = 0.0,
        max         = 100.0,
        soft_min    = 0.0,
        soft_max    = 10.0,
        precision   = 3,
        default     = 0.1
    )

    far_tex = bpy.props.StringProperty(
        name = "Far Area Texture",
    )

    near_tex = bpy.props.StringProperty(
        name = "Near Area Texture",
    )

    inside_separate = bpy.props.BoolProperty(
        name        = "Inside Separate",
        default     = True
    )

    inside_solid = bpy.props.BoolProperty(
        name        = "Inside Solid",
        default     = False
    )

    inside_tex = bpy.props.StringProperty(
        name = "Inside Area Texture",
    )

    outside_separate = bpy.props.BoolProperty(
        name        = "Outside Separate",
        default     = False
    )

    outside_solid = bpy.props.BoolProperty(
        name        = "Outside Solid",
        default     = False
    )

    outside_tex = bpy.props.StringProperty(
        name = "Outside Area Texture",
    )

    #

    distance_tex = bpy.props.StringProperty(
        name = "Distance Texture",
    )

    far_tex_clr = bpy.props.FloatVectorProperty(
        name        = "Far Area",
        description = "",
        subtype     = 'COLOR',
        min         = 0.0,
        max         = 1.0,
        soft_min    = 0.0,
        soft_max    = 1.0,
        default     = (1,1,1)
    )

    near_tex_clr = bpy.props.FloatVectorProperty(
        name        = "Far Area",
        description = "",
        subtype     = 'COLOR',
        min         = 0.0,
        max         = 1.0,
        soft_min    = 0.0,
        soft_max    = 1.0,
        default     = (0,0,0)
    )

    inside_tex_clr = bpy.props.FloatVectorProperty(
        name        = "Far Area",
        description = "",
        subtype     = 'COLOR',
        min         = 0.0,
        max         = 1.0,
        soft_min    = 0.0,
        soft_max    = 1.0,
        default     = (0,0,0)
    )

    outside_tex_clr = bpy.props.FloatVectorProperty(
        name        = "Far Area",
        description = "",
        subtype     = 'COLOR',
        min         = 0.0,
        max         = 1.0,
        soft_min    = 0.0,
        soft_max    = 1.0,
        default     = (0,0,0)
    )

    objects = bpy.props.StringProperty(
        name = "Objects",
    )

    groups = bpy.props.StringProperty(
        name = "Groups",
    )


def DrawColorAndTexture(layout, ptr, texProp, label):
    colorProp = texProp + "_clr"

    col = layout.column(align=True)
    col.label(label+":")
    col.prop(ptr, colorProp, text="")
    col.prop_search(ptr, texProp, bpy.data, 'textures', text="")


class TexDistanceUI(ui.VRayTexturePanel, bpy.types.Panel):
    bl_label = "Distance"

    COMPAT_ENGINES = {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

    @classmethod
    def poll(cls, context):
        tex = context.texture
        if not tex:
            return False
        vtex = tex.vray
        engine = context.scene.render.engine
        return ((tex.type == 'VRAY' and vtex.type == ID) and (engine in __class__.COMPAT_ENGINES))

    def draw(self, context):
        layout = self.layout

        TexDistance = getattr(context.texture.vray, PLUG)

        row = layout.row()
        row.prop_search(TexDistance,   'objects',
                        context.scene, 'objects',
                        text="")
        row.prop_search(TexDistance, 'groups',
                        bpy.data,    'groups',
                        text="")

        layout.separator()

        col = layout.column(align=True)
        col.prop(TexDistance, 'distance')
        col.prop_search(TexDistance, 'distance_tex', bpy.data, 'textures', text="")

        split = layout.split()
        DrawColorAndTexture(split.column(), TexDistance, 'far_tex', "Far Area")
        DrawColorAndTexture(split.column(), TexDistance, 'near_tex', "Near Area")

        split = layout.split()
        col = split.column()
        DrawColorAndTexture(col, TexDistance, 'inside_tex', "Inside Area")
        col.prop(TexDistance, 'inside_separate')
        col.prop(TexDistance, 'inside_solid')
        col = split.column()
        DrawColorAndTexture(col, TexDistance, 'outside_tex', "Outside Area")
        col.prop(TexDistance, 'outside_separate')
        col.prop(TexDistance, 'outside_solid')


def write(bus):
    scene = bus['scene']
    ofile = bus['files']['textures']

    texture = bus['mtex']['texture']
    texName = bus['mtex']['name']

    ptr = texture.vray.TexDistance

    distance = "%s::out_intensity" % utils.getTexByName(ptr.distance_tex) if ptr.distance_tex else ptr.distance

    far_tex  = utils.getTexByName(ptr.far_tex)  if ptr.far_tex else ptr.far_tex_clr
    near_tex = utils.getTexByName(ptr.near_tex) if ptr.near_tex else ptr.near_tex_clr

    inside_tex  = utils.getTexByName(ptr.inside_tex)  if ptr.inside_tex else ptr.inside_tex_clr
    outside_tex = utils.getTexByName(ptr.outside_tex) if ptr.outside_tex else ptr.outside_tex_clr

    objects = ",".join([utils.get_name(ob, prefix='OB') for ob in utils.generate_object_list(ptr.objects, ptr.groups)])

    ofile.write("\nTexDistance %s {" % texName)
    ofile.write("\n\tobjects=List(%s);" % objects)
    ofile.write("\n\tdistance=%s;" % utils.a(scene, distance))
    ofile.write("\n\tfar_tex=%s;" % utils.a(scene, far_tex))
    ofile.write("\n\tnear_tex=%s;" % utils.a(scene, near_tex))
    ofile.write("\n\tinside_tex=%s;" % utils.a(scene, inside_tex))
    ofile.write("\n\tinside_solid=%s;" % utils.a(scene, ptr.inside_solid))
    ofile.write("\n\tinside_separate=%s;" % utils.a(scene, ptr.inside_separate))
    ofile.write("\n\toutside_tex=%s;" % utils.a(scene, outside_tex))
    ofile.write("\n\toutside_solid=%s;" % utils.a(scene, ptr.outside_solid))
    ofile.write("\n\toutside_separate=%s;" % utils.a(scene, ptr.outside_separate))
    ofile.write("\n}\n")

    return texName


def add_properties(VRayTexture):
    VRayTexture.TexDistance = bpy.props.PointerProperty(
        name        = "TexDistance",
        type        =  TexDistance,
        description = "V-Ray TexDistance settings"
    )


def GetRegClasses():
    return (
        TexDistance,
        TexDistanceUI,
    )


def register():
    for regClass in GetRegClasses():
        bpy.utils.register_class(regClass)


def unregister():
    for regClass in GetRegClasses():
        bpy.utils.unregister_class(regClass)
