'''
Common Unit Conversion Functions
'''
import re
import bpy
from decimal import *

def inch(inch):
    """ Converts inch to meter
    """
    return round(inch / 39.3700787,6)

def feet(inch):
    """ Converts feet to meter
    """
    return round(inch / 3.28084,6)

def millimeter(millimeter):
    """ Converts millimeter to meter
    """
    return millimeter * .001

def centimeter(millimeter):
    """ Converts centimeter to meter
    """
    return millimeter * .01

def meter_to_feet(meter):
    """ Converts meter to feet
    """
    return round(meter * 3.28084,6)

def meter_to_inch(meter):
    """ Converts meter to inch
    """
    return round(meter * 39.3700787,6)

def meter_to_millimeter(meter):
    """ Converts meter to millimeter
    """
    return meter * 1000

def meter_to_centimeter(meter):
    """ Converts meter to centimeter
    """
    return meter * 100

def meter_to_active_unit(meter):
    """ Converts meter to active unit
    """
    if bpy.context.scene.unit_settings.system == 'METRIC':
        return meter_to_millimeter(meter)
    else:
        return meter_to_inch(meter)
    
def meter_to_exact_unit(meter):
    """ Converts meter to active unit
        Ensuring it doesn't round the value
    """
    if bpy.context.scene.unit_settings.system == 'METRIC':
        return meter_to_millimeter(meter)
    else:
        return meter * 39.3700787
    
def inch_to_millimeter(inch):
    """ Converts inch to millimeter
    """
    return inch * 25.4

def decimal_inch_to_millimeter(inch):
    """ Converts inch to millimeter returned as a decimal object
    """
    return Decimal(str(inch)) * Decimal(str(25.4))

def unit_to_string(unit_settings,value):
    if unit_settings.system == 'METRIC':
        if unit_settings.length_unit == 'METERS':
            return str(round(value,3)) + "m"
        else:
            return str(round(meter_to_millimeter(value),2)) + "mm"
    elif unit_settings.system == 'IMPERIAL':
        if unit_settings.length_unit == 'FEET':
            return str(round(meter_to_feet(value),2)) + "'"
        else:
            return str(round(meter_to_inch(value),4)) + '"'
    else:
        return str(round(value,4))

def parse_feet_and_inches(input_str):
    # Define a regular expression pattern to match feet and inches notation with optional parts
    pattern = re.compile(r'^(?:(?P<feet>\d+)\')?(?:(?P<inches>\d+)\"?)?$')

    # Use regular expression to extract feet and inches
    match = pattern.match(input_str)

    if match:
        feet = int(match.group('feet')) if match.group('feet') else 0
        inches = int(match.group('inches')) if match.group('inches') else 0
        return feet, inches
    else:
        raise ValueError(f"Invalid input format. Please use the format X'Y\" or X' or Y\". Got {input_str}")
