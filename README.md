CyclesForMaya
=

A [Maya](http://www.autodesk.com/products/maya) plugin for the Cycles rendering engine.


Usage
-

- Load from the download location using Python command
	- cmds.loadPlugin( "/path/where/you/downloaded/CyclesForMaya.py" )

- Unload as appropriate
	- cmds.unloadPlugin( "CyclesForMatya.py" )

- ***VERY IMPORTANT*** 
- The first field in the Render Settings Cycles tab is the path to the 'cycles' binary. You must set this to be able to render. The setting can be specified using the CYCLES_PATH environment variable, as described below, or manually from the Render Settings UI. The path will be retained in a file's Render Settings so the value only has to be specified the first time you use a scene.


Cycles renderer
-
The file "wip5.diff" is a patch against the cycles standalone renderer, as of 2018.3.23, and is necessary for CyclesForMaya.
