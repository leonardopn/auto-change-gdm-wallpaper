import subprocess
import os

TEMP_DIR = os.path.join(os.path.dirname(__file__), "../temp")

def extract_gdm_theme():
    print("Extracting GDM theme...")
    cmd = [
        "bash",
        os.path.join(os.path.dirname(__file__), "../scripts/extract_gst.sh"),
        TEMP_DIR,
    ]
    try:
        subprocess.check_output(cmd, text=True)
        print("GDM theme extracted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error extracting GDM theme: {e}")
        exit(1)
        


def main():
   extract_gdm_theme()


if __name__ == "__main__":
    main()
