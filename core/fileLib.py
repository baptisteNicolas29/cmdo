from typing import Union, Optional, Dict, List

import os
import subprocess
from pathlib import Path
from collections import namedtuple

# from Qt import QtWidgets as qtw

# from TatMayaLibrary import projectLib

from maya import cmds


# TODO: REFACTOR THE HELL OUT OF THIS MODULE
#
#
# class File(object):
#     char_file_ids = {
#         'task': 0,
#         'version': 1,
#         'comment': 2,
#         'owner': 3
#     }
#
#     # char_path_ids = {}
#     # char_path_ids = {}
#
#     @staticmethod
#     def are_you_sure(message: Optional[int] = None) -> bool:
#
#         """
#         Ask the user if they are sure they want to overwrite the file
#
#         Args:
#             message (int, optional):
#                 The message to display to the user
#                 Defaults to None
#
#         Returns:
#             bool:
#                 Whether the user is sure they want to overwrite the file
#         """
#
#         if message is None:
#             return True
#
#         messages = {
#             0: 'File already exists, are you sure you want to overwrite it?',
#             1: 'Current file contains unsaved modification.'
#                'Would you like to save it?'
#         }
#
#         confirm = mc.confirmDialog(
#             title='Confirm Save',
#             m=messages[message],
#             button=['Yes', 'No'], defaultButton='Yes',
#             cancelButton='No', dismissString='No'
#         )
#         return confirm == 'Yes'
#
#     def __init__(
#         self,
#         path: Optional[str] = None,
#         *args,
#         **kwargs
#     ) -> None:
#
#         """
#         Initialize a File object
#
#         Args:
#             path (str, optional):
#                 The path to the file
#
#         Returns:
#             None
#         """
#
#         self._init_file_properties(path)
#
#     def print_class(self) -> str:
#
#         """
#         Print les attributs de la classe Normalize.
#
#         Returns:
#             str:
#                 Les attributs de la classe Normalize.
#         """
#
#         txt = ""
#         txt += "\n# #########################################################"
#         txt += "\n# - FILE PROPERTIES        :"
#         txt += "\n# #########################################################"
#         txt += "\n"
#         txt += f"\n - path                    : {str(self.path)}"
#         txt += "\n"
#         txt += f"\n - folder_path             : {str(self.folder_path)}"
#         txt += f"\n - folder_name             : {self.folder_name}"
#         txt += "\n"
#         txt += f"\n - file_name               : {self.file_name}"
#         txt += f"\n - file_type               : {self.file_type}"
#         txt += f"\n - file_department         : {self.file_departement}"
#         txt += f"\n - file_owner              : {self.file_owner}"
#         txt += f"\n - asset                   : {self.asset}"
#         txt += f"\n - file_version            : {self.file_version}"
#         txt += f"\n - file_comment            : {self.file_comment}"
#         txt += "\n"
#         txt += f"\n - exists                  : {self.exists}"
#         txt += "\n"
#         txt += f"\n - template                : {self.template}"
#         txt += f"\n - info                    : {self.info}"
#         txt += "\n"
#         txt += f"\n - is_valid_path           : {self.is_valid_path}"
#         txt += "\n"
#
#         return txt
#
#     # PROPERTIES --------------------------------------------------------------
#     # -------------------------------------------------------------------------
#     @property
#     def path(self) -> Optional[Path]:
#
#         """
#         Renvoie le chemin du fichier.
#         Si aucun chemin n'a été spécifié, et qu'aucune sauvegarde n'a été
#         préalablement effectuée, renvoie None.
#
#         Return:
#             Optional[Path]:
#                 Le chemin du fichier.
#                 Ou None.
#         """
#
#         path = self._path if self._path else ''
#         path = str(path).replace(projectLib.DRIVE, projectLib.HARD_DRIVE)
#         return Path(path) if path else None
#
#     @path.setter
#     def path(self, path: Union[str, Path]) -> None:
#
#         """
#         Set the file path
#
#         Args:
#             path Union[str, Path]:
#                 The file path
#
#         Returns:
#             None
#         """
#
#         if isinstance(path, Path):
#             path = str(path)
#
#         path = path.replace(projectLib.DRIVE, projectLib.HARD_DRIVE)
#         self._path = Path(path) if path else ''
#
#     @property
#     def folder_path(self) -> Optional[Path]:
#
#         """
#         Renvoie le chemin du dossier contenant le fichier.
#         Si le chemin n'existe pas, renvoie None.
#
#         Returns:
#             Optional[str]:
#                 Le dossier du fichier.
#                 Ou None.
#         """
#
#         if self.path is None:
#             return None
#
#         return self.path.parent
#
#     @property
#     def folder_name(self) -> Optional[str]:
#
#         """
#         Renvoie le nom du dossier contenant le fichier.
#         Si le chemin n'existe pas, renvoie None.
#
#         Returns:
#             Optional[str]:
#                 Le nom du dossier.
#                 Ou None.
#         """
#
#         if self.folder_path is None:
#             return None
#
#         return self.folder_path.name
#
#     @property
#     def file_name(self) -> Optional[str]:
#
#         """
#         Renvoie le nom du fichier avec son extension.
#         Si le chemin n'existe pas, renvoie None.
#
#         Returns:
#             Optional[str]:
#                 Le nom du fichier.
#                 Ou None.
#         """
#
#         if self.path is None:
#             return None
#
#         return self.path.name
#
#     @property
#     def file_type(self) -> Optional[str]:
#
#         """
#         Renvoie l'extension du fichier.
#         Si le chemin n'existe pas, renvoie None.
#
#         Returns:
#             Optional[str]:
#                 Le type du fichier.
#                 Ou None.
#         """
#
#         if self.file_name is None or not self.is_valid_path:
#             return None
#
#         return self.path.suffix
#
#     @property
#     def file_owner(
#         self
#     ) -> Optional[str]:
#
#         """
#         Renvoie le propriétaire du fichier.
#         Si le chemin n'existe pas, renvoie None.
#
#         Returns:
#             Optional[str]:
#                 Le propriétaire du fichier.
#                 Ou None.
#         """
#
#         if self.file_name is None or not self.is_valid_path:
#             return None
#
#         suffix_id = self.char_file_ids.get('owner')
#         return self.path.suffixes[suffix_id].replace('.', '')
#
#     @property
#     def file_comment(
#         self
#     ) -> Optional[str]:
#
#         """
#         Renvoie le commentaire du fichier.
#         Si le chemin n'existe pas, renvoie None.
#
#         Returns:
#             Optional[str]:
#                 Le commentaire du fichier.
#                 Ou None.
#         """
#
#         if self.file_name is None or not self.is_valid_path:
#             return None
#
#         suffix_id = self.char_file_ids.get('comment')
#         return self.path.suffixes[suffix_id].strip('.[]')
#
#     @property
#     def file_version(
#         self
#     ) -> Optional[str]:
#
#         """
#         Renvoie la version du fichier.
#         Si le chemin n'existe pas, renvoie None.
#
#         Returns:
#             Optional[str]:
#                 La version du fichier.
#                 Ou None.
#         """
#
#         if self.file_name is None or not self.is_valid_path:
#             return None
#
#         suffix_id = self.char_file_ids.get('version')
#         return self.path.suffixes[suffix_id].replace('.', '')
#
#     @property
#     def file_departement(
#         self
#     ) -> Optional[str]:
#
#         """
#         Renvoie le département du fichier.
#         Si le chemin n'existe pas, renvoie None.
#
#         Returns:
#             Optional[str]:
#                 Le département du fichier.
#                 Ou None.
#         """
#
#         if self.file_name is None or not self.is_valid_path:
#             return None
#
#         suffix_id = self.char_file_ids.get('task')
#         return self.path.suffixes[suffix_id].replace('.', '')
#
#     @property
#     def work_state(
#         self
#     ) -> Optional[str]:
#
#         """
#         Renvoie l'état de travail du fichier.
#         Si le chemin n'existe pas, renvoie None.
#
#         Returns:
#             Optional[str]:
#                 L'état de travail du fichier.
#                 Ou None.
#         """
#
#         if self.file_name is None or not self.is_valid_path:
#             return None
#
#         return self.path.parts[5].split("_")[1]
#
#     @property
#     def asset(
#         self
#     ) -> Optional[str]:
#
#         """
#         Renvoie l'asset du fichier.
#         Si le chemin n'existe pas, renvoie None.
#
#         Returns:
#             Optional[str]:
#                 L'asset du fichier.
#                 Ou None.
#         """
#
#         if self.file_name is None or not self.is_valid_path:
#             return None
#
#         return self.file_name.split('.')[0]
#
#     @property
#     def asset_type(
#         self
#     ) -> Optional[str]:
#
#         """
#         Renvoie l'état de travail du fichier.
#         Si le chemin n'existe pas, renvoie None.
#
#         Returns:
#             Optional[str]:
#                 L'état de travail du fichier.
#                 Ou None.
#         """
#
#         if self.file_name is None or not self.is_valid_path:
#             return None
#
#         path = self.path
#
#         if len(path.parts) <= 2:
#             return self._asset_type
#
#         asset_type = path.parts[2].split("_")
#         if len(asset_type) > 1 and '06_ASSET' in path.parts:
#             return asset_type[1]
#
#         asset_type = path.parts[3].split("_")
#         if len(asset_type) > 1 and '08_PUBLISH' in path.parts:
#             return asset_type[1]
#
#         return self._asset_type
#
#     @asset_type.setter
#     def asset_type(
#         self,
#         asset_type: str
#     ) -> None:
#
#         """
#         Set the asset type
#
#         Args:
#             asset_type (str):
#                 The asset type
#
#         Returns:
#             None
#         """
#
#         self._asset_type = asset_type
#
#     @property
#     def exists(
#         self
#     ) -> bool:
#
#         """
#         Check if the file exists
#
#         Returns:
#             bool:
#                 Whether the file exists
#         """
#
#         if self.path is None:
#             return False
#
#         return self.path.is_file()
#
#     @property
#     def template(
#         self
#     ) -> Dict[Optional[str], Optional[str]]:
#
#         """
#         Renvoie le template du fichier.
#         Si le chemin n'existe pas, renvoie None.
#
#         Returns:
#             Dict[Optional[str], Optional[str]]:
#                 Le template du fichier.
#                 Ou None.
#         """
#         try:
#             template = projectLib.getTemplateAndInfoFromPath(str(self.path))[0]
#
#         except Exception as e:
#             print(e)
#             template = {}
#
#         return template
#
#     @property
#     def info(
#         self
#     ) -> Dict[Optional[str], Optional[str]]:
#
#         """
#         Renvoie les informations du fichier.
#         Si le chemin n'existe pas, renvoie None.
#
#         Returns:
#             Dict[Optional[str], Optional[str]]:
#                 Les informations du fichier.
#                 Ou None.
#         """
#         try:
#             info = projectLib.getTemplateAndInfoFromPath(str(self.path))[1]
#
#         except Exception as e:
#             print(e)
#             info = {}
#
#         return info
#
#     @property
#     def is_valid_path(
#         self
#     ) -> bool:
#
#         """
#         Check if the path is valid
#
#         Returns:
#             bool:
#                 Whether the path is valid
#         """
#
#         return bool(self.path and self.template and self.info)
#
#     # PUBLIC FUNCTIONS --------------------------------------------------------
#     # -------------------------------------------------------------------------
#     def import_file(
#         self,
#         namespace: Optional[str] = None,
#         **kwargs
#     ) -> None:
#
#         """
#         Import the file
#
#         Args:
#             namespace (str, optional):
#                 Namespace to import the file in
#
#         Returns:
#             None
#         """
#
#         if not self.exists:
#             raise FileExistsError(f'File does not exist: {str(self.path)}')
#
#         if namespace is not None:
#             mc.file(
#                 str(self.path),
#                 i=True,
#                 namespace=namespace,
#                 **kwargs
#             )
#
#         else:
#             mc.file(
#                 str(self.path),
#                 i=True,
#                 **kwargs
#             )
#
#     def open_file(
#         self,
#         force: bool = True,
#         modified: bool = False,
#         message: int = None,
#         **kwargs
#     ) -> bool:
#
#         """
#         Open the current file
#
#         Args:
#             force: force open, bypass change saving
#             modified: if True and the file is modified, save the file
#             message: message when saving file
#             **kwargs: key-word arguments for the file maya command
#
#         """
#
#         if not self.exists:
#             mc.warning(f'File does not exist: {str(self.path)}')
#             return False
#
#         if modified and mc.file(q=True, modified=True):
#             self.save_file(message)
#
#         mc.file(str(self.path), o=True, f=force, **kwargs)
#
#         return True
#
#     def save_file(
#             self,
#             message: int = None,
#             **kwargs
#     ) -> bool:
#
#         if self.exists and not self.are_you_sure(message):
#             mc.warning(f'File save aborted: {str(self.path)}')
#             return False
#
#         mc.file(rename=str(self.path))
#
#         mc.file(
#             type='mayaAscii',
#             save=True,
#             force=True,
#             options='v=1',
#             **kwargs
#         )
#
#         return True
#
#     def get_files_from_folder(
#         self,
#         folder_path: Optional[str] = None,
#         extension: Union[None, str] = None,
#         recursive: bool = False
#     ) -> Optional[List[str]]:
#
#         """
#         Recursively (or not) searches for files in the folder given
#
#         Args:
#             folder_path:
#                     the folder to search in
#
#             extension:
#                 the extension of the files to return or non to
#                 return all files
#
#             recursive:
#                 whether to recursively search in sub folders for files
#
#         Returns:
#             Optional[list[str]]:
#                 all the files found in the folder
#         """
#
#         folder_path = (
#             self.folder_path
#             if folder_path is None
#             else Path(folder_path)
#         )
#
#         if not folder_path:
#             return None
#
#         file_list = []
#
#         for full_path in folder_path.iterdir():
#
#             if full_path.is_file():
#                 if extension is None or extension == full_path.suffix:
#                     file_list.append(str(full_path))
#
#             elif full_path.is_dir() and recursive:
#                 file_list.extend(
#                     self.get_files_from_folder(
#                         full_path,
#                         extension=extension,
#                         recursive=recursive
#                     )
#                 )
#
#         return file_list
#
#     def file_stats(
#         self
#     ) -> namedtuple:
#
#         """
#         Return the file stats
#
#         Returns:
#             namedtuple
#                 ('Stat', 'date time directory size owner file_name')
#         """
#         if self.file_name is None or not self.is_valid_path:
#             return None
#
#         path = self.path
#
#         if path.is_file():
#             dir_name, file_name = path.parent, path.name
#         else:
#             dir_name, file_name = path.name, None
#
#         cmd = ["cmd", "/c", "dir", dir_name, "/q"]
#         session = subprocess.Popen(
#             cmd,
#             stdin=subprocess.PIPE,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE
#         )
#
#         result = session.communicate()[0].decode('cp1252')
#
#         if path.is_dir():
#             return File.convert_cat(result.splitlines()[5])
#
#         else:
#             for line in result.splitlines()[5:]:
#                 if file_name not in line:
#                     continue
#
#                 return File.convert_cat(line)
#
#             else:
#                 raise Exception('Could not locate file')
#
#     def set_asset(
#         self
#     ) -> None:
#
#         """
#         Set the asset from a dialog traversing the asset folders
#         based on the user's choice.
#
#         Returns:
#             None
#         """
#
#         asset, path = self._get_asset_from_user()
#         if asset is None or path is None:
#             mc.warning(f'Could not find related asset {asset} - {path}')
#             return
#
#         tri = os.environ.get('USERNAME').lower()
#         file_name = f'{asset}.setup.v000.[initScene].{tri}.ma'
#
#         self.path = Path(path).joinpath(
#             asset,
#             '02_setup',
#             ('01_body' if "PERSONNAGE" in path.name else '01_rig'),
#             file_name
#         )
#
#     def init_file(
#         self
#     ) -> None:
#
#         """
#         Initialize the asset
#
#         Returns:
#             None
#         """
#
#         self.set_asset()
#         folder_path = self.folder_path
#
#         if isinstance(folder_path, Path):
#             if not folder_path.exists():
#                 folder_path.mkdir(exist_ok=True)
#
#         mc.file(rename=str(self.path))
#         self._init_file_properties()
#
#     # STATIC FUNCTIONS --------------------------------------------------------
#     # -------------------------------------------------------------------------
#     @staticmethod
#     def convert_cat(
#         line: str
#     ) -> namedtuple:
#
#         """
#         Convert the output of the 'dir' command to a namedtuple
#
#         Args:
#             line (str):
#                 The line from the 'dir' command
#
#         Returns:
#             namedtuple:
#                 A namedtuple with the file properties
#         """
#
#         # Column Align Text indices from cmd
#         # Date time dir size owner file_name
#
#         FileProperties = namedtuple(
#             'FileProperties',
#             'date time directory size owner file_name'
#         )
#
#         stat_index = FileProperties(
#             date=(0, 11),
#             time=(11, 18),
#             directory=(18, 27),
#             size=(27, 35),
#             owner=(35, 59),
#             file_name=(59, -1)
#         )
#
#         file_properties = FileProperties(
#             date=File.slice_line(line, stat_index.date),
#             time=File.slice_line(line, stat_index.time),
#             directory=File.slice_line(line, stat_index.directory),
#             size=File.slice_line(line, stat_index.size),
#             owner=File.slice_line(line, stat_index.owner),
#             file_name=File.slice_line(line, stat_index.file_name)
#         )
#
#         return file_properties
#
#     @staticmethod
#     def slice_line(
#         iterable: str,
#         tup: tuple[int, int]
#     ) -> str:
#
#         """
#         Slice a string
#
#         Args:
#             iterable (str):
#                 The string to slice
#
#             tup (tuple[int, int]):
#                 The indices to slice the string with
#
#         Returns:
#             str:
#                 The sliced string
#         """
#
#         return iterable[tup[0]:tup[1]].strip()
#
#     # PRIVATE FUNCTIONS -------------------------------------------------------
#     # -------------------------------------------------------------------------
#     def _init_file_properties(
#         self,
#         path: Optional[Path | str] = None,
#     ) -> None:
#
#         """
#         Initialise le chemin de la scène.
#
#         Args:
#             path (str, optional):
#                 Chemin de la scène.
#                 Defaults to None.
#
#         Returns:
#             None
#         """
#         if path is None and (file_path := mc.file(q=True, sn=True)):
#             self._path = Path(file_path)
#
#         elif path is not None:
#             self._path = Path(path)
#
#         else:
#             self._path = None
#
#         path = self.path
#         if path is None:
#             self._asset_type = None
#             return
#
#         if not self.is_valid_path:
#             self._asset_type = None
#             return
#
#         split_path = path.parts
#         if len(split_path) <= 2 or len(split_path[2].split("_")) <= 1:
#             self._asset_type = None
#             return
#
#         self._asset_type = split_path[2].split('_')[1]
#
#     @staticmethod
#     def _get_asset_from_user() -> tuple:
#
#         """
#         Get the asset from the user
#
#         Returns:
#             None
#         """
#
#         qtw.QApplication.instance() or qtw.QApplication([])
#
#         dialog = AssetTypeSelectionDialog()
#
#         if dialog.exec_() == qtw.QDialog.Accepted:
#             return dialog.selected_asset, Path(dialog.asset_dir)
#
#         return None, None
#
#
# class AssetTypeSelectionDialog(qtw.QDialog):
#     def __init__(self, parent=None) -> None:
#
#         """
#         Initialize the class
#         It is a dialog to select the asset type
#
#         Args:
#             parent (Optional[QWidget], optional):
#                 The parent widget
#                 Defaults to None
#         """
#
#         super().__init__(parent)
#
#         self.setWindowTitle("Sélectionnez un Asset")
#         self.setLayout(qtw.QVBoxLayout())
#
#         self.selected_asset = None
#
#         self.type_label = qtw.QLabel("Quel type d'asset voulez-vous choisir?")
#         self.layout().addWidget(self.type_label)
#
#         self.character_button = qtw.QPushButton("Character")
#         self.character_button.clicked.connect(
#             lambda: self.list_assets("character")
#         )
#         self.layout().addWidget(self.character_button)
#
#         self.props_button = qtw.QPushButton("Props")
#         self.props_button.clicked.connect(
#             lambda: self.list_assets("props")
#         )
#         self.layout().addWidget(self.props_button)
#
#         # Barre de recherche
#         self.search_bar = qtw.QLineEdit()
#         self.search_bar.setPlaceholderText("Rechercher un asset...")
#         self.search_bar.textChanged.connect(self.filter_assets)
#         self.layout().addWidget(self.search_bar)
#
#         # Liste des assets
#         self.asset_list = qtw.QListWidget()
#         self.layout().addWidget(self.asset_list)
#
#         # Boutons OK / Annuler
#         self.button_box = qtw.QDialogButtonBox(
#             qtw.QDialogButtonBox.Ok | qtw.QDialogButtonBox.Cancel
#         )
#         self.button_box.accepted.connect(self.accept_selection)
#         self.button_box.rejected.connect(self.reject)
#         self.layout().addWidget(self.button_box)
#
#         # Répertoires
#         self.dirs = {
#             "character": Path(r"P:\06_ASSET\01_PERSONNAGE"),
#             "props": Path(r"P:\06_ASSET\02_ACCESSOIRE")
#         }
#         self.all_assets = []
#
#     def list_assets(self, asset_type: str) -> None:
#
#         """
#         Asset lister.
#
#         Args:
#             asset_type (str):
#                 The type of asset to list
#         """
#
#         self.search_bar.clear()
#         self.asset_list.clear()
#         asset_dir = self.dirs.get(asset_type)
#
#         if not asset_dir.exists():
#             qtw.QMessageBox.warning(
#                 self,
#                 "Erreur",
#                 f"Le dossier {asset_dir} n'existe pas."
#             )
#             return
#
#         self.all_assets = [
#             file
#             for file in asset_dir.iterdir()
#             if asset_dir.joinpath(file).is_dir()
#         ]
#
#         if self.all_assets:
#             self.asset_list.addItems(self.all_assets)
#         else:
#             self.asset_list.addItem("(Aucun asset trouvé)")
#
#         self.asset_dir = asset_dir
#
#     def filter_assets(self, search_text: str) -> None:
#
#         """
#         Filter the assets
#
#         Args:
#             search_text (str):
#                 The text to search for
#         """
#
#         self.asset_list.clear()
#
#         if not search_text:
#             # Si le champ est vide, afficher tous les assets
#             self.asset_list.addItems([asset.name for asset in self.all_assets])
#             return
#
#         # Filtrer les assets contenant le texte saisi
#         filtered_assets = [
#             asset.name
#             for asset in self.all_assets
#             if search_text.lower() in asset.name.lower()
#         ]
#
#         if filtered_assets:
#             self.asset_list.addItems(filtered_assets)
#         else:
#             self.asset_list.addItem("(Aucun asset trouvé)")
#
#     def accept_selection(self) -> None:
#
#         """
#         Accept the selection
#         """
#
#         selected_items = self.asset_list.selectedItems()
#
#         if selected_items:
#             self.selected_asset = selected_items[0].text()
#             self.accept()
#
#         else:
#             qtw.QMessageBox.warning(
#                 self,
#                 "Avertissement",
#                 "Veuillez sélectionner un asset avant de valider."
#             )
