# Unity Blender Animation Fix

A standalone Python tool that fixes Unity's Blender importer bug where only the first animation action is imported from .blend files.

## The Problem

Unity has a long-standing bug in its Blender integration where the internal `Unity-BlenderToFBX.py` script uses `bake_anim_use_all_actions=False`, causing only the first animation action to be imported when you drag a `.blend` file into Unity. This means multi-animation Blender files lose most of their animations during import.

## The Solution

This tool automatically locates all Unity installations on your system and patches the problematic script to use `bake_anim_use_all_actions=True`, ensuring all animation actions are imported from Blender files.

## Features

- **Automatic Unity Detection**: Finds all Unity versions installed via Unity Hub
- **Safe Patching**: Creates backup files before making any changes
- **Permission Handling**: Automatically requests administrator privileges when needed
- **Cross-Version Support**: Works with all Unity versions that use the Blender importer
- **Detailed Reporting**: Shows exactly which installations were patched successfully

## Installation

1. Download `unity_blender_fix.py`
2. Ensure Python 3.x is installed on your system

## Usage

1. Close Unity and Unity Hub completely
2. Run the script:
   ```bash
   python unity_blender_fix.py
   ```
   Or simply double-click the `.py` file
3. Grant administrator privileges when prompted
4. The script will automatically find and patch all Unity installations
5. Restart Unity - your Blender files will now import all animations

## Requirements

- Python 3.x
- Windows (Unity Hub installation)
- Administrator privileges (script will request automatically)

## What Gets Changed

The script modifies `Unity-BlenderToFBX.py` in each Unity installation:

```python
# Before (broken)
bake_anim_use_all_actions=False

# After (fixed) 
bake_anim_use_all_actions=True
```

**File locations:**
```
C:\Program Files\Unity\Hub\Editor\{VERSION}\Editor\Data\Tools\Unity-BlenderToFBX.py
```

## Safety

- Original files are backed up as `.backup` before modification
- No Unity installation files are deleted or corrupted
- Changes can be reverted by restoring backup files

## Example Output

```
Unity Blender Animation Fix Tool
Fixes bake_anim_use_all_actions=False bug in Unity's Blender importer
------------------------------------------------------------

Found 3 Unity installation(s):
  2022.3.15f1: C:\Program Files\Unity\Hub\Editor\2022.3.15f1
  2023.2.8f1: C:\Program Files\Unity\Hub\Editor\2023.2.8f1
  2024.1.0f1: C:\Program Files\Unity\Hub\Editor\2024.1.0f1

Processing Unity 2022.3.15f1...
  Backup created: Unity-BlenderToFBX.py.backup
  Successfully patched!

Processing Unity 2023.2.8f1...
  Already patched or different format

Processing Unity 2024.1.0f1...
  Backup created: Unity-BlenderToFBX.py.backup
  Successfully patched!

==================================================
RESULTS SUMMARY
==================================================
Successfully patched:  2
Already fixed:         1
Permission errors:     0
Other errors:          0

SUCCESS! 2 Unity installation(s) fixed.
Your Blender files will now export all animations to Unity.
```

## Troubleshooting

**Permission Errors:**
- Make sure Unity and Unity Hub are completely closed
- Run the script as Administrator
- Or run from an Administrator command prompt

**Script Not Finding Unity:**
- Ensure Unity is installed via Unity Hub
- Check if Unity is installed in a custom location (script checks common paths)

**Backup Failed:**
- The script will continue without backup if backup creation fails
- Original functionality is preserved even if patching fails

## Contributing

This tool addresses a fundamental workflow issue for game developers using Blender animations in Unity projects. Feel free to submit issues or improvements.

## License

MIT License - Feel free to use and modify as needed.
