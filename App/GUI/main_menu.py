# Contains main menu function

# Importing dependencies
from App.AppLib.config import Config
import App.GUI.customtkinter as ctk
from tkinterdnd2 import DND_FILES
from App.FFLib.AINB import AINB
from tkinter import messagebox
from tkinter import filedialog
from functools import partial
import pygments.lexers.data
import chlorophyll


# _func class
class _Func:
    @staticmethod
    def update_ainb_editor(variables):

        if variables["open_file"] is None:
            variables["CodeBox"].delete(0.0, "end")
            return 0

        CodeBox = variables["CodeBox"]
        file = AINB(variables["open_file"], 'fp')
        CodeBox.insert(0.0, file.json)

    @staticmethod
    def focus_in_romfs_entry(romfs_path_label, event=None):
        romfs_path_label.configure(
            text="Game Dump Location*                                                                      "
        )

    @staticmethod
    def update_romfs_entry(app, romfs_path_entry, romfs_path_label, event=None):
        romfs_path = romfs_path_entry.get()
        app.settings["romfs_path"] = romfs_path
        Config.overwrite_setting("romfs_path", romfs_path)
        romfs_path_label.configure(
            text="Game Dump Location                                                                        "
        )

    @staticmethod
    def update_theme_option_menu(theme_option_menu):
        match Config.get_setting("current_theme"):
            case "dark":
                theme_option_menu.set("Dark")
            case "light":
                theme_option_menu.set("Light")
            case "system":
                theme_option_menu.set("System")

    @staticmethod
    def drop_file(tabview, variables, event=None):
        variables["open_file"] = str(event.data[1:len(event.data)-1])

        if variables["open_file"] is not None:
            continueQuitPopup = messagebox.askokcancel(
                title="AINB-Toolbox Popup",
                message="Opening this file will get rid of the last file you were editing.\nDo you want to continue?"
            )

            if continueQuitPopup is False:
                return 0

        _Func.update_ainb_editor(variables)
        tabview.set("AINB Editor")


# Button func
class ButtonFunc:
    @staticmethod
    def save_ainb_button_command(variables, codeview):
        pass  # TODO: Stub

    @staticmethod
    def export_ainb_button_command(variables, codeview):
        pass  # TODO: Stub

    @staticmethod
    def tabview_command(tabview, variables):
        _Func.update_ainb_editor(variables)

    @staticmethod
    def romfs_path_browse_button_command(app, romfs_path_entry):
        romfs_path = filedialog.askdirectory(title="Select Tears of the Kingdom RomFS Folder")
        if romfs_path == "":
            return 0
        else:
            app.settings["romfs_path"] = romfs_path
            Config.overwrite_setting("romfs_path", romfs_path)
            romfs_path_entry.delete(0, "end")
            romfs_path_entry.insert(0, romfs_path)

    @staticmethod
    def export_all_ainb_button_command(app):
        pass  # TODO: Stub

    @staticmethod
    def theme_option_menu_button_command(app, dragAndDropTarget, appearance):
        ctk.set_appearance_mode(appearance.lower())
        app.settings["current_theme"] = appearance.lower()
        Config.overwrite_setting("current_theme", appearance.lower())

        if ctk.get_appearance_mode() == "Dark":
            dragAndDropTarget.configure(fg_color="#242424")
        else:
            dragAndDropTarget.configure(fg_color="#EBEBEB")

    @staticmethod
    def drag_and_drop_button_command(tabview, variables, event=None):

        supportedFileFormats = (
            (
                'All Editable Files', [
                    '*.ainb'
                ]
            ),
            ('AI Node Binary', '*.ainb')
        )

        fp = filedialog.askopenfile(title="Select a file", filetypes=supportedFileFormats)

        if fp is None:
            return 1

        if variables["open_file"] is not None:
            continueQuitPopup = messagebox.askokcancel(
                title="AINB-Toolbox Popup",
                message="Opening this file will get rid of the last file you were editing.\nDo you want to continue?"
            )
            if continueQuitPopup is False:
                return 0

        variables["open_file"] = fp.name

        _Func.update_ainb_editor(variables)
        tabview.set("AINB Editor")


# main_menu function
def main_menu(app):

    # Detecting if the romfs_path is None
    if app.settings["romfs_path"] is None:

        # Asking user to provide romfs path
        continue_prompt = False
        while continue_prompt is False:
            messagebox.showinfo("AINB-Toolbox Pop-up", "Please select your romfs folder.")
            romfs_folder = filedialog.askdirectory(title="Select RomFS Folder Path")
            if romfs_folder == "":
                continue_prompt = messagebox.askyesno("AINB-Toolbox Pop-up",
                                    "Do you want to continue without a romfs dump?\nThis will most likely cause a lot of errors in the future.")
            else:
                app.settings["romfs_path"] = romfs_folder
                Config.overwrite_setting("romfs_path", romfs_folder)
                continue_prompt = False

    # Setting theme
    ctk.set_appearance_mode(app.settings["current_theme"])

    # Creating variables
    variables = {
        "open_file": None
    }

    # Creating root window
    root = ctk.CTk()
    root.title("AINB-Toolbox - VillainousSsnake - Alpha V0.1")
    root.geometry("850x525+200+200")

    # Defining on_close function
    def on_close():
        root.destroy()
        app.returnStatement = "exit"

    # Assigning the buttons on the tkinter window top bar
    root.protocol("WM_DELETE_WINDOW", on_close)

    # Creating tabview
    tabview = ctk.CTkTabview(root, height=1000)
    tabview_command = partial(ButtonFunc.tabview_command, tabview, variables)
    tabview.configure(command=tabview_command)
    tabview.add("Home")
    tabview.add("AINB Editor")
    tabview.add("Settings")
    tabview.set("Home")
    tabview.pack(fill=ctk.BOTH)

    #
    #
    #
    #
    #                      ########################
    #                      #    "Home" SECTION    #
    #                      ########################


    dragAndDropTarget = ctk.CTkLabel(tabview.tab("Home"), font=("Ariel", 20),
                                     text="➕ \nDrag & Drop Here",
                                     corner_radius=10, wraplength=300)
    if ctk.get_appearance_mode() == "Dark":
        dragAndDropTarget.configure(fg_color="#242424")
    else:
        dragAndDropTarget.configure(fg_color="#EBEBEB")
    dragAndDropTarget.pack(expand=True, fill=ctk.BOTH, padx=40, pady=40)

    drop_partial = partial(_Func.drop_file, tabview, variables)
    dragAndDropTarget.drop_target_register(DND_FILES)
    dragAndDropTarget.dnd_bind("<<Drop>>", drop_partial)
    drag_and_drop_button_command = partial(ButtonFunc.drag_and_drop_button_command, tabview, variables)
    dragAndDropTarget.bind("<1>", drag_and_drop_button_command)

    export_all_ainb_button_partial = partial(ButtonFunc.export_all_ainb_button_command, app)
    export_all_ainb_button = ctk.CTkButton(master=tabview.tab("Home"),
                                           text="Extract all AINB from RomFS Dump",
                                           command=export_all_ainb_button_partial)
    export_all_ainb_button.pack()

    #
    #
    #
    #
    #                      ############################
    #                      #    "Settings" SECTION    #
    #                      ############################

    root.columnconfigure(0)
    root.columnconfigure(1)

    romfs_path_label = ctk.CTkLabel(
        master=tabview.tab("Settings"),
        text="Game Dump Location                                                                        ",
        corner_radius=5, fg_color="#3B8ED0"
    )
    romfs_path_label.grid(row=0, column=0, padx=20, pady=10)

    romfs_path_entry = ctk.CTkEntry(master=tabview.tab("Settings"))
    if app.settings["romfs_path"] is None:
        romfs_path_entry.configure(placeholder_text="Eg. (D:\\Tears of the Kingdom\\romfs)")
    else:
        romfs_path_entry.insert(0, app.settings["romfs_path"])
    romfs_path_entry.grid(row=0, column=1, padx=20, pady=10)
    romfs_path_entry_command_partial = partial(_Func.update_romfs_entry, app, romfs_path_entry, romfs_path_label)
    romfs_path_entry_focus_partial = partial(_Func.focus_in_romfs_entry, romfs_path_label)
    romfs_path_entry.bind("<Return>", romfs_path_entry_command_partial)
    romfs_path_entry.bind("<Key>", romfs_path_entry_focus_partial)

    romfs_browse_command = partial(ButtonFunc.romfs_path_browse_button_command, app, romfs_path_entry)
    romfs_path_browse = ctk.CTkButton(
        tabview.tab("Settings"),
        text="Browse...", fg_color="grey",
        command=romfs_browse_command,
    )
    romfs_path_browse.grid(row=0, column=3)

    theme_label = ctk.CTkLabel(
        master=tabview.tab("Settings"),
        text="Current Theme                                                                                    ",
        corner_radius=5, fg_color="#3B8ED0"
    )
    theme_label.grid(row=1, column=0, padx=20, pady=10)

    theme_option_menu_command = partial(ButtonFunc.theme_option_menu_button_command, app, dragAndDropTarget)
    theme_option_menu = ctk.CTkOptionMenu(
        master=tabview.tab("Settings"),
        values=["Dark", "Light", "System"],
        command=theme_option_menu_command
    )
    _Func.update_theme_option_menu(theme_option_menu)
    theme_option_menu.grid(row=1, column=1, padx=20, pady=10)

    #
    #
    #
    #
    #                      ###############################
    #                      #    "AINB Editor" SECTION    #
    #                      ###############################

    # Creating and configuring the CodeView
    CodeBox = chlorophyll.CodeView(
        master=tabview.tab("AINB Editor"), lexer=pygments.lexers.data.JsonLexer, color_scheme="dracula", height=1000,
    )
    CodeBox.pack(fill="both", pady=50)
    variables["CodeBox"] = CodeBox

    # Creating save button
    save_ainb_button_command = partial(ButtonFunc.export_ainb_button_command, variables, CodeBox)
    save_ainb_button = ctk.CTkButton(master=tabview.tab("AINB Editor"), text="Save",
                                     command=save_ainb_button_command)
    save_ainb_button.place(x=0, y=0)

    # Creating export button
    export_ainb_button_command = partial(ButtonFunc.export_ainb_button_command, variables, CodeBox)
    export_ainb_button = ctk.CTkButton(master=tabview.tab("AINB Editor"), text="Export",
                                       command=export_ainb_button_command)
    export_ainb_button.place(x=150, y=0)

    # Updating to ainb_editor
    _Func.update_ainb_editor(variables)

    # Root mainloop
    root.mainloop()
