import os
from typing import Dict, List, Any
from tools.editing_tools import JSONEditor

CONFIG_FILE_PATH: str = 'config.json'
SETTINGS_FILE_PATH: str = 'settings.json'

def create_json_file(file_path: str, content: Dict[str, Any]) -> None:
    if not os.path.exists(file_path):
        JSONEditor.build_json_file(file_path=file_path, content=content)

def load_json_data(file_path: str) -> Dict[str, Any]:
    json_file: JSONEditor = JSONEditor(json_file_path=file_path)
    return json_file.get_json_data()

def main() -> None:
    paths: List[str] = [CONFIG_FILE_PATH, SETTINGS_FILE_PATH]
    for path in paths:
        try:
            os.remove(path=path)
        except FileNotFoundError:
            pass

    game_settings: Dict[str, Any] = {
        'window_width': 1920,
        'window_height': 1080,
        'game_title': 'Kalpak Game',
        'fps': 120,
        'icon_path': os.path.join('graphics','icon.ico')
    }

    config_data: Dict[str, str] = {'example':'checking'}

    create_json_file(CONFIG_FILE_PATH, config_data)
    create_json_file(SETTINGS_FILE_PATH, game_settings)

main()
config_contents: Dict[str, Any] = load_json_data(CONFIG_FILE_PATH)
settings_contents: Dict[str, Any] = load_json_data(SETTINGS_FILE_PATH)