#    callirhoe - high quality calendar rendering
#    Copyright (C) 2012 George M. Tzoumas

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/

# --- style.rainbow_gfs ---

"""module defining rainbow color & gfs style"""

import gfs

# day of week
class dow(gfs.dow): pass
    
# day of month
class dom(gfs.dom): pass

class dom_weekend(gfs.dom_weekend): pass 

class dom_holiday(gfs.dom_holiday): pass
    
class dom_weekend_holiday(gfs.dom_weekend_holiday): pass

class dom_phantom(gfs.dom_phantom): pass

class dom_weekend_phantom(gfs.dom_weekend_phantom): pass

class dom_multi(gfs.dom_multi): pass

class dom_weekend_multi(gfs.dom_weekend_multi): pass

from lib.geom import color_mix, color_scale, color_auto_fg

class month(gfs.month):
    winter = (0,0.5,1)
    spring = (0.0,0.7,0.0)
    summer = (1,0.3,0)
    autumn = (0.9,0.9,0)
    _c1 = ((0,0,0), winter,
        color_mix(winter,spring,0.66), color_mix(winter,spring,0.33), spring, # april
        color_mix(spring,summer,0.66), color_mix(spring,summer,0.33), summer, # july
        color_mix(summer,autumn,0.66), color_mix(summer,autumn,0.33), autumn, # october
        color_mix(autumn,winter,0.66), color_mix(autumn,winter,0.33)) # december
    color_map_bg = (map(lambda x: color_scale(x, 0.5), _c1), _c1)
    color_map_fg = (((1,1,1),)*13, ((0,0,0),)*13)
#                    map(lambda x: color_auto_fg(x), color_map_bg[1]
