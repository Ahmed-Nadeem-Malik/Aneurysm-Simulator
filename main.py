import sys
import os
from PyQt5 import QtWidgets, QtCore
import pyvista as pv
from pyvistaqt import QtInteractor


#Initilise path and what files the user wants
basepath = "/Users/ahmed/Projects/Aneurysm_Model/models/"
file_chosen = "SNF00000227"


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aneurysm Model Visualization")


        # Create a central widget with a horizontal layout
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QHBoxLayout()
        central_widget.setLayout(layout)
        

        # Create the PyVista render window widget 2/3 of the window
        self.render_widget = QtInteractor(self)
        layout.addWidget(self.render_widget.interactor, stretch=2)
        

        # Create a separate widget for the sliders 1/3 of the window
        self.slider_panel = QtWidgets.QWidget()
        slider_layout = QtWidgets.QVBoxLayout()
        self.slider_panel.setLayout(slider_layout)
        layout.addWidget(self.slider_panel, stretch=1)
        

        # Checks whether the file exists and valid
        try:
            self.affected_segment_mesh = self.load_mesh(f"{basepath}aneurysms/remeshed/area-005/{file_chosen}_cut1.vtp")
            self.vessel_mesh = self.load_mesh(f"{basepath}vessels/remeshed/area-005/{file_chosen}.vtp")
            self.aneurysm_mesh = self.load_mesh(f"{basepath}aneurysms/remeshed/area-005/{file_chosen}_ninja.vtp")
        except FileNotFoundError as e:
            print(f"\n[ERROR] {e}\n")  
            sys.exit(1)


        # Add the meshes to the render window and capture actor references (actor is just a fancy word for mesh when using VTK)
        self.affected_segment_actor = self.render_widget.add_mesh(self.affected_segment_mesh, color="red", opacity=0.5)
        self.vessel_actor = self.render_widget.add_mesh(self.vessel_mesh, color="lightgrey", opacity=0.3)
        self.aneurysm_actor = self.render_widget.add_mesh(self.aneurysm_mesh, color="red", opacity=0.8)
        

        # Create sliders for each mesh
        self.create_slider(slider_layout, "Vessel Opacity", 0.3, lambda v: self.update_opacity(self.vessel_actor, v))
        self.create_slider(slider_layout, "Affected Segment Opacity", 0.5, lambda v: self.update_opacity(self.affected_segment_actor, v))
        self.create_slider(slider_layout, "Aneurysm Opacity", 0.8, lambda v: self.update_opacity(self.aneurysm_actor, v))
        

        #Pushes the sliders to the top of the window
        slider_layout.addStretch()



    #Code for checks / file validity
    def load_mesh(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Required file not found: {filepath}")
        try:
            return pv.read(filepath)
        except Exception as e:
            raise RuntimeError(f"Error loading mesh {filepath}: {e}")
        

    #Makes the sliders
    def create_slider(self, layout, title, initial, callback):
        label = QtWidgets.QLabel(title)
        slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setValue(int(initial * 100))
        slider.valueChanged.connect(lambda v: callback(v / 100.0))
        layout.addWidget(label)
        layout.addWidget(slider)


    #Updates the opacity of the segment that has changed
    def update_opacity(self, actor, value):
        actor.GetProperty().SetOpacity(value)
        self.render_widget.update()


#Runs the program
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())