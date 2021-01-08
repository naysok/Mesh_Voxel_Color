import sys
sys.path.append("_module_\\Mesh_Contour")

from mesh_contour import run_mesh_contour
mc = run_mesh_contour.RunMeshContour()


class SliceGeometry():


    def get_meshes_and_ranges(self, file_path):
        meshes, ranges = mc.set_mesh(file_path)
        return meshes, ranges


    def contour_meshes(self, meshes, ranges, height):
        meshes_filtered, lines = mc.run_contour(meshes, ranges, height)
        return lines
