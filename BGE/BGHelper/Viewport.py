"""
Copyright (c) 2013-2014 SolarLune

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files
(the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

P.S. It would be nice if you could attribute me for the creation of this and my other scripts. Thanks!
"""

# View port-related code for the BGE.

import collections

import bge


class CViewManager():
    """
    A static class that you don't have to instantiate to use.
    """

    AH_NONE = 0

    AH_VERTICAL = 1  # Increases from first camera added at top to last camera added at bottom
    AH_VERTICAL_REVERSED = 2  # Goes the other way

    AH_HORIZONTAL = 3  # Increases from first camera added at left to last camera added at right
    AH_HORIZONTAL_REVERSED = 4  # Goes...

    def __init__(self):

        self.views = collections.OrderedDict()  # Views and their setups.

        self.remove_all_views()  # Initialize view dictionary

    def add_view(self, name, auto_set_hint=AH_NONE):

        self.views[name] = {'camera': None,
                            'w': 0.0,
                            'h': 0.0,
                            'x': 0.0,
                            'y': 0.0,
        }

        if auto_set_hint != self.AH_NONE:

            num_of_views = len(self.views)

            for v in self.views:

                view = self.views[v]
                v_index = list(self.views.keys()).index(v)

                if auto_set_hint == self.AH_HORIZONTAL:

                    self.set_view_position(v, ((1.0 / num_of_views) * v_index), 0.0)
                    self.set_view_size(v, 1.0 / num_of_views, 1.0)

                elif auto_set_hint == self.AH_HORIZONTAL_REVERSED:

                    self.set_view_position(v, 1.0 - ((1.0 / num_of_views) * (v_index + 1)), 0.0)
                    self.set_view_size(v, 1.0 / num_of_views, 1.0)

                elif auto_set_hint == self.AH_VERTICAL:

                    self.set_view_position(v, 0.0, 1.0 - ((1.0 / num_of_views) * (v_index + 1)))
                    self.set_view_size(v, 1.0, 1.0 / num_of_views)

                elif auto_set_hint == self.AH_VERTICAL_REVERSED:

                    self.set_view_position(v, 0.0, (1.0 / num_of_views) * v_index)
                    self.set_view_size(v, 1.0, 1.0 / num_of_views)

            pass  # Reconfigure the views to orient correctly

        self.update_views()

    def remove_view(self, name):

        del self.views[name]
        self.update_views()

    def remove_all_views(self):

        self.views.clear()  # Clear views to ensure that you're not dealing with any
        self.add_view('default')  # Add a default view (the current one)
        self.set_view_size('default', 1.0, 1.0)  # View size is set in fractions for ease of use
        self.set_camera('default', bge.logic.getCurrentScene().active_camera)  # Set the camera to be the active one

        self.update_views()

    def set_camera(self, name, camera):

        self.views[name]['camera'] = camera
        self.update_views()

    def set_view_size(self, name, width, height):

        self.views[name]['w'] = width
        self.views[name]['h'] = height
        self.update_views()

    def set_view_position(self, name, pos_x, pos_y):

        self.views[name]['x'] = pos_x
        self.views[name]['y'] = pos_y
        self.update_views()

    def update_views(self):

        for v in self.views:

            view = self.views[v]

            view_cam = view['camera']

            if view_cam is not None and not view_cam.invalid:

                assert isinstance(view_cam, bge.types.KX_Camera)

                win_w = bge.render.getWindowWidth()
                win_h = bge.render.getWindowHeight()

                view_cam.setViewport(int(view['x'] * win_w), int(view['y'] * win_h),
                                     int(view['x'] * win_w) + int(view['w'] * win_w),
                                     int(view['y'] * win_h) + int(view['h'] * win_h))

                if len(self.views) > 1:  # You're not just using one view

                    view_cam.useViewport = True

                else:

                    view_cam.useViewport = False  # Gotta test this out

            else:

                if view_cam is not None and view_cam.invalid:
                    print('ERROR: Camera for view ' + v + ' has become invalid.')

                    view['camera'] = None


manager = CViewManager()