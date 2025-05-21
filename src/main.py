import subprocess
import os
import shutil
import re

TEMP_FOLDER = os.path.join(os.path.dirname(__file__), "../temp")
THEME_FOLDER = os.path.join(TEMP_FOLDER, "shell-theme", "theme")

ORIGINAL_COMPILED_THEME = "/usr/share/gnome-shell/gnome-shell-theme.gresource"

OWN_THEME_XML = os.path.join(THEME_FOLDER, "gnome-shell-theme.gresource.xml")
OWN_THEME_COMPILED = OWN_THEME_XML.replace(".xml", "")
OWN_THEME_DARK_CSS = os.path.join(THEME_FOLDER, "gnome-shell-dark.css")
OWN_THEME_LIGHT_CSS = os.path.join(THEME_FOLDER, "gnome-shell-light.css")


def create_temp_folder() -> None:
    print("Creating temp folder...")
    if not os.path.exists(TEMP_FOLDER):
        os.makedirs(TEMP_FOLDER)
        print(f"Temp folder created at {TEMP_FOLDER}")
    else:
        print(f"Temp folder already exists at {TEMP_FOLDER}")


def extract_gdm_theme() -> None:
    print("Extracting GDM theme...")
    cmd = [
        "bash",
        os.path.join(os.path.dirname(__file__), "../scripts/extract_gst.sh"),
        TEMP_FOLDER,
    ]
    try:
        subprocess.check_output(cmd, text=True)

        print("GDM theme extracted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error extracting GDM theme: {e.output}")
        exit(1)


def copy_current_wallpaper_to_theme_folder() -> None:
    print("Copying wallpaper to theme folder...")
    # TODO: Check if the user is using Gnome, if not, try to get the wallpaper using another method
    cmd = ["gsettings", "get", "org.gnome.desktop.background", "picture-uri"]
    try:
        output = subprocess.check_output(cmd, text=True)
        print("Wallpaper URI:", output.strip())

        wallpaper_path = output.strip().replace("file://", "")
        wallpaper_path = wallpaper_path.replace("'", "")
        copiedFile = shutil.copy2(wallpaper_path, THEME_FOLDER)
        dest_path = os.path.join(THEME_FOLDER, "wallpaper.png")

        os.rename(copiedFile, dest_path)
        print(f"Copied wallpaper to {dest_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error copying current wallpaper {e}")
        exit(1)


def create_own_theme_file() -> None:
    print("Creating own theme...")
    open(OWN_THEME_XML, "w").close()
    try:
        with open(OWN_THEME_XML, "w") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write("<gresources>\n")
            f.write('  <gresource prefix="/org/gnome/shell/theme">\n')
            f.write("    <file>calendar-today.svg</file>\n")
            f.write("    <file>calendar-today-light.svg</file>\n")
            f.write("    <file>gnome-shell-dark.css</file>\n")
            f.write("    <file>gnome-shell-light.css</file>\n")
            f.write("    <file>gnome-shell-high-contrast.css</file>\n")
            f.write("    <file>gnome-shell-start.svg</file>\n")
            f.write("    <file>pad-osd.css</file>\n")
            f.write("    <file>workspace-placeholder.svg</file>\n")
            f.write("    <file>wallpaper.png</file>\n")
            f.write("  </gresource>\n")
            f.write("</gresources>\n")

        print(f"Created {OWN_THEME_XML}")
    except Exception as e:
        print(f"Error creating own theme file: {e}")
        exit(1)


def change_wallpaper_style_on_css() -> None:
    print("Changing wallpaper style on CSS...")
    try:
        style_files = [OWN_THEME_DARK_CSS, OWN_THEME_LIGHT_CSS]

        for style_file in style_files:
            with open(style_file, "r") as f:
                content = f.read()
                pattern = r"#lockDialogGroup\s*\{[^}]*\}"
                content = re.sub(pattern, "", content, flags=re.DOTALL)
                content += "\n"
                content += "#lockDialogGroup {\n"
                content += "    background: url('wallpaper.png');\n"
                content += "    background-size: auto;\n"
                content += "    background-repeat: no-repeat;\n"
                content += "}\n"
            with open(style_file, "w") as f:
                f.write(content)
    except Exception as e:
        print(f"Error changing wallpaper style: {e}")
        exit(1)


def compile_gresource() -> None:
    print("Compiling GResource...")
    cmd = ["glib-compile-resources", "--sourcedir=" + THEME_FOLDER, OWN_THEME_XML]
    try:
        subprocess.check_output(cmd, text=True)
        print("GResource compiled successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error compiling GResource: {e}")
        exit(1)


def backup_original_gdm_theme() -> None:
    print("Backing up original GDM theme...")
    BACKUP_COMPILED_THEME = ORIGINAL_COMPILED_THEME + ".bak"
    if not os.path.exists(BACKUP_COMPILED_THEME):
        try:
            cmd = ["sudo", "cp", ORIGINAL_COMPILED_THEME, BACKUP_COMPILED_THEME]

            result = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
            )

            print(f"Original GDM theme backed up to {BACKUP_COMPILED_THEME}")
        except subprocess.CalledProcessError as e:
            print(f"Error doing backup of GDM original theme: {e}")
            exit(1)
    else:
        print("No original GDM theme found to back up.")


def main() -> None:
    create_temp_folder()
    extract_gdm_theme()
    copy_current_wallpaper_to_theme_folder()
    create_own_theme_file()
    change_wallpaper_style_on_css()
    compile_gresource()
    backup_original_gdm_theme()


if __name__ == "__main__":
    main()
