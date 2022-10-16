from ursina import held_keys, camera, time, application
# from SwaRail.Utilities.command_panel import CommandPanel
from SwaRail import settings


# APPLICATION_IS_PAUSED = False

def _check_keyboard_navigations():

    # movement checks
    if held_keys['w']:
        camera.y += settings.CAMERA_NAVIGATION_SPEED * time.dt

    elif held_keys['a']:
        camera.x -= settings.CAMERA_NAVIGATION_SPEED * time.dt

    elif held_keys['s']:
        camera.y -= settings.CAMERA_NAVIGATION_SPEED * time.dt

    elif held_keys['d']:
        camera.x += settings.CAMERA_NAVIGATION_SPEED * time.dt


    # zoom in and out checks

    elif  held_keys['z']:
        camera.z += settings.CAMERA_NAVIGATION_SPEED * time.dt

    elif held_keys['x']:
        camera.z -= settings.CAMERA_NAVIGATION_SPEED * time.dt


    # toggle command panel

    # elif held_keys['c']:
    #     CommandPanel.toggle_state()

    # pausing and playing application checks

    elif held_keys['p']:
        global APPLICATION_IS_PAUSED
        if APPLICATION_IS_PAUSED:
            APPLICATION_IS_PAUSED = False
            application.resume()
            # TODO : resume application here and enable stuff like CLI if it isn't enabled automatically
        else:
            APPLICATION_IS_PAUSED = True
            application.pause()
            # TODO : pause application here and disable stuff like CLI if it isn't diabled automatically




INITIAL_MOUSE_POSITION = None

def _check_mouse_navigations():

    # check mouse position

    # zoom in and out checks # TODO :- NOT WORKING

    if held_keys['scroll up']:
        camera.z += settings.CAMERA_NAVIGATION_SPEED * time.dt

    elif held_keys['scroll down']:
        camera.z -= settings.CAMERA_NAVIGATION_SPEED * time.dt


def check_navigations():
    # if CommandPanel.active:
    #     return None
        
    _check_keyboard_navigations()
    # _check_mouse_navigations()

    



def process_commands(command):
    pass