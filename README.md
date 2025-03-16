# Aneurysm Model Visualization

This project is a PyQt5 application that visualizes aneurysm models using PyVista and PyVistaQt. To get the files visit https://zenodo.org/records/6678442 and download the file containing the vascular surface models in VTK format: models-v1.0.zip.

## Requirements

Make sure you have the required Python libraries installed:

```bash
pip install pyqt5 pyvista pyvistaqt
```

## Running the Application

Navigate to the directory containing the script and run:

```bash
python main.py
```

## File Structure

The script expects the following directory structure:

```
/Users/ahmed/Projects/Aneurysm_Model/models/
    ├── aneurysms/
    │   ├── remeshed/
    │   │   ├── area-005/
    │   │   │   ├── SNF00000227_cut1.vtp
    │   │   │   ├── SNF00000227_ninja.vtp
    ├── vessels/
    │   ├── remeshed/
    │   │   ├── area-005/
    │   │   │   ├── SNF00000227.vtp
```

Ensure that the specified files exist in the expected locations and change it for your case.

## Features

- Loads and visualizes three mesh files:
  - **Affected segment mesh** (red, 50% opacity)
  - **Vessel mesh** (light grey, 30% opacity)
  - **Aneurysm mesh** (red, 80% opacity)
- Provides sliders to adjust opacity in real-time.

## Error Handling

If a required file is missing, the script will output an error message and exit.

## UI Layout

- The visualization window occupies 2/3 of the main window.
- A panel on the right (1/3 of the window) contains opacity sliders.

## Controls

- Use the sliders to adjust opacity of different meshes.
- The UI updates in real-time when slider values change.

## License

This project is open-source. Modify and distribute freely.
