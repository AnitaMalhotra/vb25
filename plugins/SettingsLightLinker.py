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

from vb25 import utils
from vb25 import dbg


TYPE = 'SETTINGS'
ID   = 'SettingsLightLinker'
NAME = 'Light Linker'
DESC = "Light Linker settings."

PARAMS = ()


def add_properties(p):
    pass


def write(bus):
    ofile = bus['files']['lights']
    scene = bus['scene']

    if not bus['lightlinker']:
        return

    ignored_lights = []
    # ignored_shadow_lights = []

    for light in bus['lightlinker']:
        lightSettings = bus['lightlinker'][light]

        hasInclude = len(lightSettings.get('include', ()))
        hasExclude = len(lightSettings.get('exclude', ()))

        if not (hasInclude or hasExclude):
            continue

        # If exclude then add as is
        exclude = set()
        if hasExclude:
            for ob in lightSettings['exclude']:
                exclude.add(utils.get_name(ob, prefix='OB'))

        # If include then add all others that are not in the list
        if hasInclude:
            for ob in utils.GeometryObjectIt(scene):
                if ob not in lightSettings['include']:
                    exclude.add(utils.get_name(ob, prefix='OB'))

        ignored_lights.append("List(%s,%s)" % (light, ",".join(exclude)))

    ofile.write("\n{ID} {ID} {{".format(ID=ID))
    ofile.write("\n\tignored_lights=List(%s);" % ",".join(ignored_lights))
    # ofile.write("\n\tignored_shadow_lights=List(%s);\n" % ignored_shadow_lights)
    ofile.write("\n}\n")
