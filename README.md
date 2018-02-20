MitsubaForMaya
=

A [Maya](http://www.autodesk.com/products/maya) plugin for the [Mitsuba](http://www.mitsuba-renderer.org/) rendering engine.


Supported Features
-
Mitsuba 0.5.0 is the currently supported version.

Supported Mitsuba Features:

**BSDFs / Materials**: Diffuse, Rough Diffuse, Smooth Dielectric, Thin Dielectric, Rough Dielectric, Smooth Conductor, Rough Conductor, Smooth Plastic, Rough Plastic, Smooth Coating, Rough Coating, Bump Map, Phong, Ward, Mixture, Blend, Mask, Two Sided, Diffuse Transmitter, Hanrahan-Krueger, Irawan-Marschner Woven Cloth, Dipole SSS + Rough Plastic.

**Emitters / Lights**: Point, Spot, Directional, Object Area Light, Sun Sky, Envmap (IBL)

**Volume Scattering Models**: Homogeneous, Heterogeneous

**Phase Functions**: Isotropic, Henyey-Greenstein, Rayleigh, Kajiya-Kay, Micro-flake

**Sensors**: Perspective, Orthographic, Perspective with Thin Lens, Spherical, Telecentric, Radiance Meter, Fluence Meter, Perspective with Radial Distortion.

**Integrators** : Ambient Occlusion, Direct Illumination, Path Tracer, Simple Volumetric Path Tracer, Extended Volumetric Path Tracer, Bidirectional Path Tracer, Photon Map, Progressive Photon Mapping, Stochastic Progressive Photon Mapping, Primary Sample Space Metropolis Light Transport, Path Space Metropolis Light Transport, Energy Redistribution Path Tracing, Adjoint Particle Tracer, Adaptive, Irradiance Caching, Multi-Channel

**Sampler Generators** : Independent, Stratified, Low Discrepancy, Halton QMC, Hammersley QMC, Sobol QMC

**Films / Output Drivers** : HDR (exr/hdr/pfm), Tiled HDR (exr), LDR (jpg, png), Matlab / Mathematica / Numpy

Notes
-

For a variety of Mitsuba materials, volumes and lights, check the Hypershade under Maya/Surface, Maya/Volumetric and Maya/Lights.

Render settings have been set to balance render time vs. quality. The main thing that controls render quality is the sampleCount in the Image Sampler drop down.

The default lighting in Mitsuba is a sunsky, so if you do not set up any lighting, that is what this plugin will default to as well. For normal Maya lights, environment maps or the Sun+Sky model, see the appropriate nodes in the Hypershader under Maya/Lights. To use an area light, assign the MitsubaObjectAreaLightShader shader as the Material for the object that you would like to act as an area light.

To set up volumetric scattering, assign one of the Volumetric Scattering models to a Material's Shading Group's 'Volume Material' slot. Be sure to use either the Simple Volumetric Path Tracer or Extended Volumetric Path Tracer Integrator when rendering with Volume Scattering Models.

Usage
-

- Load from the download location using Python command
	- cmds.loadPlugin( "/path/where/you/downloaded/MitsubaForMaya.py" )

- Unload as appropriate
	- cmds.unloadPlugin( "MitsubaForMaya.py" )

- ***VERY IMPORTANT*** 
- The first field in the Render Settings Mituba tab is the path to the 'mitsuba' binary. You must set this to be able to render. The setting can be specified using the MITSUBA_PATH environment variable, as described below, or manually from the Render Settings UI. The path will be retained in a file's Render Settings so the value only has to be specified the first time you use a scene.

	- OSX: ex. /path/where/you/downloaded/Mitsuba.app/Contents/MacOS/mitsuba

	- Linux: ex. /usr/local/mitsuba/mitsuba

	- Windows: ex. C:/path/where/you/downloaded/Mitsuba 0.5.0 64bit/Mitsuba 0.5.0/mitsuba.exe

- The second field in the Render Settings Mituba tab is the path to the 'oiiotool' binary. You must set this to be able to use Maya's render region functionality. The setting can be specified using the OIIOTOOL_PATH environment variable, as described below, or manually from the Render Settings UI. The path will be retained in a file's Render Settings so the value only has to be specified the first time you use a scene.

- Currently, only Mitsuba Lights, Materials and Volumes are supported. These can be found and assigned using the Hypershade

Installation and Application Environment
- 
The path to the Mitsuba binary has to be specified, either in the Render Settings manually or by using the Maya.env or other environment setup file.

- To set the value in the Maya.env or in your shell environment, set the MITSUBA_PATH environment variable to  

	- Windows: MITSUBA_PATH = C:\path\to\Mitsuba 0.5.0\mitsuba.exe

	- Mac: MITSUBA_PATH = /path/to/Mitsuba.app/Contents/MacOS/mitsuba

	- Linux: MITSUBA_PATH = /path/to/mitsuba

In order to render in Batch mode, you'll need to set two additional environment variables

- MAYA_RENDER_DESC_PATH has to point to the folder containing the MitsubaRenderer.xml file.

- MAYA_PLUG_IN_PATH has to point to the MitsubaForMaya plug-ins folder

- Example Maya.env settings for Windows:

	- MAYA_RENDER_DESC_PATH = C:\path\to\MitsubaForMaya

	- MAYA_PLUG_IN_PATH = C:\path\to\MitsubaForMaya\plug-ins

***VERY IMPORTANT*** 
If your scene contains animation on the parameters of the Mitsuba lights, materials or volumes and you are using Maya 2016 or later, you will need to set the following environment variable

- MAYA_RELEASE_PYTHON_GIL = 1

- Without this setting, Maya will lock up.

- [Discussion on Python Programming for Autodesk Maya Google Group](https://groups.google.com/forum/?hl=en#!topic/python_inside_maya/Zk7FKPu7J_A)


In order for the Maya render region functionality to work, the path to the [OpenImageIO](https://github.com/OpenImageIO/oiio) 'oiiotool' binary has to be specified, either in the Render Settings manually or by using the Maya.env or other environment setup file.

- To set the value in the Maya.env or in your shell environment, set the OIIOTOOL_PATH environment variable to  

	- Windows: OIIOTOOL_PATH = C:\path\to\oiiotool.exe

	- Mac: OIIOTOOL_PATH = /path/to/oiiotool

	- Linux: OIIOTOOL_PATH = /path/to/oiiotool

- Resources for OpenImageIO include

	- [OpenImageIO github](https://github.com/OpenImageIO/oiio)

	- [Prebuilt Windows binaries](http://www.lfd.uci.edu/~gohlke/pythonlibs/#openimageio)

	- [Build instructions for Linux and OSX](https://github.com/OpenImageIO/oiio/blob/master/INSTALL)


Maya.env
-

Maya.env files can be saved in the following folders

- Windows: C:\Users\\*username*\\Documents\maya\<mayaVersion>

- Mac: /Users/*username*/Library/Preferences/Autodesk/maya/<mayaVersion>

- Linux: /home/*username*/maya/<mayaVersion>

*Autodesk Reference links*

- [Setting the Maya.env](http://help.autodesk.com/view/MAYAUL/2016/ENU/?guid=GUID-8EFB1AC1-ED7D-4099-9EEE-624097872C04)

- [Brief description of MAYA_RENDER_DESC_PATH](http://knowledge.autodesk.com/support/maya/learn-explore/caas/CloudHelp/cloudhelp/2016/ENU/Maya/files/GUID-AF8A7EA4-DEEF-49EF-A18C-CDA72B4F9E1E-htm.html)


Rendering in Batch
-
Rendering an animation in Batch mode works, with a couple of caveats

- Batch renders can't be canceled from the UI

References
-

- [Mitsuba](http://www.mitsuba-renderer.org/)

- [Mitsuba Downloads](http://www.mitsuba-renderer.org/download.html)

- [Mitsuba Blog](http://www.mitsuba-renderer.org/devblog/)

- [Mitsuba Respository](https://www.mitsuba-renderer.org/repos/)

- [OpenMaya renderer integrations](https://github.com/haggi/OpenMaya)

- [Irawan Cloth Data Sets](http://www.mitsuba-renderer.org/scenes/irawan.zip)

- [Source of test mesh geometry](http://graphics.cs.williams.edu/data/meshes.xml)

	- Material preview scene by Jonas Pilo


Testing
-

This plugin was tested with Maya 2016 on OSX Yosemite, Windows 7 and CentOS 7 Linux.

