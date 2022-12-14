# Modification by VidhosticeSDK

Same as below, but the OBJx import is here: `File --> Import --> Wavefront with 4xUV,VC,Mat (.objx)`

```
# Wavefront OBJx file (extension: 4xUV, VertexColor, multiple Materials)
# Creator: I3DShapesTool by Donkie (edited by VidhosticeSDK)
# Name: untitled
# Scale: 1.00

g default

v 1.000000 1.000000 1.000000 1.000000 1.000000 1.000000           <- Vertex Color
v -1.000000 1.000000 1.000000 1.000000 1.000000 1.000000
...
...
vt 0.625000 0.750000            <- UV1
vt 0.625000 1.000000
...
...
vt2 0.333333 0.333333           <- UV2
vt2 0.000000 0.333333
...
...
vt3 1.000000 0.000000           <- UV3
vt3 1.000000 1.000000
...
...
vt4 0.319734 0.619069           <- UV4
vt4 0.093471 0.848276
...
...
vn 0.000000 0.000000 1.000000
vn 0.000000 0.000000 1.000000
...
...
s off
g Cube
usemtl 1                       <- Material 1
f 1/1/1 2/2/2 3/3/3
f 4/4/4 5/5/5 6/6/6
f 1/1/1 3/3/3 7/7/7
usemtl 2                       <- Material 2
f 8/8/8 9/9/9 10/10/10
f 8/8/8 10/10/10 11/11/11
```

<br/>

># Blender Addon for Wavefront OBJ with Vertex Color
>
>Blender Addon to import/export Wavefront OBJ with Vertex Color. This addon is based on [the official blender addon](https://github.com/blender/blender-addons).
>
>So far the testing is not really sufficient. If you have any troubles importing / exporting your .obj data, please report an issue.
>
>## Installation
>
>1. Download zip of this repository.
>2. Open your blender 2.8
>3. Navigate to `Preferences --> Add-ons`
>4. Press `Install` and select the downloaded zip
>5. Enable the addon
>6. Done. You can import Wavefront OBJ with vertex color from `File --> Import --> Wavefront with VC (.obj)`, or export it in the same way.
