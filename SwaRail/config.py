from ursina import window, Ursina, camera, color, Vec3


SwaRailApplication = Ursina()


# setting up windows

window.title = 'My Game'                # The window title
window.borderless = False               # Show a border
window.fullscreen = False               # Do not go Fullscreen
window.exit_button.visible = False      # Do not show the in-game red X that loses

window.color = color.black90            # TODO :- find out about different shades of black

# setting up camera

camera.x += (window.size.x / 100) - 2.5
camera.y -= (window.size.y / 100) - 4

camera.position += Vec3(32.5, 0, -90)