import os
import json
import tkinter as tk
import subprocess
import shutil
from tkinter import filedialog

fighter_names = {
    'mario': 'Mario',
    'donkey': 'Donkey Kong',
    'link': 'Link',
    'samus': 'Samus',
    'samusd': 'Dark Samus',
    'yoshi': 'Yoshi',
    'kirby': 'Kirby',
    'fox': 'Fox',
    'pikachu': 'Pikachu',
    'luigi': 'Luigi',
    'ness': 'Ness',
    'captain': 'Captain Falcon',
    'purin': 'Jigglypuff',
    'peach': 'Peach',
    'daisy': 'Daisy',
    'koopa': 'Bowser',
    'koopag': 'Giga Bowser',
    'nana': 'Ice Climbers',
    'popo': 'Ice Climbers',
    'ice': 'Ice Climbers',
    'sheik': 'Sheik',
    'zelda': 'Zelda',
    'mariod': 'Dr. Mario',
    'pichu': 'Pichu',
    'falco': 'Falco',
    'marth': 'Marth',
    'lucina': 'Lucina',
    'younglink': 'Young Link',
    'ganon': 'Ganondorf',
    'mewtwo': 'Mewtwo',
    'roy': 'Roy',
    'chrom': 'Chrom',
    'gamewatch': 'Mr. Game & Watch',
    'metaknight': 'Meta Knight',
    'pit': 'Pit',
    'pitb': 'Dark Pit',
    'szerosuit': 'Zero Suit Samus',
    'wario': 'Wario',
    'snake': 'Snake',
    'ike': 'Ike',
    'ptrainer': 'Pokémon Trainer',
    'pzenigame': 'Squitle',
    'pfushigisou': 'Ivysaur',
    'plizardon': 'Charizard',
    'diddy': 'Diddy Kong',
    'lucas': 'Lucas',
    'sonic': 'Sonic',
    'dedede': 'King Dedede',
    'pikmin': 'Olimar',
    'lucario': 'Lucario',
    'robot': 'R.O.B.',
    'toonlink': 'Toon Link',
    'wolf': 'Wolf',
    'murabito': 'Villager',
    'rockman': 'Mega Man',
    'wiifit': 'Wii Fit Trainer',
    'rosetta': 'RosaLina & Luma',
    'littlemac': 'Little Mac',
    'gekkouga': 'Greninja',
    'miifighter': 'Mii Brawler',
    'miiswordsman': 'Mii Swordfighter',
    'miigunner': 'Mii Gunner',
    'palutena': 'Palutena',
    'pacman': 'Pac-man',
    'reflet': 'Robin',
    'shulk': 'Shulk',
    'koopajr': 'Bowser JR.',
    'duckhunt': 'Duck Hunt',
    'ryu': 'Ryu',
    'ken': 'Ken',
    'cloud': 'Cloud',
    'kamui': 'Corrin',
    'bayonetta': 'Bayonetta',
    'inkling': 'Inkling',
    'ridley': 'Ridley',
    'simon': 'Simon',
    'richter': 'Richter',
    'krool': 'King K. Rool',
    'shizue': 'Isabelle',
    'gaogaen': 'Incineroar',
    'packun': 'Piranha Plant',
    'jack': 'Joker',
    'brave': 'Hero',
    'buddy': 'Banjo & Kazooie',
    'dolly': 'Terry',
    'master': 'Byleth',
    'tantan': 'Min Min',
    'pickel': 'Steve',
    'edge': 'Sephiroth',
    'eflame': 'Pyra',
    'element': 'Rex',
    'elight': 'Mythra',
    'demon': 'Kazuya',
    'trail': 'Sora'
}


def export_as_files(base_directory, output_directory, include_jsons_var, keep_paths):
    paths = {}
    # Loops through Modpack
    for root, dirs, files in os.walk(base_directory):
        for file_name in files:
            # Get the full path of the file
            file_path = str(os.path.join(root, file_name).replace("\\", "/"))
            mod_name = file_path.split("/mods/")[1].split("/")[0]
            normalized_path = file_path.split(f"{mod_name}/")[1]
            if any(normalized_path.startswith(i) for i in keep_paths):
                # Add the path to the corresponding mod name in the dictionary
                if mod_name not in paths:
                    paths[mod_name] = []
                paths[mod_name].append(normalized_path)

                if "chara/chara_1/chara_1_" in normalized_path and "bntx" in normalized_path:
                    char_name = normalized_path.split("chara/chara_1/chara_1_")[1].split("_")[0]
                    skin_pos = "C" + normalized_path.split(f"_{char_name}_")[1].split(".")[0].replace("first_",
                                                                                                      "").replace(
                        "only_", "")

                    fighter = fighter_names[char_name]
                    os.makedirs(f"{output_directory}/{fighter}", exist_ok=True)
                    cmd = f"ultimate_tex_cli.exe \"{file_path}\" \"{output_directory}/{fighter}/{skin_pos}__{mod_name}.png\""
                    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

                    # Check the result
                    if result.returncode != 0:
                        return

                    if include_jsons_var:
                        json_file_path = "mod_paths.json"
                        with open(json_file_path, "w") as json_file:
                            json.dump(paths, json_file, indent=4)


def main(entry_base_directory, status_label, include_jsons_var):
    # Checks directory to determine whether we can proceed
    base_directory = entry_base_directory.get()
    if not os.path.exists(base_directory):
        status_label.config(text="Invalid directory path.", fg="red")
        return

    keep_paths = ["fighter", "ui", "effect", "sound", "config.json", "stream", "stage", "info.toml", "preview.webp"]

    current_directory = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
    output_directory = f"{current_directory}/output"

    # If it exists, remove the entire directory and its contents
    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)
    os.makedirs(output_directory, exist_ok=True)

    # Export data as files and folders
    export_as_files(base_directory, output_directory, include_jsons_var, keep_paths)
    status_label.config(text=f"Done!!!", fg="green")


# Create the main window
root = tk.Tk()
root.title("Modpack Image Dictionary Creator")

# Create and place widgets using grid
label_base_directory = tk.Label(root, text="Select the modpack/mod directory:")
label_base_directory.grid(row=0, column=0, pady=10)

entry_base_directory = tk.Entry(root, width=30)
entry_base_directory.grid(row=0, column=1)

browse_button = tk.Button(root, text="Browse",
                          command=lambda: entry_base_directory.insert(tk.END, filedialog.askdirectory()))
browse_button.grid(row=0, column=2)

status_label = tk.Label(root, text="", fg="black")
status_label.grid(row=2, column=0, columnspan=3)

# Checkbox to select export format
include_jsons_var = tk.BooleanVar()
include_jsons_checkbox = tk.Checkbutton(root, text="Include Modpack Json", variable=include_jsons_var)
include_jsons_checkbox.grid(row=1, column=0, columnspan=2)

ok_button = tk.Button(root, text="OK", command=lambda: main(entry_base_directory, status_label,
                                                            include_jsons_var.get()))
ok_button.grid(row=3, column=0, columnspan=4, pady=10)

root.mainloop()
