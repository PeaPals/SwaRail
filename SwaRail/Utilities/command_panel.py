from ursina import WindowPanel, InputField


class CommandPanel:
    input_field = InputField(character_limit=70)

    window_panel = WindowPanel(
        title='Command Panel',
        content=(
            input_field,
        )
    )

    @classmethod
    def initialize(cls):
        cls.input_field.on_submit = cls.execute_command

    @classmethod
    def execute_command(cls, value):
        print("Executed with value : ", value)