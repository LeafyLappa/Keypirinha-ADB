import keypirinha
import keypirinha_util
import shutil
import os
import time

class Adb(keypirinha.Plugin):
    def __init__(self):
        self.item_creator = ItemCreator(self)

    def on_start(self):
        self.set_default_icon(self.load_icon("res://{}/adb.ico".format(self.package_full_name())))

    def on_events(self, flags):
        if flags & keypirinha.Events.PACKCONFIG:
            self.on_catalog()

    def on_catalog(self):
        catalog = [self.item_creator.adb()]
        self.set_catalog(catalog)

    def on_suggest(self, user_input, items_chain):
        if not items_chain:
            return
        elif items_chain[-1].target() == "menu_input_text":
            if user_input:
                self.set_suggestions([self.item_creator.input_text(user_input)])
        else:
            suggestions = [
                self.item_creator.stream_screen(),
                self.item_creator.press_power_button(),
                self.item_creator.press_home_button(),
                self.item_creator.press_volume_up_button(),
                self.item_creator.press_volume_down_button(),
                self.item_creator.press_menu_button(),
                self.item_creator.press_back_button(),
                self.item_creator.input_text_menu(),
                self.item_creator.screencap(),
            ]
            self.set_suggestions(suggestions)

    def on_execute(self, item, action):
        if item.target() == "action_stream":
            keypirinha_util.shell_execute(thing="scrcpy", show=0)
        elif item.target() == "action_screencap":
            desktop_path = os.path.join(os.path.expandvars("%USERPROFILE%"),"Desktop")
            screencap_path = "/sdcard/screencap.png"

            cmd_screencap = f"adb shell screencap -p {screencap_path}".split()
            cmd_pull = f"adb pull {screencap_path} {desktop_path}".split()

            keypirinha_util.shell_execute(thing=cmd_screencap[0], args=cmd_screencap[1:], show=0)
            time.sleep(0.5)
            keypirinha_util.shell_execute(thing=cmd_pull[0], args=cmd_pull[1:], show=0)
        else:
           cmd = item.short_desc().split()
           keypirinha_util.shell_execute(thing=cmd[0], args=cmd[1:], show=0)


class ItemCreator:
    def __init__(self, plugin: keypirinha.Plugin):
        self.plugin = plugin

    def adb(self):
        path = shutil.which("adb")
        description = f"Using ADB: {path}" if path is not None else "Warning: could not find adb on PATH!" 
        return self.plugin.create_item(
            category=keypirinha.ItemCategory.KEYWORD,
            label="Android Debug Bridge Snippets",
            short_desc=description,
            target="adb",
            args_hint=keypirinha.ItemArgsHint.REQUIRED,
            hit_hint=keypirinha.ItemHitHint.KEEPALL
        )

    def stream_screen(self):
        path = shutil.which("scrcpy")
        description = f"Using scrcpy: {path}" if path is not None else "Warning: could not find scrcpy on PATH!" 
        return self.plugin.create_item(
            category=keypirinha.ItemCategory.CMDLINE,
            label="Stream device screen",
            short_desc=description,
            target="action_stream",
            args_hint=keypirinha.ItemArgsHint.FORBIDDEN,
            hit_hint=keypirinha.ItemHitHint.IGNORE
        )

    def press_power_button(self):
        return self.plugin.create_item(
            category=keypirinha.ItemCategory.CMDLINE,
            label="Emulate power button",
            short_desc="adb shell input keyevent 26",
            target="action_keyevent_power",
            args_hint=keypirinha.ItemArgsHint.FORBIDDEN,
            hit_hint=keypirinha.ItemHitHint.IGNORE
        )

    def press_home_button(self):
        return self.plugin.create_item(
            category=keypirinha.ItemCategory.CMDLINE,
            label="Emulate home button",
            short_desc="adb shell input keyevent 3",
            target="action_keyevent_home",
            args_hint=keypirinha.ItemArgsHint.FORBIDDEN,
            hit_hint=keypirinha.ItemHitHint.IGNORE
        )

    def press_volume_up_button(self):
        return self.plugin.create_item(
            category=keypirinha.ItemCategory.CMDLINE,
            label="Emulate volume up button",
            short_desc="adb shell input keyevent 24",
            target="action_keyevent_volume_up",
            args_hint=keypirinha.ItemArgsHint.FORBIDDEN,
            hit_hint=keypirinha.ItemHitHint.IGNORE
        )

    def press_volume_down_button(self):
        return self.plugin.create_item(
            category=keypirinha.ItemCategory.CMDLINE,
            label="Emulate volume down button",
            short_desc="adb shell input keyevent 25",
            target="action_keyevent_volume_down",
            args_hint=keypirinha.ItemArgsHint.FORBIDDEN,
            hit_hint=keypirinha.ItemHitHint.IGNORE
        )

    def press_menu_button(self):
        return self.plugin.create_item(
            category=keypirinha.ItemCategory.CMDLINE,
            label="Emulate menu button",
            short_desc="adb shell input keyevent 1",
            target="action_keyevent_menu",
            args_hint=keypirinha.ItemArgsHint.FORBIDDEN,
            hit_hint=keypirinha.ItemHitHint.IGNORE
        )

    def press_back_button(self):
        return self.plugin.create_item(
            category=keypirinha.ItemCategory.CMDLINE,
            label="Emulate back button",
            short_desc="adb shell input keyevent 4",
            target="action_keyevent_back",
            args_hint=keypirinha.ItemArgsHint.FORBIDDEN,
            hit_hint=keypirinha.ItemHitHint.IGNORE
        )


    def input_text_menu(self):
        return self.plugin.create_item(
            category=keypirinha.ItemCategory.KEYWORD,
            label="Emulate text input",
            short_desc="adb shell input text",
            target="menu_input_text",
            args_hint=keypirinha.ItemArgsHint.REQUIRED,
            hit_hint=keypirinha.ItemHitHint.IGNORE
        )

    def input_text(self, text):
        return self.plugin.create_item(
            category=keypirinha.ItemCategory.CMDLINE,
            label=text,
            short_desc=f"adb shell input text {text}",
            target="action_input_text",
            args_hint=keypirinha.ItemArgsHint.FORBIDDEN,
            hit_hint=keypirinha.ItemHitHint.IGNORE,
        )

    def screencap(self):
        desktop_path = os.path.join(os.path.expandvars("%USERPROFILE%"),"Desktop")
        screencap_path = "/sdcard/screencap.png"
        return self.plugin.create_item(
            category=keypirinha.ItemCategory.CMDLINE,
            label="Take a screencap",
            short_desc=f"adb shell screencap -p {screencap_path} && adb pull {screencap_path} {desktop_path}",
            target="action_screencap",
            args_hint=keypirinha.ItemArgsHint.FORBIDDEN,
            hit_hint=keypirinha.ItemHitHint.IGNORE
        )