import inspect
import os
import sys
import time

import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

kPluginCmdName = "Mitsuba"

pluginDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.append(pluginDir)

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'util')))

from process import Process

# Import modules for settings, material, lights and volumes
import MitsubaRenderSettings

global renderSettings
renderSettings = None


#
# IO
#
import MitsubaRendererIO

#
# Utility functions
#
def registMaterialNodeType(materialNodeType):
    MitsubaRendererIO.materialNodeTypes.append(materialNodeType)

def createRenderSettingsNode():
    global renderSettings
    print( "\n\n\nMitsuba Render Settings - Create Node - Python\n\n\n" )

    existingSettings = cmds.ls(type='MitsubaRenderSettings')
    if existingSettings != []:
        # Just use the first one?
        renderSettings = existingSettings[0]
        print( "Using existing Mitsuba settings node : %s" % renderSettings)
    else:
        renderSettings = cmds.createNode('MitsubaRenderSettings', name='defaultMitsubaRenderGlobals', shared=True)
        print( "Creating new Mitsuba settings node : %s" % renderSettings)

def getRenderSettingsNode():
    global renderSettings
    return renderSettings

def updateRenderSettings():
    global renderSettings
    print( "\n\n\nMitsuba Render Settings - Update - Python\n\n\n" )

def getImageExtension(renderSettings):
    filmType = cmds.getAttr( "%s.film" % renderSettings )

    if filmType == 'HDR Film':
        fHDRFilmFileFormat = cmds.getAttr("%s.%s" % (renderSettings, "fHDRFilmFileFormat"))

        mayaFileFormatUINameToExtension = {
            "OpenEXR (.exr)"  : "exr",
            "RGBE (.hdr)" : "hdr",
            "Portable Float Map (.pfm)"  : "pfm"
        }

        if fHDRFilmFileFormat in mayaFileFormatUINameToExtension:
            fHDRFilmFileFormatExtension = mayaFileFormatUINameToExtension[fHDRFilmFileFormat]
        else:
            fHDRFilmFileFormatExtension = "exr"

        extension = fHDRFilmFileFormatExtension

    elif filmType == 'HDR Film - Tiled':
        extension = "exr"

    elif filmType == 'LDR Film':
        fLDRFilmFileFormat = cmds.getAttr("%s.%s" % (renderSettings, "fLDRFilmFileFormat"))

        mayaFileFormatUINameToExtension = {
            "PNG (.png)"  : "png",
            "JPEG (.jpg)" : "jpg"
        }

        if fLDRFilmFileFormat in mayaFileFormatUINameToExtension:
            fLDRFilmFileFormatExtension = mayaFileFormatUINameToExtension[fLDRFilmFileFormat]
        else:
            fLDRFilmFileFormatExtension = "png"

        extension = fLDRFilmFileFormatExtension

    elif filmType == 'Math Film':
        fMathFilmFileFormat = cmds.getAttr("%s.%s" % (renderSettings, "fMathFilmFileFormat"))

        mayaFileFormatUINameToExtension = {
            "Matlab (.m)"  : "m",
            "Mathematica (.m)" : "m",
            "NumPy (.npy)" : "npy"
        }

        if fMathFilmFileFormat in mayaFileFormatUINameToExtension:
            fMathFilmFileFormatExtension = mayaFileFormatUINameToExtension[fMathFilmFileFormat]
        else:
            fMathFilmFileFormatExtension = "m"

        extension = fMathFilmFileFormatExtension

    else:
        extension = "exr"

    return extension


#
# UI
#
import MitsubaRendererUI

#
# Renderer functions
#

# A command to render with Maya
class mitsubaForMaya(OpenMayaMPx.MPxCommand):
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)

    # Invoked when the command is run.
    def doIt(self,argList):
        global renderSettings
        print "Rendering with Mitsuba..."

        # Create a render settings node
        createRenderSettingsNode()

        #Save the user's selection
        userSelection = cmds.ls(sl=True)
        
        print( "Render Settings - Node            : %s" % renderSettings )

        #Get the directories and other variables
        projectDir = cmds.workspace(q=True, fn=True)
        renderDir = os.path.join(projectDir, "renderData")
        pluginDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        version = cmds.about(v=True).replace(" ", "-")

        # Get render settings
        mitsubaPath = cmds.getAttr("%s.%s" % (renderSettings, "mitsubaPath"))
        oiiotoolPath = cmds.getAttr("%s.%s" % (renderSettings, "oiiotoolPath"))
        mtsDir = os.path.split(mitsubaPath)[0]
        integrator = cmds.getAttr("%s.%s" % (renderSettings, "integrator"))
        sampler = cmds.getAttr("%s.%s" % (renderSettings, "sampler"))
        sampleCount = cmds.getAttr("%s.%s" % (renderSettings, "sampleCount"))
        reconstructionFilter = cmds.getAttr("%s.%s" % (renderSettings, "reconstructionFilter"))
        keepTempFiles = cmds.getAttr("%s.%s" % (renderSettings, "keepTempFiles"))
        verbose = cmds.getAttr("%s.%s" % (renderSettings, "verbose"))

        print( "Render Settings - Mitsuba Path     : %s" % mitsubaPath )
        print( "Render Settings - Integrator       : %s" % integrator )
        print( "Render Settings - Sampler          : %s" % sampler )
        print( "Render Settings - Sample Count     : %s" % sampleCount )
        print( "Render Settings - Reconstruction   : %s" % reconstructionFilter )
        print( "Render Settings - Keep Temp Files  : %s" % keepTempFiles )
        print( "Render Settings - Verbose          : %s" % verbose )
        print( "Render Settings - Render Dir       : %s" % renderDir )
        print( "Render Settings - oiiotool Path    : %s" % mitsubaPath )

        animation = self.isAnimation()
        print( "Render Settings - Animation        : %s" % animation )

        # Animation
        if animation:
            startFrame = int(cmds.getAttr("defaultRenderGlobals.startFrame"))
            endFrame = int(cmds.getAttr("defaultRenderGlobals.endFrame"))
            byFrame = int(cmds.getAttr("defaultRenderGlobals.byFrameStep"))
            print( "Animation frame range : %d to %d, step %d" % (
                startFrame, endFrame, byFrame) )

            for frame in range(startFrame, endFrame+1, byFrame):
                print( "Rendering frame " + str(frame) + " - begin" )

                self.exportAndRender(renderDir, renderSettings, mitsubaPath, oiiotoolPath,
                    mtsDir, keepTempFiles, animation, frame, verbose)

                print( "Rendering frame " + str(frame) + " - end" )

            print( "Animation finished" )

        # Single frame
        else:
            imageName = self.exportAndRender(renderDir, renderSettings, mitsubaPath, oiiotoolPath,
                mtsDir, keepTempFiles, animation, None, verbose)

            # Display the render
            if not cmds.about(batch=True):
                MitsubaRendererUI.showRender(imageName)

        # Select the objects that the user had selected before they rendered, or clear the selection
        if len(userSelection) > 0:
            cmds.select(userSelection)
        else:
            cmds.select(cl=True)

    def isAnimation(self):
        animation = cmds.getAttr("defaultRenderGlobals.animation")
        if not cmds.about(batch=True) and animation:
            print( "Animation isn't currently supported outside of Batch mode. Rendering current frame." )
            animation = False

        mayaReleasePythonGIL = os.environ.get('MAYA_RELEASE_PYTHON_GIL')
        mayaVersion = float(cmds.about(version=True))
        if mayaVersion >= 2016 and not mayaReleasePythonGIL:
            print( "\n\n\n\n")
            print( "For versions of Maya 2016 and greater, you must set the environment variable MAYA_RELEASE_PYTHON_GIL"
                " to 1 to render animations. Rendering current frame only." )
            print( "\n\n\n\n")
            animation = False

        return animation

    def resetImageDataWindow(self, imageName, oiiotoolPath):
        editor = cmds.renderWindowEditor(q=True, editorName=True )
        #print( "resetImageDataWindow - editor : %s" % editor )
        if editor:
            renderRegion = cmds.renderWindowEditor(editor, q=True, mq=True)
            #print( "resetImageDataWindow - render region : %s" % renderRegion )
            if renderRegion:
                left = cmds.getAttr( "defaultRenderGlobals.left" )
                right = cmds.getAttr( "defaultRenderGlobals.rght" )
                top = cmds.getAttr( "defaultRenderGlobals.top" )
                bottom = cmds.getAttr( "defaultRenderGlobals.bot" )
            
                imageWidth = cmds.getAttr("defaultResolution.width")
                imageHeight = cmds.getAttr("defaultResolution.height")

                pathTokens = os.path.splitext(imageName)
                imageNameCropped = "%s_crop%s" % (pathTokens[0], pathTokens[1])
                #print( "Generating cropped image : %s" % imageNameCropped )

                oiiotoolResult = None
                try:
                    #cmd = '/usr/local/bin/oiiotool'
                    cropArgs = '%dx%d-%d-%d' % (imageWidth, imageHeight, left, imageHeight-top)
                    args = ['-v', imageName, '--crop', cropArgs, '--noautocrop', '-o', imageNameCropped]
                    oiiotool = Process(description='reset image data window',
                        cmd=oiiotoolPath,
                        args=args)
                    oiiotool.execute()
                    oiiotoolResult = oiiotool.status
                    #print( "oiiotool result : %s" % oiiotoolResult )
                except:
                    print( "Unable to run oiiotool" )
                    oiiotoolResult = None

                # Move the image with the new data window over the original rendered image
                if oiiotoolResult in [0, None]:
                    os.rename(imageNameCropped, imageName)

    def getScenePrefix(self):
        return str('.'.join(os.path.split(cmds.file(q=True, sn=True))[-1].split('.')[:-1]))

    def renderScene(self,
                    outFileName, 
                    renderDir, 
                    mitsubaPath,
                    oiiotoolPath, 
                    mtsDir, 
                    keepTempFiles, 
                    geometryFiles, 
                    animation=False, 
                    frame=1, 
                    verbose=False,
                    renderSettings=None):
        imageDir = os.path.join(os.path.split(renderDir)[0], 'images')
        os.chdir(imageDir)

        sceneName = self.getScenePrefix()

        imagePrefix = cmds.getAttr("defaultRenderGlobals.imageFilePrefix")
        if imagePrefix is None:
            imagePrefix = sceneName

        writePartialResults = False
        writePartialResultsInterval = -1
        blockSize = 32
        threads = 0
        if renderSettings:
            extension = getImageExtension(renderSettings)

            writePartialResults = cmds.getAttr("%s.%s" % (renderSettings, "writePartialResults"))
            writePartialResultsInterval = cmds.getAttr("%s.%s" % (renderSettings, "writePartialResultsInterval"))
            blockSize = cmds.getAttr("%s.%s" % (renderSettings, "blockSize"))
            threads = cmds.getAttr("%s.%s" % (renderSettings, "threads"))

            print( "Render Settings - Partial Results  : %s" % writePartialResults )
            print( "Render Settings - Results Interval : %s" % writePartialResultsInterval )
            print( "Render Settings - Block Size       : %s" % blockSize )
            if threads:
                print( "Render Settings - Threads          : %s" % threads )

        if animation:
            extensionPadding = cmds.getAttr("defaultRenderGlobals.extensionPadding")
            logName = os.path.join(imageDir, imagePrefix + "." + str(frame).zfill(extensionPadding) +".log")
            imageName = os.path.join(imageDir, imagePrefix + "." + str(frame).zfill(extensionPadding) + "." + extension)
        else:
            logName = os.path.join(imageDir, imagePrefix + ".log")
            imageName = os.path.join(imageDir, imagePrefix + "." + extension)

        args = []
        if verbose:
            args.append('-v')
        if writePartialResults:
            args.extend(['-r', str(writePartialResultsInterval)])
        if threads:
            args.extend(['-p', str(threads)])
        args.extend([
            '-b', str(blockSize), 
            '-o',
            imageName,
            outFileName])

        if ' ' in mtsDir:
            env = {"LD_LIBRARY_PATH":str("\"%s\"" % mtsDir)}
        else:
            env = {"LD_LIBRARY_PATH":str(mtsDir)}

        mitsubaRender = Process(description='render an image',
            cmd=mitsubaPath,
            args=args,
            env=env)

        def renderLogCallback(line):
            if "Writing image" in line:
                imageName = line.split("\"")[-2]

                # Display the render
                if not cmds.about(batch=True):
                    MitsubaRendererUI.showRender(imageName)

        mitsubaRender.log_callback = renderLogCallback
        #mitsubaRender.echo = False

        mitsubaRender.execute()
        mitsubaRender.write_log_to_disk(logName, format='txt')

        print( "Render execution returned : %s" % mitsubaRender.status )

        if oiiotoolPath != "":
            self.resetImageDataWindow(imageName, oiiotoolPath)

        if not keepTempFiles:
            #Delete all of the temp file we just made
            os.chdir(renderDir)
            for geometryFile in geometryFiles:
                try:
                    #print( "Removing geometry : %s" % geometryFile )
                    os.remove(geometryFile)
                except:
                    print( "Error removing temporary file : %s" % geometryFile )
            #print( "Removing mitsuba scene description : %s" % outFileName )
            os.remove(outFileName)
            #os.remove(logName)
        else:
            print( "Keeping temporary files" )

        return imageName

    def exportAndRender(self,
                        renderDir,
                        renderSettings,
                        mitsubaPath,
                        oiiotoolPath,
                        mtsDir, 
                        keepTempFiles,  
                        animation, 
                        frame=None, 
                        verbose=False):

        if frame != None:
            # Calling this can lead to Maya 2016 locking up if you don't have MAYA_RELEASE_PYTHON_GIL set
            # See Readme
            cmds.currentTime(float(frame))
        else:
            frame = 1

        sceneName = self.getScenePrefix()

        scenePrefix = cmds.getAttr("defaultRenderGlobals.imageFilePrefix")
        if scenePrefix is None:
            scenePrefix = sceneName

        outFileName = os.path.join(renderDir, "%s.xml" % scenePrefix)

        # Export scene and geometry
        geometryFiles = MitsubaRendererIO.writeScene(outFileName, renderDir, renderSettings)

        # Render scene, delete scene and geometry
        imageName = self.renderScene(outFileName, renderDir, mitsubaPath, oiiotoolPath,
            mtsDir, keepTempFiles, geometryFiles, animation, frame, verbose,
            renderSettings)

        return imageName

def batchRenderProcedure(options):
    print("\n\n\nbatchRenderProcedure - options : %s\n\n\n" % str(options))

    '''
    kwargs = {}
    try:
        cmds.batchRender(mc='Mitsuba')
    except RuntimeError, err:
        print err
    '''

def batchRenderOptionsProcedure():
    print("\n\n\nbatchRenderOptionsProcedure\n\n\n")

def batchRenderOptionsStringProcedure():
    print("\n\n\nbatchRenderOptionsStringProcedure\n\n\n")
    return ' -r %s' % kPluginCmdName

def cancelBatchRenderProcedure():
    print("\n\n\ncancelBatchRenderProcedure\n\n\n")
    cmds.batchRender()

def commandRenderProcedure(options):
    print("\n\n\ncommandRenderProcedure - options : %s\n\n\n" % str(options))

    kwargs = {}
    try:
        cmds.Mitsuba(batch=True, **kwargs)
    except RuntimeError, err:
        print err

# Creator
def cmdCreator():
    return OpenMayaMPx.asMPxPtr( mitsubaForMaya() )

def createMelPythonCallback(module, function, options=False):
    # Return value for python mel command is documented as string[] but seems to return
    # string in some cases. Commands that don't have options are assumed to return string.
    # Commands with options are assumed to return string[]
    mel = ""
    if options:
        mel += "global proc string[] melPythonCallbackOptions_%s_%s(string $options) { " % (module, function)
        #mel += "    print(\"\\n\\n\\ncallback with options - %s, %s\\n\\n\\n\");" % (module, function)
        mel += "    string $result[] = python( \"import %s; %s.%s(\\\"\" + $options + \"\\\")\" ); " % (module, module, function)
        mel += "    return $result; "
        mel += "} "
        mel += "melPythonCallbackOptions_%s_%s" % (module, function)
    else:
        mel += "global proc string melPythonCallback_%s_%s() { " % (module, function)
        #mel += "    print(\"\\n\\n\\ncallback w/o  options - %s, %s\\n\\n\\n\");" % (module, function)
        mel += "    string $result = `python( \"import %s; %s.%s()\" )`; " % (module, module, function)
        mel += "    return $result; "
        mel += "} "
        mel += "melPythonCallback_%s_%s" % (module, function)

    return mel

# Register Renderer
def registerRenderer():
    cmds.renderer("Mitsuba", rendererUIName=kPluginCmdName)
    cmds.renderer("Mitsuba", edit=True, renderProcedure=kPluginCmdName)

    batchRenderProcedureMel = createMelPythonCallback("MitsubaRenderer", "batchRenderProcedure", True)
    cmds.renderer("Mitsuba", edit=True, batchRenderProcedure=batchRenderProcedureMel)

    commandRenderProcedureMel = createMelPythonCallback("MitsubaRenderer", "commandRenderProcedure", True)
    cmds.renderer("Mitsuba", edit=True, commandRenderProcedure=commandRenderProcedureMel)

    batchRenderOptionsProcedureMel = createMelPythonCallback("MitsubaRenderer", "batchRenderOptionsProcedure")
    cmds.renderer("Mitsuba", edit=True, batchRenderOptionsProcedure=batchRenderOptionsProcedureMel)

    batchRenderOptionsStringProcedureMel = createMelPythonCallback("MitsubaRenderer", "batchRenderOptionsStringProcedure")
    cmds.renderer("Mitsuba", edit=True, batchRenderOptionsStringProcedure=batchRenderOptionsStringProcedureMel)

    cancelBatchRenderProcedureMel = createMelPythonCallback("MitsubaRenderer", "cancelBatchRenderProcedure")
    cmds.renderer("Mitsuba", edit=True, cancelBatchRenderProcedure=cancelBatchRenderProcedureMel)

    cmds.renderer("Mitsuba", edit=True, renderRegionProcedure="mayaRenderRegion" )

    cmds.renderer("Mitsuba", edit=True, addGlobalsTab=("Common", 
        "createMayaSoftwareCommonGlobalsTab", 
        "updateMayaSoftwareCommonGlobalsTab"))

    cmds.renderer("Mitsuba", edit=True, addGlobalsTab=("Mitsuba Common", 
        createMelPythonCallback("MitsubaRendererUI", "createRenderSettings"),
        createMelPythonCallback("MitsubaRenderer", "updateRenderSettings")))

    cmds.renderer("Mitsuba", edit=True, addGlobalsNode="defaultMitsubaRenderGlobals" )


# Initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)

    # Load needed plugins
    try:
        if not cmds.pluginInfo( "objExport", query=True, loaded=True ):
            cmds.loadPlugin( "objExport" )
    except:
            sys.stderr.write( "Failed to load objExport plugin\n" )
            raise

    try:
        # Register Mitsuba Renderer
        mplugin.registerCommand( kPluginCmdName, cmdCreator )
    except:
        sys.stderr.write( "Failed to register command: %s\n" % kPluginCmdName )
        raise

    try:
        registerRenderer()
    except:
        sys.stderr.write( "Failed to register renderer: %s\n" % kPluginCmdName )
        raise

# Uninitialize the script plug-in
def uninitializePlugin(mobject):
    global materialNodeModules
    global generalNodeModules

    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        cmds.renderer("Mitsuba", edit=True, unregisterRenderer=True)
    except:
        sys.stderr.write( "Failed to unregister renderer: %s\n" % kPluginCmdName )

    try:
        mplugin.deregisterCommand( kPluginCmdName )
    except:
        sys.stderr.write( "Failed to unregister command: %s\n" % kPluginCmdName )

