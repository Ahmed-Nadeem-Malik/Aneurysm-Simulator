import sys
from PyQt5 import QtWidgets, QtCore
import pyvista as pv
from pyvistaqt import QtInteractor

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Aneurysm Model Visualization")
        # Create a central widget with a horizontal layout
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QHBoxLayout()
        central_widget.setLayout(layout)
        
        # Create the PyVista render window widget
        self.vtk_widget = QtInteractor(self)
        layout.addWidget(self.vtk_widget.interactor, stretch=2)
        
        # Create a separate widget for the sliders
        self.slider_panel = QtWidgets.QWidget()
        slider_layout = QtWidgets.QVBoxLayout()
        self.slider_panel.setLayout(slider_layout)
        layout.addWidget(self.slider_panel, stretch=1)
        
        # Load the meshes
        self.vessel_aneurysm = pv.read("/Users/ahmed/Projects/Aneurysm_Model/models/aneurysms/remeshed/area-001/ANSYS_UNIGE_16_cut1.vtp")
        self.centerline      = pv.read("/Users/ahmed/Projects/Aneurysm_Model/models/centerlines/ANSYS_UNIGE_16.vtp")
        self.full_vessel     = pv.read("/Users/ahmed/Projects/Aneurysm_Model/models/vessels/remeshed/area-001/ANSYS_UNIGE_16.vtp")
        self.ninja           = pv.read("/Users/ahmed/Projects/Aneurysm_Model/models/aneurysms/remeshed/area-001/ANSYS_UNIGE_16_ninja.vtp")
        
        # Add the meshes to the render window and capture actor references
        self.actor_aneurysm = self.vtk_widget.add_mesh(self.vessel_aneurysm, color="red", opacity=0.5)
        self.actor_vessel   = self.vtk_widget.add_mesh(self.full_vessel, color="lightgrey", opacity=0.3)
        self.actor_center   = self.vtk_widget.add_mesh(self.centerline, color="black", opacity=1.0)
        self.actor_ninja    = self.vtk_widget.add_mesh(self.ninja, color="red", opacity=0.8)
        
        # Create sliders for each mesh
        self.create_slider(slider_layout, "Affected Segment Opacity", 0.5, self.update_aneurysm_opacity)
        self.create_slider(slider_layout, "Vessel Opacity", 0.3, self.update_vessel_opacity)
        self.create_slider(slider_layout, "Centerline Opacity", 1.0, self.update_centerline_opacity)
        self.create_slider(slider_layout, "Aneurysm Opacity", 0.8, self.update_ninja_opacity)
        
        # Optionally, add a spacer to push sliders to the top
        slider_layout.addStretch()

    def create_slider(self, layout, title, initial, callback):
        label = QtWidgets.QLabel(title)
        slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setValue(int(initial * 100))
        slider.valueChanged.connect(lambda value: callback(value / 100.0))
        layout.addWidget(label)
        layout.addWidget(slider)

    def update_aneurysm_opacity(self, value):
        self.actor_aneurysm.GetProperty().SetOpacity(value)
        self.vtk_widget.update()

    def update_vessel_opacity(self, value):
        self.actor_vessel.GetProperty().SetOpacity(value)
        self.vtk_widget.update()

    def update_centerline_opacity(self, value):
        self.actor_center.GetProperty().SetOpacity(value)
        self.vtk_widget.update()

    def update_ninja_opacity(self, value):
        self.actor_ninja.GetProperty().SetOpacity(value)
        self.vtk_widget.update()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())