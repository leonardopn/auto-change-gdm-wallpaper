import subprocess
import os
import shutil

TEMP_FOLDER = os.path.join(os.path.dirname(__file__), "../temp")
THEME_FOLDER = os.path.join(TEMP_FOLDER, "shell-theme", "theme")
OWN_THEME_FILE = os.path.join(THEME_FOLDER, "gnome-shell-theme.gresource.xml")

def extract_gdm_theme():
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
        print(f"Error extracting GDM theme: {e}")
        exit(1)

def copy_current_wallpaper_to_theme_folder():
    print("Copying wallpaper to theme folder...")
    # TODO: Check if the user is using Gnome, if not, try to get the wallpaper using another method
    cmd = [
        "gsettings",
        "get",
        "org.gnome.desktop.background",
        "picture-uri"
    ]
    try:
        output = subprocess.check_output(cmd, text=True)
        print("Wallpaper URI:", output.strip())
        
        wallpaper_path = output.strip().replace("file://", "")
        wallpaper_path = wallpaper_path.replace("'", "")
        copiedFile =shutil.copy2(wallpaper_path, THEME_FOLDER)
        dest_path = os.path.join(THEME_FOLDER, "wallpaper.png")
        
        os.rename(copiedFile, dest_path)
        print(f"Copied wallpaper to {dest_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error copying current wallpaper {e}")
        exit(1)

def create_own_theme_file():
    print("Creating own theme...")
    open (OWN_THEME_FILE, "w").close()
    try:
        with open(OWN_THEME_FILE, "w") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write("<gresources>\n")
            f.write('  <gresource prefix="/org/gnome/shell/theme">\n')
            f.write('    <file>calendar-today.svg</file>\n')
            f.write('    <file>calendar-today-light.svg</file>\n')
            f.write('    <file>gnome-shell-dark.css</file>\n')
            f.write('    <file>gnome-shell-light.css</file>\n')
            f.write('    <file>gnome-shell-high-contrast.css</file>\n')
            f.write('    <file>gnome-shell-start.svg</file>\n')
            f.write('    <file>pad-osd.css</file>\n')
            f.write('    <file>process-working-dark.svg</file>\n')
            f.write('    <file>process-working-light.svg</file>\n')
            f.write('    <file>workspace-placeholder.svg</file>\n')
            f.write('    <file>wallpaper.png</file>\n')
            f.write('  </gresource>\n')
            f.write("</gresources>\n")
            
        print(f"Created {OWN_THEME_FILE}")
    except Exception as e:
        print(f"Error creating own theme file: {e}")
        exit(1)


def main():
   extract_gdm_theme()
   copy_current_wallpaper_to_theme_folder()
   create_own_theme_file()


if __name__ == "__main__":
    main()
