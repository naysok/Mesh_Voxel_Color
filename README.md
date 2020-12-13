# Mesh Voxel Color  

ドット・バイ・ドットのボクセル入稿ができるフルカラー 3D Printing に向けて、メッシュを数理的に解くライブラリ。  

このライブラリで生成した連番画像から 3D 描画は、3D プリントデータへの変換ソフトではできるが、適当なソフトウェアでは難しい。これだと不便なので擬似的にレンダリングを行うライブラリを書いた。  


### Project Result  

```
_prj_
    └── PRJECT_NAME
        ├── image_0
        │     // Contour Lines
        ├── image_1
        │     // Filled Contour Lines
```


### Related Projects  

- Contour_Draw_3D  
  - 3D ジオメトリを輪切りして切り出した断面の連番画像から、擬似的に 3D ジオメトリを描画するライブラリ  
  [https://github.com/naysok/Contour_Draw_3D](https://github.com/naysok/Contour_Draw_3D)  

- Mesh_Contour  
  - Ray-Triangle Intersection を用いて、メッシュの輪切りの線を計算するライブラリ。 
  [https://github.com/naysok/Mesh_Contour](https://github.com/naysok/Mesh_Contour)  

- GH_Renderer  
  - リストで出力される計算結果を Grasshopper に出力するライブラリ。
  - Grasshopper をインターフェースにコーディングするときは計算結果をこれで描画。  
  [https://github.com/naysok/GH_Renderer](https://github.com/naysok/GH_Renderer)  


### Ref  

- レイと三角形の交差判定（Pheemaの学習帳）  
  [https://pheema.hatenablog.jp/entry/ray-triangle-intersection](https://pheema.hatenablog.jp/entry/ray-triangle-intersection)  

- Möller–Trumbore intersection algorithm（Wikipedia）  
  [https://en.wikipedia.org/wiki/M%C3%B6ller%E2%80%93Trumbore_intersection_algorithm](https://en.wikipedia.org/wiki/M%C3%B6ller%E2%80%93Trumbore_intersection_algorithm)  

- Pythonの計算機イプシロン（Qiita）  
  [https://qiita.com/ikuzak/items/1332625192daab208e22](https://qiita.com/ikuzak/items/1332625192daab208e22)  

- Contours Hierarchy (opencv-python-tutroals)  
  [https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_contours/py_contours_hierarchy/py_contours_hierarchy.html#contours-hierarchy](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_contours/py_contours_hierarchy/py_contours_hierarchy.html#contours-hierarchy)  

- STLファイルフォーマット  
  [https://www.hiramine.com/programming/3dmodelfileformat/stlfileformat.html](https://www.hiramine.com/programming/3dmodelfileformat/stlfileformat.html)

- Stanford Bunny（thingiverse）  
  [https://www.thingiverse.com/thing:3731](https://www.thingiverse.com/thing:3731)  

- 3DBenchy - The jolly 3D printing torture-test by CreativeTools.se (Thingiverse)  
  [https://www.thingiverse.com/thing:763622](https://www.thingiverse.com/thing:763622)  

- Guide to Voxel Printing（GrabCAD）  
  [https://help.grabcad.com/article/230-guide-to-voxel-printing?locale=en&fbclid=IwAR3PvdP71KfqY1herjNa87oGvXnszbsXIcaNfOUYNfbDLn_kIZydNeyYXes](https://help.grabcad.com/article/230-guide-to-voxel-printing?locale=en&fbclid=IwAR3PvdP71KfqY1herjNa87oGvXnszbsXIcaNfOUYNfbDLn_kIZydNeyYXes)  

  - Vectorized way of calculating row-wise dot product two matrices with Scipy（Stackoverrun）  
  [https://stackoverrun.com/ja/q/4238423](https://stackoverrun.com/ja/q/4238423)  