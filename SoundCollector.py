import MapClasses
import ErrorTable

prefix = "[AUDIO_FETCH]"

def get_sound_files(level, soundFolder) -> List[str]:
    '''Get the required sound files used in level.'''
    unique_sounds = []
    sound_paths = []
    for entity in level.entities:

        if entity.keyPairs["classname"] != "env_sound":
            continue

        if entity.keyPairs["sound"] not in unique_sounds:
            if entity.keyPairs["sound"] == "":
                continue
            unique_sounds.append(entity.keyPairs["sound"])
            print(prefix, f"Unique sound file {entity.keyPairs["sound"]} listed")

    if len(unique_sounds) == 0:
        print(prefix, "No sound files needed.")
        return

    for sound in unique_sounds:
        soundPath = soundFolder / sound
        if not soundPath.exists():
            print(ErrorTable.e0, soundPath)
            continue
        sound_paths.append(soundPath)
        print(prefix, f"File {soundPath} retrieved")

    return sound_paths
    