from ursina import InputField
import SwaRail.settings as settings
from .command_handler import CommandHandler


class CommandPanel:
    input_field = InputField(
            character_limit=settings.COMMAND_PANEL_CHARACTER_LIMIT,
            color=settings.COMMAND_PANEL_COLOR,
            position=settings.COMMAND_PANEL_POSITION
        )

    active = True

    @classmethod
    def initialize(cls):        
        # cls.input_field.scale = (0.5, .05)
        cls.input_field.submit_on = 'enter'
        cls.input_field.on_submit = cls.execute_command
        cls.toggle_state()


    @classmethod
    def execute_command(cls):
        CommandHandler.execute_command(cls.input_field.text)
        cls.input_field.text = ''
        cls.toggle_state()


    @classmethod
    def toggle_state(cls):
        if cls.active:
            cls.deactivate()
        else:
            cls.activate()


    @classmethod
    def activate(cls):
        cls.input_field.visible = True
        cls.input_field.enable()
        cls.input_field.active = True
        cls.active = True


    @classmethod
    def deactivate(cls):
        cls.input_field.visible = False
        cls.input_field.disable()
        cls.input_field.active = False
        cls.active = False