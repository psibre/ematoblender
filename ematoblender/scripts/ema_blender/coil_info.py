__author__ = 'Kristy'

import os
import json
from . import blender_shared_objects as bsh
from ..ema_shared import properties as pps


def import_sensor_info_json(jsonfilename='./sensor_info.json'):
    """Access the JSON file with information about which data corresponds to which sensor."""
    inds = {}
    outerdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))

    def find(name, path):
        for root, dirs, files in os.walk(path):
            if name in files:
                return os.path.join(root, name)
    try:
        file = find(os.path.basename(jsonfilename), outerdir)
        with open(file, 'r') as jsonfile:
            inds = json.load(jsonfile)
            bsh.local_json_copy = inds
    except FileNotFoundError:
        print("JSON FILE NOT FOUND, RECONSIDER WORKING DIR OR JSON LOCATION")
    return inds


def get_sensor_roles():
    """From the JSON file, put lists of item by behaviour into Blender's shared objects list."""

    # open the json file
    jdict = import_sensor_info_json(jsonfilename=pps.json_loc)
    bsh.ema_active_meshes, bsh.ema_biteplate_meshes, bsh.ema_reference_meshes = [], [], []

    #print(jdict); print('all objects', bsh.all_ema_meshes)

    # append the objects to the relevant sublists based on behaviour
    for ind, obj in bsh.all_ema_meshes:
        #print(ind, obj)
        sensor = jdict.get(str(ind), False)  # if there is something in the JSON file corresponding to the index
        if sensor:
            place = sensor["place"]
            bp, ref, act = jdict[str(ind)]['biteplate'],jdict[str(ind)]['reference'],jdict[str(ind)]['active']
            if bp:
                bsh.ema_biteplate_meshes.append((ind, obj, place))
            if ref:
                bsh.ema_reference_meshes.append((ind, obj, place))
            if act:
                bsh.ema_active_meshes.append((ind, obj, place))
    #print(bsh.ema_active_meshes)
    return bsh.ema_active_meshes, bsh.ema_biteplate_meshes, bsh.ema_reference_meshes


def get_sensor_roles_no_blender():
    """Get the sensor roles with no access to Blender shared objects."""
    jdict = import_sensor_info_json(jsonfilename=pps.json_loc)
    #print('jdict', jdict)
    ema_active_meshes, ema_biteplate_meshes, ema_reference_meshes = [],[],[]
    for ind in range(20):
        sensor = jdict.get(str(ind), False) # if there is something in the JSON file corresponding to the index
        if sensor:
            place = sensor["place"]
            bp, ref, act = jdict[str(ind)]['biteplate'],jdict[str(ind)]['reference'],jdict[str(ind)]['active']
            obj = None
            if bp:
                ema_biteplate_meshes.append((ind, obj, place))
            if ref:
                ema_reference_meshes.append((ind, obj, place))
            if act:
                ema_active_meshes.append((ind, obj, place))
    return ema_active_meshes, ema_biteplate_meshes, ema_reference_meshes


def find_sensor_index(name):
    """Give the index of the first sensor found with the given name."""
    if bsh.local_json_copy is None:
        import_sensor_info_json(jsonfilename=pps.json_loc)
    for ki, vi in bsh.local_json_copy.items():
        if vi.get("place", False) == name:
            return int(ki)


def find_sensor_location_by_name(name):
    i = find_sensor_index(name)
    loc = find_sensor_location_by_index(i)
    return loc


def find_sensor_location_by_index(ind):
    s = bsh.ema_mesh_name_rule(ind)
    loc = None
    try:
        import bge
        scn = bge.logic.getCurrentScene()
        obj = scn.objects[s]
        loc = obj.worldPosition
    except ImportError:
        try:
            import bpy
            obj = bpy.data.objects.get(s, False)
            if obj:
                loc = obj.location
        except ImportError:
            loc = (0, 0, 0)
    return loc


def find_transform_by_index(i):
    """From the key return any additional transformation"""
    jdict = bsh.local_json_copy if bsh.local_json_copy is not None else import_sensor_info_json(jsonfilename=pps.json_loc)
    coil = jdict.get(str(i), False)
    if coil:
        transform = coil.get('transform', False)
        if transform:
            return transform
    return (0, 0, 0)


def main():
    print(find_transform_by_index(4))
    print(find_sensor_location_by_name("UL"))
    print(find_sensor_location_by_name("SL"))
    print(find_sensor_index("TB"))

if __name__=="__main__":
    main()
