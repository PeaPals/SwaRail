from ursina import held_keys, camera, time, mouse, Vec3
from SwaRail.Frontend import constants


APPLICATION_IS_PAUSED = False

def _check_keyboard_navigations():
    
    # movement checks
    if held_keys['w']:
        camera.y += constants.CAMERA_NAVIGATION_SPEED * time.dt

    elif held_keys['a']:
        camera.x -= constants.CAMERA_NAVIGATION_SPEED * time.dt

    elif held_keys['s']:
        camera.y -= constants.CAMERA_NAVIGATION_SPEED * time.dt

    elif held_keys['d']:
        camera.x += constants.CAMERA_NAVIGATION_SPEED * time.dt


    # zoom in and out checks # TODO :- NOT WORKING

    # elif (held_keys['control']) and (held_keys['left control'] or held_keys['right control']):
    #     pass

    elif  held_keys['z']:
        camera.z += constants.CAMERA_NAVIGATION_SPEED * time.dt

    elif held_keys['x']:
        camera.z -= constants.CAMERA_NAVIGATION_SPEED * time.dt


    # pausing and playing application checks

    elif held_keys['space']:
        if APPLICATION_IS_PAUSED:
            APPLICATION_IS_PAUSED = False
            # TODO : resume application here and enable stuff like CLI if it isn't enabled automatically
        else:
            APPLICATION_IS_PAUSED = True
            # TODO : pause application here and disable stuff like CLI if it isn't diabled automatically




INITIAL_MOUSE_POSITION = None

def _check_mouse_navigations():

    # check mouse position

    # zoom in and out checks # TODO :- NOT WORKING

    if held_keys['scroll up']:
        camera.z += constants.CAMERA_NAVIGATION_SPEED * time.dt

    elif held_keys['scroll down']:
        camera.z -= constants.CAMERA_NAVIGATION_SPEED * time.dt


def check_navigations():
    _check_keyboard_navigations()
    # _check_mouse_navigations()

    



def process_commands(command):
    pass