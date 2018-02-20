import os
import struct

import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

import pymel.core

from process import Process

# Will be populated as materials are registered with Maya
materialNodeTypes = []

#
# XML formatted printing
#
def writeElementText(element, depth=0):
    #print( "element : %s" % str(element) )

    if element in [{}, None]:
        return ""

    if 'attributes' in element:
        attributes = element['attributes']
    else:
        attributes = {}
    if 'children' in element:
        children = element['children']
    else:
        children = []
    typeName = element['type']

    spacing = '\t'*depth

    elementText = ""
    elementText += spacing + "<%s" % typeName
    for key, value in attributes.iteritems():
        elementText += " %s=\"%s\"" % (key, value)
    if children:
        elementText += ">\n"
        for child in children:
            #print( "child : %s" % str(child) )
            elementText += writeElementText(child, depth+1)
            #element += "\n"
        elementText  += spacing + "</%s>\n" % typeName
    else:
        elementText += "/>\n"
    
    # Simple formatting cheat to make the files a little more readable
    if depth == 1:
        elementText += "\n"

    return elementText

# Other options to be provided later
def writeElement(outFile, element, depth=0):
    elementText = writeElementText(element, depth)
    outFile.write(elementText)

#
# IO functions
#

#
# General functionality
#

# Returns the surfaceShader node for a piece of geometry (geom)
def getSurfaceShader(geom):
    shapeNode = cmds.listRelatives(geom, children=True, shapes=True, fullPath=True)[0]
    sg = cmds.listConnections(shapeNode, type="shadingEngine")[0]
    shader = cmds.listConnections(sg+".surfaceShader")
    #if shader is None:
    #    shader = cmds.listConnections(sg+".volumeShader")
    if shader:
        shader = shader[0]
    return shader

def getVolumeShader(geom):
    shapeNode = cmds.listRelatives(geom, children=True, shapes=True, fullPath=True)[0]
    sg = cmds.listConnections(shapeNode, type="shadingEngine")[0]
    shader = cmds.listConnections(sg+".volumeShader")
    if shader:
        shader = shader[0]
    return shader

def listToMitsubaText(list):
    return " ".join( map(str, list) )

def booleanToMisubaText(b):
    if b:
        return "true"
    else:
        return "false"

#
# Scene Element representation
#
class SceneElement(dict):
    def __init__(self, elementType, attributes=None, *args):
        dict.__init__(self, args)
        self.children = []
        self.attributes = {}
        dict.__setitem__(self, 'children', self.children )
        dict.__setitem__(self, 'attributes', self.attributes )
        dict.__setitem__(self, 'type', elementType )
        if attributes:
            for key, value in attributes.iteritems():
                self.attributes[key] = value
      
    def addChild(self, child):
        self.children.append( child )
         
    def addChildren(self, children):
        self.children.extend( children )

    def getChild(self, index):
        return self.children[index]
        
    def addAttribute(self, key, value):
        self.attributes[key] = value

    def removeAttribute(self, key):
        if key in self.attributes:
            del( self.attributes[key] )         

    def getAttribute(self, key):
        if key in self.attributes:
            return self.attributes[key]
        else:
            return None

def BooleanParameter(name, value):
    return SceneElement('boolean', {'name':name, 'value':booleanToMisubaText(value)} )

def IntegerParameter(name, value):
    return SceneElement('integer', {'name':name, 'value':str(value)} )

def FloatParameter(name, value):
    return SceneElement('float', {'name':name, 'value':str(value)} )

def VectorParameter(name, x, y, z):
    return SceneElement('vector', {'name':name, 'x':str(x), 'y':str(y), 'z':str(z)} )

def PointParameter(name, x, y, z):
    return SceneElement('point', {'name':name, 'x':str(x), 'y':str(y), 'z':str(z)} )

def StringParameter(name, value):
    return SceneElement('string', {'name':name, 'value':str(value)} )

def ColorParameter(name, value, colorspace='srgb'):
    return SceneElement(colorspace, {'name':name, 'value':listToMitsubaText(value)} )

def SpectrumParameter(name, value):
    return SceneElement('spectrum', {'name':name, 'value':str(value)} )

def RotateElement(axis, angle):
    return SceneElement('rotate', { axis:str(1), 'angle':str(angle) } )

def TranslateElement(x, y, z):
    return SceneElement('translate', { 'x':str(x), 'y':str(y), 'z':str(z) } )

def Scale2Element(x, y):
    return SceneElement('scale', { 'x':x, 'y':y } )

def LookAtElement(aim, origin, up):
    return SceneElement('lookat', { 'target':listToMitsubaText(aim), 
        'origin':listToMitsubaText(origin), 'up':listToMitsubaText(up) } )

def createSceneElement(typeAttribute=None, id=None, elementType='scene'):
    element = SceneElement(elementType)
    if typeAttribute:
        element.addAttribute('type', typeAttribute)
    if id:
        element.addAttribute('id', id) 
    return element

def BSDFElement(typeAttribute=None, id=None):
    return createSceneElement(typeAttribute, id, 'bsdf')

def PhaseElement(typeAttribute=None, id=None):
    return createSceneElement(typeAttribute, id, 'phase')

def MediumElement(typeAttribute=None, id=None):
    return createSceneElement(typeAttribute, id, 'medium')

def ShapeElement(typeAttribute=None, id=None):
    return createSceneElement(typeAttribute, id, 'shape')

def EmitterElement(typeAttribute=None, id=None):
    return createSceneElement(typeAttribute, id, 'emitter')

def SubsurfaceElement(typeAttribute=None, id=None):
    return createSceneElement(typeAttribute, id, 'subsurface')

def IntegratorElement(typeAttribute=None, id=None):
    return createSceneElement(typeAttribute, id, 'integrator')

def FilmElement(typeAttribute=None, id=None):
    return createSceneElement(typeAttribute, id, 'film')

def SensorElement(typeAttribute=None, id=None):
    return createSceneElement(typeAttribute, id, 'sensor')

def SamplerElement(typeAttribute=None, id=None):
    return createSceneElement(typeAttribute, id, 'sampler')

def TransformElement(typeAttribute=None, id=None):
    return createSceneElement(typeAttribute, id, 'transform')

def RefElement(typeAttribute=None, id=None):
    return createSceneElement(typeAttribute, id, 'ref')

def VolumeElement(name, volumePath=None, typeAttribute='gridvolume'):
    element = createSceneElement(typeAttribute, elementType='volume')
    element.addAttribute('name', name)
    if volumePath:
        element.addChild( StringParameter('filename', volumePath) )

    return element

def NestedBSDFElement(material, connectedAttribute="bsdf", useDefault=True):
    hasNestedBSDF = False
    shaderElement = None

    connections = cmds.listConnections(material, connections=True)
    for i in range(len(connections)):
        if i%2==1:
            connection = connections[i]
            connectionType = cmds.nodeType(connection)

            if connectionType in materialNodeTypes and connections[i-1]==(material + "." + connectedAttribute):
                #We've found the nested bsdf, so build a structure for it
                shaderElement = writeShader(connection, connection)

                # Remove the id so there's no chance of this embedded definition conflicting with another
                # definition of the same BSDF                
                shaderElement.removeAttribute('id')

                hasNestedBSDF = True

    if useDefault and not hasNestedBSDF:
        bsdf = cmds.getAttr(material + "." + connectedAttribute)

        shaderElement = BSDFElement('diffuse')
        shaderElement.addChild( ColorParameter('reflectance', bsdf[0], colorspace='srgb') )

    return shaderElement

def getTextureFile(material, connectionAttr):
    connections = cmds.listConnections(material, connections=True)
    fileTexture = None
    for i in range(len(connections)):
        if i%2==1:
            connection = connections[i]
            connectionType = cmds.nodeType(connection)
            if connectionType == "file" and connections[i-1]==(material+"."+connectionAttr):
                fileTexture = cmds.getAttr(connection+".fileTextureName")
                hasFile=True
                #print( "Found texture : %s" % fileTexture )
                animatedTexture = cmds.getAttr("%s.%s" % (connection, "useFrameExtension"))
                if animatedTexture:
                    textureFrameNumber = cmds.getAttr("%s.%s" % (connection, "frameExtension"))
                    # Should make this an option at some point
                    tokens = fileTexture.split('.')
                    tokens[-2] = str(textureFrameNumber).zfill(4)
                    fileTexture = '.'.join(tokens)
                    #print( "Animated texture path : %s" % fileTexture )
            #else:
            #    print "Source can only be an image file"

    return fileTexture

def TextureElement(name, texturePath, scale=None):
    textureElementDict = createSceneElement('bitmap', elementType='texture')
    textureElementDict.addChild( StringParameter('filename', texturePath) )

    if scale:
        scaleElementDict = createSceneElement('scale', elementType='texture')
        scaleElementDict.addChild( FloatParameter('scale', scale) )
        scaleElementDict.addChild( textureElementDict )
        textureElementDict = scaleElementDict

    textureElementDict.addAttribute('name', name)
    return textureElementDict

def TexturedColorAttributeElement(material, attribute, mitsubaParameter=None, colorspace='srgb', scale=None):
    if not mitsubaParameter:
        mitsubaParameter = attribute
    fileTexture = getTextureFile(material, attribute)
    if fileTexture:
        element = TextureElement(mitsubaParameter, fileTexture, scale)
    else:
        value = cmds.getAttr(material + "." + attribute)
        element = ColorParameter(mitsubaParameter, value[0], colorspace )

    return element

def TexturedFloatAttributeElement(material, attribute, mitsubaParameter=None, scale=None):
    if not mitsubaParameter:
        mitsubaParameter = attribute
    fileTexture = getTextureFile(material, attribute)
    if fileTexture:
        element = TextureElement(mitsubaParameter, fileTexture, scale)
    else:
        value = cmds.getAttr(material + "." + attribute)
        element = FloatParameter(mitsubaParameter, value )

    return element

def TexturedVolumeAttributeElement(material, attribute, mitsubaParameter=None):
    if not mitsubaParameter:
        mitsubaParameter = attribute
    fileTexture = getTextureFile(material, attribute)
    if fileTexture:
        element = VolumeElement(mitsubaParameter, fileTexture)
    else:
        value = cmds.getAttr(material + "." + attribute)
        element = SpectrumParameter('value', value)

        volumeWrapperElement = VolumeElement(mitsubaParameter, typeAttribute='constvolume')
        volumeWrapperElement.addChild( element )
        element = volumeWrapperElement

    return element

# UI to API name mappings
conductorUIToPreset = {
    "100\% reflecting mirror" : "none",
    "Amorphous carbon" : "a-C",
    "Silver" : "Ag",
    "Aluminium" : "Al",
    "Cubic aluminium arsenide" : "AlAs",
    "Cubic aluminium antimonide" : "AlSb",
    "Gold" : "Au",
    "Polycrystalline beryllium" : "Be",
    "Chromium" : "Cr",
    "Cubic caesium iodide" : "CsI",
    "Copper" : "Cu",
    "Copper (I) oxide" : "Cu2O",
    "Copper (II) oxide" : "CuO",
    "Cubic diamond" : "d-C",
    "Mercury" : "Hg",
    "Mercury telluride" : "HgTe",
    "Iridium" : "Ir",
    "Polycrystalline potassium" : "K",
    "Lithium" : "Li",
    "Magnesium oxide" : "MgO",
    "Molybdenum" : "Mo",
    "Sodium" : "Na_palik",
    "Niobium" : "Nb",
    "Nickel" : "Ni_palik",
    "Rhodium" : "Rh",
    "Selenium" : "Se",
    "Hexagonal silicon carbide" : "SiC",
    "Tin telluride" : "SnTe",
    "Tantalum" : "Ta",
    "Trigonal tellurium" : "Te",
    "Polycryst. thorium (IV) fuoride" : "ThF4",
    "Polycrystalline titanium carbide" : "TiC",
    "Titanium nitride" : "TiN",
    "Tetragonal titan. dioxide" : "TiO2",
    "Vanadium carbide" : "VC",
    "Vanadium" : "V_palik",
    "Vanadium nitride" : "VN",
    "Tungsten" : "W",
}

distributionUIToPreset = {
    "Beckmann" : "beckmann",
    "GGX" : "ggx",
    "Phong" : "phong",
    "Ashikhmin Shirley" : "as",
}

iorMaterialUIToPreset = {
    "Vacuum" : "vacuum",
    "Helum"  : "helium",
    "Hydrogen" : "hydrogen",
    "Air" : "air",
    "Carbon Dioxide" : "carbon dioxide",
    "Water" : "water",
    "Acetone" : "acetone",
    "Ethanol" : "ethanol",
    "Carbon Tetrachloride" : "carbon tetrachloride",
    "Glycerol" : "glycerol",
    "Benzene" : "benzene",
    "Silicone Oil" : "silicone oil",
    "Bromine" : "bromine",
    "Water Ice" : "water ice",
    "Fused Quartz" : "fused quartz",
    "Pyrex" : "pyrex",
    "Acrylic Glass" : "acrylic glass",
    "Polypropylene" : "polypropylene",
    "BK7" : "bk7",
    "Sodium Chloride" : "sodium chloride",
    "Amber" : "amber",
    "Pet" : "pet",
    "Diamond" : "diamond",
}

wardVariantUIToPreset = {
    "Ward" : "ward",
    "Ward-Duer" : "ward-duer",
    "Balanced" : "balanced",
}

mediumMaterialUIToPreset = {
    "Apple" : "Apple",
    "Cream" : "Cream",
    "Skimmilk" : "Skimmilk",
    "Spectralon" : "Spectralon",
    "Chicken1" : "Chicken1",
    "Ketchup" : "Ketchup",
    "Skin1" : "Skin1",
    "Wholemilk" : "Wholemilk",
    "Chicken2" : "Chicken2",
    "Potato" : "Potato",
    "Skin2" : "Skin2",
    "Lowfat Milk" : "Lowfat Milk",
    "Reduced Milk" : "Reduced Milk",
    "Regular Milk" : "Regular Milk",
    "Espresso" : "Espresso",
    "Mint Mocha Coffee" : "Mint Mocha Coffee",
    "Lowfat Soy Milk" : "Lowfat Soy Milk",
    "Regular Soy Milk" : "Regular Soy Milk",
    "Lowfat Chocolate Milk" : "Lowfat Chocolate Milk",
    "Regular Chocolate Milk" : "Regular Chocolate Milk",
    "Coke" : "Coke",
    "Pepsi Sprite" : "Pepsi Sprite",
    "Gatorade" : "Gatorade",
    "Chardonnay" : "Chardonnay",
    "White Zinfandel" : "White Zinfandel",
    "Merlot" : "Merlot",
    "Budweiser Beer" : "Budweiser Beer",
    "Coors Light Beer" : "Coors Light Beer",
    "Clorox" : "Clorox",
    "Apple Juice" : "Apple Juice",
    "Cranberry Juice" : "Cranberry Juice",
    "Grape Juice" : "Grape Juice",
    "Ruby Grapefruit Juice" : "Ruby Grapefruit Juice",
    "White Grapefruit Juice" : "White Grapefruit Juice",
    "Shampoo" : "Shampoo",
    "Strawberry Shampoo" : "Strawberry Shampoo",
    "Head & Shoulders Shampoo" : "Head & Shoulders Shampoo",
    "Lemon Tea Powder" : "Lemon Tea Powder",
    "Orange Juice Powder" : "Orange Juice Powder",
    "Pink Lemonade Powder" : "Pink Lemonade Powder",
    "Cappuccino Powder" : "Cappuccino Powder",
    "Salt Powder" : "Salt Powder",
    "Sugar Powder" : "Sugar Powder",
    "Suisse Mocha" : "Suisse Mocha",
}

phaseFunctionUIToPreset = {
    "Isotropic" : "isotropic",
    "Henyey-Greenstein" : "hg",
    "Rayleigh" : "rayleigh",
    "Kajiya-Kay" : "kkay",
    "Micro-Flake" : "microflake",
}

samplingMethodUIToPreset = {
    "Simpson" : "simpson",
    "Woodcock" : "woodcock",
}

#
# Medium Scattering Models
#

# A homogeneous medium
def writeMediumHomogeneous(medium, mediumName):
    useSigmaAS = cmds.getAttr(medium+".useSigmaAS")
    useSigmaTAlbedo = cmds.getAttr(medium+".useSigmaTAlbedo")
    sigmaA = cmds.getAttr(medium+".sigmaA")
    sigmaS = cmds.getAttr(medium+".sigmaS")
    sigmaT = cmds.getAttr(medium+".sigmaT")
    albedo = cmds.getAttr(medium+".albedo")
    scale = cmds.getAttr(medium+".scale")    

    # Create a structure to be written
    mediumElement = MediumElement('homogeneous', mediumName)

    if useSigmaAS:
        mediumElement.addChild( ColorParameter('sigmaA', sigmaA[0], colorspace='rgb') )
        mediumElement.addChild( ColorParameter('sigmaS', sigmaS[0], colorspace='rgb') )

    elif useSigmaTAlbedo:
        mediumElement.addChild( ColorParameter('sigmaT', sigmaT[0], colorspace='rgb') )
        mediumElement.addChild( ColorParameter('albedo', albedo[0], colorspace='rgb') )

    else:
        materialString = cmds.getAttr(medium+".material", asString=True)
        mediumElement.addChild( StringParameter('material', materialString) )

    mediumElement.addChild( FloatParameter('scale', scale) )

    phaseFunctionUIName = cmds.getAttr(medium+".phaseFunction", asString=True)
    if phaseFunctionUIName in phaseFunctionUIToPreset:
        phaseFunctionName = phaseFunctionUIToPreset[phaseFunctionUIName]

        phaseFunctionElement = PhaseElement(phaseFunctionName)
        if phaseFunctionName == 'hg':
            g = cmds.getAttr(medium+".phaseFunctionHGG")
            phaseFunctionElement.addChild( FloatParameter('g', g) )
        elif phaseFunctionName == 'microflake':
            s = cmds.getAttr(medium+".phaseFunctionMFSD")
            phaseFunctionElement.addChild( FloatParameter('stddev', s) )

        mediumElement.addChild( phaseFunctionElement  )

    return mediumElement

# A heterogeneous medium
def writeMediumHeterogeneous(medium, mediumName):
    # Create a structure to be written
    mediumElement = MediumElement('heterogeneous', mediumName)

    samplingMethodUIName = cmds.getAttr(medium+".samplingMethod", asString=True)
    if samplingMethodUIName in samplingMethodUIToPreset:
        samplingMethodName = samplingMethodUIToPreset[samplingMethodUIName]
    mediumElement.addChild( StringParameter('method', samplingMethodName) )

    mediumElement.addChild( TexturedVolumeAttributeElement(medium, 'density') )
    mediumElement.addChild( TexturedVolumeAttributeElement(medium, 'albedo') )

    fileTexture = getTextureFile(medium, 'orientation')
    if fileTexture:
        mediumElement.addChild( VolumeElement('orientation', fileTexture) )

    scale = cmds.getAttr(medium+".scale")
    mediumElement.addChild( FloatParameter('scale', scale) )

    phaseFunctionUIName = cmds.getAttr(medium+".phaseFunction", asString=True)
    if phaseFunctionUIName in phaseFunctionUIToPreset:
        phaseFunctionName = phaseFunctionUIToPreset[phaseFunctionUIName]

        phaseFunctionElement = PhaseElement(phaseFunctionName)
        if phaseFunctionName == 'hg':
            g = cmds.getAttr(medium+".phaseFunctionHGG")
            phaseFunctionElement.addChild( FloatParameter('g', g) )
        elif phaseFunctionName == 'microflake':
            s = cmds.getAttr(medium+".phaseFunctionMFSD")
            phaseFunctionElement.addChild( FloatParameter('stddev', s) )

        mediumElement.addChild( phaseFunctionElement  )

    return mediumElement


#
# Surface Scattering Models
#
def writeShaderSmoothCoating(material, materialName):
    bsdfElement = BSDFElement('coating', materialName)

    thickness = cmds.getAttr(material+".thickness")
    bsdfElement.addChild( FloatParameter('thickness', thickness) )

    bsdfElement.addChild( TexturedColorAttributeElement(material, "sigmaA") )
    bsdfElement.addChild( TexturedColorAttributeElement(material, "specularReflectance") )

    # Get interior IOR preset or value
    interiorMaterialName = cmds.getAttr(material + ".interiorMaterial", asString=True)
    interiorMaterialName = interiorMaterialName.split('-')[0].strip()
    if interiorMaterialName in iorMaterialUIToPreset:
        interiorMaterialPreset = iorMaterialUIToPreset[interiorMaterialName]

        bsdfElement.addChild( StringParameter('intIOR', interiorMaterialPreset)  )
    else:
        intIOR = cmds.getAttr(material+".intior")
        bsdfElement.addChild( FloatParameter('intIOR', intIOR)  )

    # Get exterior IOR preset or value
    exteriorMaterialName = cmds.getAttr(material + ".exteriorMaterial", asString=True)
    exteriorMaterialName = exteriorMaterialName.split('-')[0].strip()
    if exteriorMaterialName in iorMaterialUIToPreset:
        exteriorMaterialPreset = iorMaterialUIToPreset[exteriorMaterialName]

        bsdfElement.addChild( StringParameter('extIOR', exteriorMaterialPreset)  )
    else:
        extIOR = cmds.getAttr(material+".extior")
        bsdfElement.addChild( FloatParameter('extIOR', extIOR)  )

    # Get connected BSDF
    nestedBSDFElement = NestedBSDFElement(material, "bsdf")
    if nestedBSDFElement:
        bsdfElement.addChild( nestedBSDFElement )

    return bsdfElement

def writeShaderConductor(material, materialName):
    extEta = cmds.getAttr(material+".extEta")

    conductorMaterialUI = cmds.getAttr(material+".material", asString=True)
    if conductorMaterialUI in conductorUIToPreset:
        conductorMaterialPreset = conductorUIToPreset[conductorMaterialUI]
    else:
        # Default to a perfectly reflective mirror
        conductorMaterialPreset = "none"

    # Create a structure to be written
    bsdfElement = BSDFElement('conductor', materialName)

    bsdfElement.addChild( StringParameter('material', conductorMaterialPreset) )
    bsdfElement.addChild( FloatParameter('extEta', extEta) )
    bsdfElement.addChild( TexturedColorAttributeElement(material, "specularReflectance") )

    return bsdfElement

def writeShaderDielectric(material, materialName):
    bsdfElement = BSDFElement('dielectric', materialName)

    # Get interior IOR preset or value
    interiorMaterialName = cmds.getAttr(material + ".interiorMaterial", asString=True)
    interiorMaterialName = interiorMaterialName.split('-')[0].strip()
    if interiorMaterialName in iorMaterialUIToPreset:
        interiorMaterialPreset = iorMaterialUIToPreset[interiorMaterialName]

        bsdfElement.addChild( StringParameter('intIOR', interiorMaterialPreset)  )
    else:
        intIOR = cmds.getAttr(material+".intior")
        bsdfElement.addChild( FloatParameter('intIOR', intIOR)  )

    # Get exterior IOR preset or value
    exteriorMaterialName = cmds.getAttr(material + ".exteriorMaterial", asString=True)
    exteriorMaterialName = exteriorMaterialName.split('-')[0].strip()
    if exteriorMaterialName in iorMaterialUIToPreset:
        exteriorMaterialPreset = iorMaterialUIToPreset[exteriorMaterialName]

        bsdfElement.addChild( StringParameter('extIOR', exteriorMaterialPreset)  )
    else:
        extIOR = cmds.getAttr(material+".extior")
        bsdfElement.addChild( FloatParameter('extIOR', extIOR)  )

    bsdfElement.addChild( TexturedColorAttributeElement(material, "specularReflectance") )
    bsdfElement.addChild( TexturedColorAttributeElement(material, "specularTransmittance") )

    return bsdfElement

def writeShaderDiffuseTransmitter(material, materialName):
    bsdfElement = BSDFElement('difftrans', materialName)
    bsdfElement.addChild( TexturedColorAttributeElement(material, "transmittance") )

    return bsdfElement

def writeShaderDiffuse(material, materialName):
    bsdfElement = BSDFElement('diffuse', materialName)
    bsdfElement.addChild( TexturedColorAttributeElement(material, "reflectance") )

    return bsdfElement

def writeShaderPhong(material, materialName):
    exponent = cmds.getAttr(material+".exponent")
    specularReflectance = cmds.getAttr(material+".specularReflectance")
    diffuseReflectance = cmds.getAttr(material+".diffuseReflectance")

    # Create a structure to be written
    bsdfElement = BSDFElement('phong', materialName)

    bsdfElement.addChild( TexturedFloatAttributeElement(material, "exponent")  )
    bsdfElement.addChild( TexturedColorAttributeElement(material, "diffuseReflectance") )
    bsdfElement.addChild( TexturedColorAttributeElement(material, "specularReflectance") )

    return bsdfElement

def writeShaderPlastic(material, materialName):
    bsdfElement = BSDFElement('plastic', materialName)

    # Get interior IOR preset or value
    interiorMaterialName = cmds.getAttr(material + ".interiorMaterial", asString=True)
    interiorMaterialName = interiorMaterialName.split('-')[0].strip()
    if interiorMaterialName in iorMaterialUIToPreset:
        interiorMaterialPreset = iorMaterialUIToPreset[interiorMaterialName]

        bsdfElement.addChild( StringParameter('intIOR', interiorMaterialPreset)  )
    else:
        intIOR = cmds.getAttr(material+".intior")
        bsdfElement.addChild( FloatParameter('intIOR', intIOR)  )

    # Get exterior IOR preset or value
    exteriorMaterialName = cmds.getAttr(material + ".exteriorMaterial", asString=True)
    exteriorMaterialName = exteriorMaterialName.split('-')[0].strip()
    if exteriorMaterialName in iorMaterialUIToPreset:
        exteriorMaterialPreset = iorMaterialUIToPreset[exteriorMaterialName]

        bsdfElement.addChild( StringParameter('extIOR', exteriorMaterialPreset)  )
    else:
        extIOR = cmds.getAttr(material+".extior")
        bsdfElement.addChild( FloatParameter('extIOR', extIOR)  )

    bsdfElement.addChild( TexturedColorAttributeElement(material, "diffuseReflectance") )
    bsdfElement.addChild( TexturedColorAttributeElement(material, "specularReflectance") )

    nonlinear = cmds.getAttr(material+".nonlinear")
    bsdfElement.addChild( BooleanParameter('nonlinear', nonlinear)  )

    return bsdfElement

def writeShaderRoughCoating(material, materialName):
    bsdfElement = BSDFElement('roughcoating', materialName)

    thickness = cmds.getAttr(material+".thickness")
    bsdfElement.addChild( FloatParameter('thickness', thickness) )
    bsdfElement.addChild( TexturedFloatAttributeElement(material, "alpha") )
    bsdfElement.addChild( TexturedColorAttributeElement(material, "sigmaA") )
    bsdfElement.addChild( TexturedColorAttributeElement(material, "specularReflectance") )

    distributionUI = cmds.getAttr(material+".distribution", asString=True)

    if distributionUI in distributionUIToPreset:
        distributionPreset = distributionUIToPreset[distributionUI]
    else:
        distributionPreset = "beckmann"

    bsdfElement.addChild( StringParameter('distribution', distributionPreset) )

    # Get interior IOR preset or value
    interiorMaterialName = cmds.getAttr(material + ".interiorMaterial", asString=True)
    interiorMaterialName = interiorMaterialName.split('-')[0].strip()
    if interiorMaterialName in iorMaterialUIToPreset:
        interiorMaterialPreset = iorMaterialUIToPreset[interiorMaterialName]

        bsdfElement.addChild( StringParameter('intIOR', interiorMaterialPreset)  )
    else:
        intIOR = cmds.getAttr(material+".intior")
        bsdfElement.addChild( FloatParameter('intIOR', intIOR)  )

    # Get exterior IOR preset or value
    exteriorMaterialName = cmds.getAttr(material + ".exteriorMaterial", asString=True)
    exteriorMaterialName = exteriorMaterialName.split('-')[0].strip()
    if exteriorMaterialName in iorMaterialUIToPreset:
        exteriorMaterialPreset = iorMaterialUIToPreset[exteriorMaterialName]

        bsdfElement.addChild( StringParameter('extIOR', exteriorMaterialPreset)  )
    else:
        extIOR = cmds.getAttr(material+".extior")
        bsdfElement.addChild( FloatParameter('extIOR', extIOR)  )

    # Get connected BSDF
    nestedBSDFElement = NestedBSDFElement(material, "bsdf")
    if nestedBSDFElement:
        bsdfElement.addChild( nestedBSDFElement )

    return bsdfElement

def writeShaderRoughConductor(material, materialName):
    distributionUI = cmds.getAttr(material+".distribution", asString=True)
    alphaUV = cmds.getAttr(material+".alphaUV")
    alpha = cmds.getAttr(material+".alpha")
    conductorMaterialUI = cmds.getAttr(material+".material", asString=True)
    extEta = cmds.getAttr(material+".extEta")

    if distributionUI in distributionUIToPreset:
        distributionPreset = distributionUIToPreset[distributionUI]
    else:
        distributionPreset = "beckmann"

    if conductorMaterialUI in conductorUIToPreset:
        conductorMaterialPreset = conductorUIToPreset[conductorMaterialUI]
    else:
        conductorMaterialPreset = "Cu"

    # Create a structure to be written
    bsdfElement = BSDFElement('roughconductor', materialName)

    bsdfElement.addChild( StringParameter('distribution', distributionPreset) )
    if distributionPreset == "as":
        bsdfElement.addChild( FloatParameter('alphaU', alphaUV[0]) )
        bsdfElement.addChild( FloatParameter('alphaV', alphaUV[1]) )
    else:
        bsdfElement.addChild( FloatParameter('alpha', alpha) )

    bsdfElement.addChild( StringParameter('material', conductorMaterialPreset) )
    bsdfElement.addChild( FloatParameter('extEta', extEta) )

    bsdfElement.addChild( TexturedColorAttributeElement(material, "specularReflectance") )

    return bsdfElement

def writeShaderRoughDielectric(material, materialName):
    bsdfElement = BSDFElement('roughdielectric', materialName)

    distributionUI = cmds.getAttr(material+".distribution", asString=True)
    if distributionUI in distributionUIToPreset:
        distributionPreset = distributionUIToPreset[distributionUI]
    else:
        distributionPreset = "beckmann"

    bsdfElement.addChild( StringParameter('distribution', distributionPreset) )
    if distributionPreset == "as":
        alphaUV = cmds.getAttr(material+".alphaUV")
        bsdfElement.addChild( FloatParameter('alphaU', alphaUV[0])  )
        bsdfElement.addChild( FloatParameter('alphaV', alphaUV[1])  )
    else:
        alpha = cmds.getAttr(material+".alpha")
        bsdfElement.addChild( TexturedFloatAttributeElement(material, "alpha") )

    # Get interior IOR preset or value
    interiorMaterialName = cmds.getAttr(material + ".interiorMaterial", asString=True)
    interiorMaterialName = interiorMaterialName.split('-')[0].strip()
    if interiorMaterialName in iorMaterialUIToPreset:
        interiorMaterialPreset = iorMaterialUIToPreset[interiorMaterialName]

        bsdfElement.addChild( StringParameter('intIOR', interiorMaterialPreset)  )
    else:
        intIOR = cmds.getAttr(material+".intior")
        bsdfElement.addChild( FloatParameter('intIOR', intIOR)  )

    # Get exterior IOR preset or value
    exteriorMaterialName = cmds.getAttr(material + ".exteriorMaterial", asString=True)
    exteriorMaterialName = exteriorMaterialName.split('-')[0].strip()
    if exteriorMaterialName in iorMaterialUIToPreset:
        exteriorMaterialPreset = iorMaterialUIToPreset[exteriorMaterialName]

        bsdfElement.addChild( StringParameter('extIOR', exteriorMaterialPreset)  )
    else:
        extIOR = cmds.getAttr(material+".extior")
        bsdfElement.addChild( FloatParameter('extIOR', extIOR)  )

    bsdfElement.addChild( TexturedColorAttributeElement(material, "specularReflectance") )
    bsdfElement.addChild( TexturedColorAttributeElement(material, "specularTransmittance") )

    return bsdfElement

def writeShaderRoughDiffuse(material, materialName):
    alpha = cmds.getAttr(material+".alpha")
    useFastApprox = cmds.getAttr(material+".useFastApprox")

    # Create a structure to be written
    bsdfElement = BSDFElement('roughdiffuse', materialName)

    bsdfElement.addChild( TexturedColorAttributeElement(material, "reflectance") )
    bsdfElement.addChild( FloatParameter('alpha', alpha)  )
    bsdfElement.addChild( BooleanParameter('useFastApprox', useFastApprox)  )

    return bsdfElement

def writeShaderRoughPlastic(material, materialName):
    bsdfElement = BSDFElement('roughplastic', materialName)

    bsdfElement.addChild( TexturedColorAttributeElement(material, "specularReflectance") )
    bsdfElement.addChild( TexturedColorAttributeElement(material, "diffuseReflectance") )

    distributionUI = cmds.getAttr(material+".distribution", asString=True)
    if distributionUI in distributionUIToPreset:
        distributionPreset = distributionUIToPreset[distributionUI]
    else:
        distributionPreset = "beckmann"

    bsdfElement.addChild( StringParameter('distribution', distributionPreset) )

    alpha = cmds.getAttr(material+".alpha")
    bsdfElement.addChild( TexturedFloatAttributeElement(material, "alpha") )

    # Get interior IOR preset or value
    interiorMaterialName = cmds.getAttr(material + ".interiorMaterial", asString=True)
    interiorMaterialName = interiorMaterialName.split('-')[0].strip()
    if interiorMaterialName in iorMaterialUIToPreset:
        interiorMaterialPreset = iorMaterialUIToPreset[interiorMaterialName]

        bsdfElement.addChild( StringParameter('intIOR', interiorMaterialPreset)  )
    else:
        intIOR = cmds.getAttr(material+".intior")
        bsdfElement.addChild( FloatParameter('intIOR', intIOR)  )

    # Get exterior IOR preset or value
    exteriorMaterialName = cmds.getAttr(material + ".exteriorMaterial", asString=True)
    exteriorMaterialName = exteriorMaterialName.split('-')[0].strip()
    if exteriorMaterialName in iorMaterialUIToPreset:
        exteriorMaterialPreset = iorMaterialUIToPreset[exteriorMaterialName]

        bsdfElement.addChild( StringParameter('extIOR', exteriorMaterialPreset)  )
    else:
        extIOR = cmds.getAttr(material+".extior")
        bsdfElement.addChild( FloatParameter('extIOR', extIOR)  )

    nonlinear = cmds.getAttr(material+".nonlinear")
    bsdfElement.addChild( BooleanParameter('nonlinear', nonlinear) )

    return bsdfElement

def writeShaderThinDielectric(material, materialName):
    bsdfElement = BSDFElement('thindielectric', materialName)

    # Get interior IOR preset or value
    interiorMaterialName = cmds.getAttr(material + ".interiorMaterial", asString=True)
    interiorMaterialName = interiorMaterialName.split('-')[0].strip()
    if interiorMaterialName in iorMaterialUIToPreset:
        interiorMaterialPreset = iorMaterialUIToPreset[interiorMaterialName]

        bsdfElement.addChild( StringParameter('intIOR', interiorMaterialPreset)  )
    else:
        intIOR = cmds.getAttr(material+".intior")
        bsdfElement.addChild( FloatParameter('intIOR', intIOR)  )

    # Get exterior IOR preset or value
    exteriorMaterialName = cmds.getAttr(material + ".exteriorMaterial", asString=True)
    exteriorMaterialName = exteriorMaterialName.split('-')[0].strip()
    if exteriorMaterialName in iorMaterialUIToPreset:
        exteriorMaterialPreset = iorMaterialUIToPreset[exteriorMaterialName]

        bsdfElement.addChild( StringParameter('extIOR', exteriorMaterialPreset)  )
    else:
        extIOR = cmds.getAttr(material+".extior")
        bsdfElement.addChild( FloatParameter('extIOR', extIOR)  )

    bsdfElement.addChild( TexturedColorAttributeElement(material, "specularReflectance") )
    bsdfElement.addChild( TexturedColorAttributeElement(material, "specularTransmittance") )

    return bsdfElement


def writeShaderWard(material, materialName):
    bsdfElement = BSDFElement('ward', materialName)

    variant = cmds.getAttr(material+".variant", asString=True)
    if variant in wardVariantUIToPreset:
        variantPreset = wardVariantUIToPreset[variant]
    else:
        variantPreset = "balanced"

    bsdfElement.addChild( StringParameter('variant', variantPreset)  )

    bsdfElement.addChild( TexturedFloatAttributeElement(material, "alphaU") )
    bsdfElement.addChild( TexturedFloatAttributeElement(material, "alphaV") )

    bsdfElement.addChild( TexturedColorAttributeElement(material, "diffuseReflectance") )
    bsdfElement.addChild( TexturedColorAttributeElement(material, "specularReflectance") )

    return bsdfElement

def writeShaderIrawan(material, materialName):
    filename = cmds.getAttr(material+".filename", asString=True)
    repeatu = cmds.getAttr(material+".repeatu")
    repeatv = cmds.getAttr(material+".repeatv")
    warpkd = cmds.getAttr(material+".warpkd")
    warpks = cmds.getAttr(material+".warpks")
    weftkd = cmds.getAttr(material+".weftkd")
    weftks = cmds.getAttr(material+".weftks")

    bsdfElement = BSDFElement('irawan', materialName)

    bsdfElement.addChild( StringParameter('filename', filename) )
    bsdfElement.addChild( FloatParameter('repeatU', repeatu) )
    bsdfElement.addChild( FloatParameter('repeatV', repeatv) )

    bsdfElement.addChild( ColorParameter('warp_kd', warpkd[0], colorspace='rgb') )
    bsdfElement.addChild( ColorParameter('warp_ks', warpks[0], colorspace='rgb') )

    bsdfElement.addChild( ColorParameter('weft_kd', weftkd[0], colorspace='rgb') )
    bsdfElement.addChild( ColorParameter('weft_ks', weftks[0], colorspace='rgb') )

    return bsdfElement

def writeShaderTwoSided(material, materialName):
    bsdfElement = BSDFElement('twosided', materialName)

    frontBSDFElement = NestedBSDFElement(material, "frontBSDF")
    bsdfElement.addChild( frontBSDFElement )

    backBSDFElement = NestedBSDFElement(material, "backBSDF", useDefault=False)
    if backBSDFElement:
        bsdfElement.addChild( backBSDFElement )

    return bsdfElement

def writeShaderMixture(material, materialName):
    bsdfElement = BSDFElement('mixturebsdf', materialName)

    weight1 = cmds.getAttr(material+".weight1")
    weight2 = cmds.getAttr(material+".weight2")
    weight3 = cmds.getAttr(material+".weight3")
    weight4 = cmds.getAttr(material+".weight4")

    weights = [weight1, weight2, weight3, weight4]
    weights = [x for x in weights if x != 0]
    weightString = ", ".join(map(str, weights))

    if weight1 > 0.0:
        bsdf1Element = NestedBSDFElement(material, "bsdf1")
        bsdfElement.addChild( bsdf1Element )

    if weight2 > 0.0:
        bsdf2Element = NestedBSDFElement(material, "bsdf2")
        bsdfElement.addChild( bsdf2Element )

    if weight3 > 0.0:
        bsdf3Element = NestedBSDFElement(material, "bsdf3")
        bsdfElement.addChild( bsdf3Element )

    if weight4 > 0.0:
        bsdf4Element = NestedBSDFElement(material, "bsdf4")
        bsdfElement.addChild( bsdf4Element )

    bsdfElement.addChild( StringParameter('weights', weightString) )

    return bsdfElement

def writeShaderBlend(material, materialName):
    bsdfElement = BSDFElement('blendbsdf', materialName)

    bsdfElement.addChild( TexturedFloatAttributeElement(material, "weight") )

    bsdf1Element = NestedBSDFElement(material, "bsdf1")
    bsdfElement.addChild( bsdf1Element )

    bsdf2Element = NestedBSDFElement(material, "bsdf2")
    bsdfElement.addChild( bsdf2Element )

    return bsdfElement

def writeShaderMask(material, materialName):
    bsdfElement = BSDFElement('mask', materialName)

    bsdfElement.addChild( TexturedColorAttributeElement(material, "opacity") )

    bsdf1Element = NestedBSDFElement(material, "bsdf")
    bsdfElement.addChild( bsdf1Element )

    return bsdfElement

def writeShaderBump(material, materialName):
    bsdfElement = BSDFElement('bumpmap', materialName)

    bumpScale = cmds.getAttr(material+".bumpScale")
    bsdfElement.addChild( TexturedColorAttributeElement(material, "texture", scale=bumpScale) )

    bsdf1Element = NestedBSDFElement(material, "bsdf")
    bsdfElement.addChild( bsdf1Element )

    return bsdfElement

def writeShaderHK(material, materialName):
    bsdfElement = BSDFElement('hk', materialName)

    useSigmaSA = cmds.getAttr(material+".useSigmaSA")
    useSigmaTAlbedo = cmds.getAttr(material+".useSigmaTAlbedo")
    if useSigmaSA:
        bsdfElement.addChild( TexturedColorAttributeElement(material, "sigmaS") )
        bsdfElement.addChild( TexturedColorAttributeElement(material, "sigmaA") )

    elif useSigmaTAlbedo:
        bsdfElement.addChild( TexturedColorAttributeElement(material, "sigmaT") )
        bsdfElement.addChild( TexturedColorAttributeElement(material, "albedo") )

    else:
        materialString = cmds.getAttr(material+".material", asString=True)
        bsdfElement.addChild( StringParameter('material', materialString) )

    thickness = cmds.getAttr(material+".thickness")
    bsdfElement.addChild( FloatParameter('thickness', thickness) )

    phaseFunctionUIName = cmds.getAttr(material+".phaseFunction", asString=True)
    if phaseFunctionUIName in phaseFunctionUIToPreset:
        phaseFunctionName = phaseFunctionUIToPreset[phaseFunctionUIName]

        phaseFunctionElement = PhaseElement(phaseFunctionName)
        if phaseFunctionName == 'hg':
            g = cmds.getAttr(material+".phaseFunctionHGG")
            phaseFunctionElement.addChild( FloatParameter('g', g) )
        elif phaseFunctionName == 'microflake':
            s = cmds.getAttr(material+".phaseFunctionMFSD")
            phaseFunctionElement.addChild( FloatParameter('stddev', s) )

        bsdfElement.addChild( phaseFunctionElement  )

    return bsdfElement

def writeShaderObjectAreaLight(material, materialName):
    elementDict = EmitterElement('area', materialName)

    color = cmds.getAttr(material+".radiance")
    samplingWeight = cmds.getAttr(material+".samplingWeight")

    elementDict.addChild( ColorParameter('radiance', color[0], colorspace='rgb') )
    elementDict.addChild( FloatParameter('samplingWeight', samplingWeight) )

    return elementDict

def writeShaderDipoleSSS(material, materialName):
    sssElement = SubsurfaceElement('dipole', materialName)

    useSigmaSA = cmds.getAttr(material+".useSigmaSA")
    useSigmaTAlbedo = cmds.getAttr(material+".useSigmaTAlbedo")
    if useSigmaSA:
        sigmaS = cmds.getAttr(material+".sigmaS")
        sigmaA = cmds.getAttr(material+".sigmaA")
        sssElement.addChild( ColorParameter("sigmaS", sigmaS[0]) )
        sssElement.addChild( ColorParameter("sigmaA", sigmaA[0]) )

    elif useSigmaTAlbedo:
        sigmaT = cmds.getAttr(material+".sigmaT")
        albedo = cmds.getAttr(material+".albedo")
        sssElement.addChild( ColorParameter("sigmaT", sigmaT[0]) )
        sssElement.addChild( ColorParameter("albedo", albedo[0]) )

    else:
        materialString = cmds.getAttr(material+".material", asString=True)
        sssElement.addChild( StringParameter('material', materialString) )

    scale = cmds.getAttr(material+".scale")
    sssElement.addChild( FloatParameter("scale", scale) )

    irrSamples = cmds.getAttr(material+".irrSamples")
    sssElement.addChild( IntegerParameter("irrSamples", irrSamples) )

    # Get interior IOR preset or value
    interiorMaterialName = cmds.getAttr(material + ".interiorMaterial", asString=True)
    interiorMaterialName = interiorMaterialName.split('-')[0].strip()
    if interiorMaterialName in iorMaterialUIToPreset:
        interiorMaterialPreset = iorMaterialUIToPreset[interiorMaterialName]

        sssElement.addChild( StringParameter('intIOR', interiorMaterialPreset)  )
    else:
        intIOR = cmds.getAttr(material+".intior")
        sssElement.addChild( FloatParameter('intIOR', intIOR)  )

    # Get exterior IOR preset or value
    exteriorMaterialName = cmds.getAttr(material + ".exteriorMaterial", asString=True)
    exteriorMaterialName = exteriorMaterialName.split('-')[0].strip()
    if exteriorMaterialName in iorMaterialUIToPreset:
        exteriorMaterialPreset = iorMaterialUIToPreset[exteriorMaterialName]

        sssElement.addChild( StringParameter('extIOR', exteriorMaterialPreset)  )
    else:
        extIOR = cmds.getAttr(material+".extior")
        sssElement.addChild( FloatParameter('extIOR', extIOR)  )

    return sssElement

def addTwoSided(material, materialElement):
    # Create a structure to be written
    elementDict = BSDFElement('twosided', material)

    # Remove the id so there's no chance of this embedded definition conflicting with another
    # definition of the same BSDF                
    materialElement.removeAttribute('id')

    elementDict.addChild( materialElement)
    
    return elementDict

#
#Write a surface material (material) to a Mitsuba scene file (outFile)
#
def writeShader(material, materialName):
    matType = cmds.nodeType(material)
    
    mayaMaterialTypeToShaderFunction = {
        "MitsubaSmoothCoatingShader" : writeShaderSmoothCoating,
        "MitsubaConductorShader" : writeShaderConductor,
        "MitsubaDielectricShader" : writeShaderDielectric,
        "MitsubaDiffuseTransmitterShader" : writeShaderDiffuseTransmitter,
        "MitsubaDiffuseShader" : writeShaderDiffuse,
        "MitsubaPhongShader" : writeShaderPhong,
        "MitsubaPlasticShader" : writeShaderPlastic,
        "MitsubaRoughCoatingShader" : writeShaderRoughCoating,
        "MitsubaRoughConductorShader" : writeShaderRoughConductor,
        "MitsubaRoughDielectricShader" : writeShaderRoughDielectric,
        "MitsubaRoughDiffuseShader" : writeShaderRoughDiffuse,
        "MitsubaRoughPlasticShader" : writeShaderRoughPlastic,
        "MitsubaThinDielectricShader" : writeShaderThinDielectric,
        "MitsubaWardShader" : writeShaderWard,
        "MitsubaIrawanShader" : writeShaderIrawan,
        "MitsubaObjectAreaLightShader" : writeShaderObjectAreaLight,
        "MitsubaTwoSidedShader" : writeShaderTwoSided,
        "MitsubaMixtureShader" : writeShaderMixture,
        "MitsubaBlendShader" : writeShaderBlend,
        "MitsubaMaskShader" : writeShaderMask,
        "MitsubaBumpShader" : writeShaderBump,
        "MitsubaHKShader" : writeShaderHK,
        "MitsubaHomogeneousParticipatingMedium" : writeMediumHomogeneous,
        "MitsubaHeterogeneousParticipatingMedium" : writeMediumHeterogeneous,
        "MitsubaSSSDipoleShader" : writeShaderDipoleSSS,
    }

    if matType in mayaMaterialTypeToShaderFunction:
        writeShaderFunction = mayaMaterialTypeToShaderFunction[matType]
    else:
        print( "Skipping unsupported material : %s." % matType)
        writeShaderFunction = None

    shaderElement = None
    if writeShaderFunction:
        shaderElement = writeShaderFunction(material, materialName)

        if "twosided" in cmds.listAttr(material) and cmds.getAttr(material + ".twosided"):
            shaderElement = addTwoSided(material, shaderElement)

    return shaderElement

#
#Write the appropriate integrator
#
def writeIntegratorPathTracer(renderSettings, integratorMitsuba):
    attrPrefixes = { 
        "path" : "", 
        "volpath" : "Volumetric", 
        "volpath_simple" : "SimpleVolumetric"
    }
    attrPrefix = attrPrefixes[integratorMitsuba]

    # Get values from the scene
    iPathTracerUseInfiniteDepth = cmds.getAttr("%s.%s" % (renderSettings, "i%sPathTracerUseInfiniteDepth" % attrPrefix))
    iPathTracerMaxDepth = cmds.getAttr("%s.%s" % (renderSettings, "i%sPathTracerMaxDepth" % attrPrefix))
    iPathTracerRRDepth = cmds.getAttr("%s.%s" % (renderSettings, "i%sPathTracerRRDepth" % attrPrefix))
    iPathTracerStrictNormals = cmds.getAttr("%s.%s" % (renderSettings, "i%sPathTracerStrictNormals" % attrPrefix))
    iPathTracerHideEmitters = cmds.getAttr("%s.%s" % (renderSettings, "i%sPathTracerHideEmitters" % attrPrefix))

    iPathTracerMaxDepth = -1 if iPathTracerUseInfiniteDepth else iPathTracerMaxDepth

    # Create a structure to be written
    element = IntegratorElement(integratorMitsuba)

    element.addChild( IntegerParameter('maxDepth', iPathTracerMaxDepth)  )
    element.addChild( IntegerParameter('rrDepth', iPathTracerRRDepth)  )
    element.addChild( BooleanParameter('strictNormals', iPathTracerStrictNormals)  )
    element.addChild( BooleanParameter('hideEmitters', iPathTracerHideEmitters)  )

    return element

def writeIntegratorBidirectionalPathTracer(renderSettings, integratorMitsuba):
    # Get values from the scene
    iBidrectionalPathTracerUseInfiniteDepth = cmds.getAttr("%s.%s" % (renderSettings, "iBidrectionalPathTracerUseInfiniteDepth"))
    iBidrectionalPathTracerMaxDepth = cmds.getAttr("%s.%s" % (renderSettings, "iBidrectionalPathTracerMaxDepth"))
    iBidrectionalPathTracerRRDepth = cmds.getAttr("%s.%s" % (renderSettings, "iBidrectionalPathTracerRRDepth"))
    iBidrectionalPathTracerLightImage = cmds.getAttr("%s.%s" % (renderSettings, "iBidrectionalPathTracerLightImage"))
    iBidrectionalPathTracerSampleDirect = cmds.getAttr("%s.%s" % (renderSettings, "iBidrectionalPathTracerSampleDirect"))

    iBidrectionalPathTracerMaxDepth = -1 if iBidrectionalPathTracerUseInfiniteDepth else iBidrectionalPathTracerMaxDepth

    # Create a structure to be written
    elementDict = IntegratorElement(integratorMitsuba)

    elementDict.addChild( IntegerParameter('maxDepth', iBidrectionalPathTracerMaxDepth) )
    elementDict.addChild( IntegerParameter('rrDepth', iBidrectionalPathTracerRRDepth) )
    elementDict.addChild( BooleanParameter('lightImage', iBidrectionalPathTracerLightImage) )
    elementDict.addChild( BooleanParameter('sampleDirect', iBidrectionalPathTracerSampleDirect) )

    return elementDict


def writeIntegratorAmbientOcclusion(renderSettings, integratorMitsuba):
    # Get values from the scene
    iAmbientOcclusionShadingSamples = cmds.getAttr("%s.%s" % (renderSettings, "iAmbientOcclusionShadingSamples"))
    iAmbientOcclusionUseAutomaticRayLength = cmds.getAttr("%s.%s" % (renderSettings, "iAmbientOcclusionUseAutomaticRayLength"))
    iAmbientOcclusionRayLength = cmds.getAttr("%s.%s" % (renderSettings, "iAmbientOcclusionRayLength"))

    iAmbientOcclusionRayLength = -1 if iAmbientOcclusionUseAutomaticRayLength else iAmbientOcclusionRayLength

    # Create a structure to be written
    elementDict = IntegratorElement(integratorMitsuba)

    elementDict.addChild( IntegerParameter('shadingSamples', iAmbientOcclusionShadingSamples) )
    elementDict.addChild( FloatParameter('rayLength', iAmbientOcclusionRayLength) )

    return elementDict


def writeIntegratorDirectIllumination(renderSettings, integratorMitsuba):
    # Get values from the scene
    iDirectIlluminationShadingSamples = cmds.getAttr("%s.%s" % (renderSettings, "iDirectIlluminationShadingSamples"))
    iDirectIlluminationUseEmitterAndBSDFSamples = cmds.getAttr("%s.%s" % (renderSettings, "iDirectIlluminationUseEmitterAndBSDFSamples"))
    iDirectIlluminationEmitterSamples = cmds.getAttr("%s.%s" % (renderSettings, "iDirectIlluminationEmitterSamples"))
    iDirectIlluminationBSDFSamples = cmds.getAttr("%s.%s" % (renderSettings, "iDirectIlluminationBSDFSamples"))
    iDirectIlluminationStrictNormals = cmds.getAttr("%s.%s" % (renderSettings, "iDirectIlluminationStrictNormals"))
    iDirectIlluminationHideEmitters = cmds.getAttr("%s.%s" % (renderSettings, "iDirectIlluminationHideEmitters"))

    # Create a structure to be written
    elementDict = IntegratorElement(integratorMitsuba)

    if iDirectIlluminationUseEmitterAndBSDFSamples:
        elementDict.addChild( IntegerParameter('emitterSamples', iDirectIlluminationEmitterSamples) )
        elementDict.addChild( IntegerParameter('bsdfSamples', iDirectIlluminationBSDFSamples) )
    else:
        elementDict.addChild( IntegerParameter('shadingSamples', iDirectIlluminationShadingSamples) )

    elementDict.addChild( BooleanParameter('strictNormals', iDirectIlluminationStrictNormals) )
    elementDict.addChild( BooleanParameter('hideEmitters', iDirectIlluminationHideEmitters) )

    return elementDict


def writeIntegratorPhotonMap(renderSettings, integratorMitsuba):
    # Get values from the scene
    iPhotonMapDirectSamples = cmds.getAttr("%s.%s" % (renderSettings, "iPhotonMapDirectSamples"))
    iPhotonMapGlossySamples = cmds.getAttr("%s.%s" % (renderSettings, "iPhotonMapGlossySamples"))
    iPhotonMapUseInfiniteDepth = cmds.getAttr("%s.%s" % (renderSettings, "iPhotonMapUseInfiniteDepth"))
    iPhotonMapMaxDepth = cmds.getAttr("%s.%s" % (renderSettings, "iPhotonMapMaxDepth"))
    iPhotonMapGlobalPhotons = cmds.getAttr("%s.%s" % (renderSettings, "iPhotonMapGlobalPhotons"))
    iPhotonMapCausticPhotons = cmds.getAttr("%s.%s" % (renderSettings, "iPhotonMapCausticPhotons"))
    iPhotonMapVolumePhotons = cmds.getAttr("%s.%s" % (renderSettings, "iPhotonMapVolumePhotons"))
    iPhotonMapGlobalLookupRadius = cmds.getAttr("%s.%s" % (renderSettings, "iPhotonMapGlobalLookupRadius"))
    iPhotonMapCausticLookupRadius = cmds.getAttr("%s.%s" % (renderSettings, "iPhotonMapCausticLookupRadius"))
    iPhotonMapLookupSize = cmds.getAttr("%s.%s" % (renderSettings, "iPhotonMapLookupSize"))
    iPhotonMapGranularity = cmds.getAttr("%s.%s" % (renderSettings, "iPhotonMapGranularity"))
    iPhotonMapHideEmitters = cmds.getAttr("%s.%s" % (renderSettings, "iPhotonMapHideEmitters"))
    iPhotonMapRRDepth = cmds.getAttr("%s.%s" % (renderSettings, "iPhotonMapRRDepth"))

    iPhotonMapMaxDepth = -1 if iPhotonMapUseInfiniteDepth else iPhotonMapMaxDepth

    # Create a structure to be written
    elementDict = IntegratorElement(integratorMitsuba)

    elementDict.addChild( IntegerParameter('directSamples', iPhotonMapDirectSamples) )
    elementDict.addChild( IntegerParameter('glossySamples', iPhotonMapGlossySamples) )

    elementDict.addChild( IntegerParameter('maxDepth', iPhotonMapMaxDepth) )

    elementDict.addChild( IntegerParameter('globalPhotons', iPhotonMapGlobalPhotons) )
    elementDict.addChild( IntegerParameter('causticPhotons', iPhotonMapCausticPhotons) )
    elementDict.addChild( IntegerParameter('volumePhotons', iPhotonMapVolumePhotons) )

    elementDict.addChild( FloatParameter('globalLookupRadius', iPhotonMapGlobalLookupRadius) )
    elementDict.addChild( FloatParameter('causticLookupRadius', iPhotonMapCausticLookupRadius) )

    elementDict.addChild( IntegerParameter('lookupSize', iPhotonMapLookupSize) )
    elementDict.addChild( IntegerParameter('granularity', iPhotonMapGranularity) )

    elementDict.addChild( BooleanParameter('hideEmitters', iPhotonMapHideEmitters) )
    elementDict.addChild( IntegerParameter('rrDepth', iPhotonMapRRDepth) )

    return elementDict


def writeIntegratorProgressivePhotonMap(renderSettings, integratorMitsuba):
    # Get values from the scene
    attrPrefixes = { 
        "ppm" : "", 
        "sppm" : "Stochastic", 
    }
    attrPrefix = attrPrefixes[integratorMitsuba]

    iProgressivePhotonMapUseInfiniteDepth = cmds.getAttr("%s.%s" % (renderSettings, "i%sProgressivePhotonMapUseInfiniteDepth" % attrPrefix))
    iProgressivePhotonMapMaxDepth = cmds.getAttr("%s.%s" % (renderSettings, "i%sProgressivePhotonMapMaxDepth" % attrPrefix))
    iProgressivePhotonMapPhotonCount = cmds.getAttr("%s.%s" % (renderSettings, "i%sProgressivePhotonMapPhotonCount" % attrPrefix))
    iProgressivePhotonMapInitialRadius = cmds.getAttr("%s.%s" % (renderSettings, "i%sProgressivePhotonMapInitialRadius" % attrPrefix))
    iProgressivePhotonMapAlpha = cmds.getAttr("%s.%s" % (renderSettings, "i%sProgressivePhotonMapAlpha" % attrPrefix))
    iProgressivePhotonMapGranularity = cmds.getAttr("%s.%s" % (renderSettings, "i%sProgressivePhotonMapGranularity" % attrPrefix))
    iProgressivePhotonMapRRDepth = cmds.getAttr("%s.%s" % (renderSettings, "i%sProgressivePhotonMapRRDepth" % attrPrefix))
    iProgressivePhotonMapMaxPasses = cmds.getAttr("%s.%s" % (renderSettings, "i%sProgressivePhotonMapMaxPasses" % attrPrefix))

    iProgressivePhotonMapMaxDepth = -1 if iProgressivePhotonMapUseInfiniteDepth else iProgressivePhotonMapMaxDepth

    # Create a structure to be written
    elementDict = IntegratorElement(integratorMitsuba)

    elementDict.addChild( IntegerParameter('maxDepth', iProgressivePhotonMapMaxDepth) )
    elementDict.addChild( IntegerParameter('photonCount', iProgressivePhotonMapPhotonCount) )

    elementDict.addChild( FloatParameter('initialRadius', iProgressivePhotonMapInitialRadius) )
    elementDict.addChild( FloatParameter('alpha', iProgressivePhotonMapAlpha) )

    elementDict.addChild( IntegerParameter('granularity', iProgressivePhotonMapGranularity) )
    elementDict.addChild( IntegerParameter('rrDepth', iProgressivePhotonMapRRDepth) )
    elementDict.addChild( IntegerParameter('maxPasses', iProgressivePhotonMapMaxPasses) )

    return elementDict


def writeIntegratorPrimarySampleSpaceMetropolisLightTransport(renderSettings, integratorMitsuba):
    # Get values from the scene
    iPrimarySampleSpaceMetropolisLightTransportBidirectional = cmds.getAttr("%s.%s" % (renderSettings, "iPrimarySampleSpaceMetropolisLightTransportBidirectional"))
    iPrimarySampleSpaceMetropolisLightTransportUseInfiniteDepth = cmds.getAttr("%s.%s" % (renderSettings, "iPrimarySampleSpaceMetropolisLightTransportUseInfiniteDepth"))
    iPrimarySampleSpaceMetropolisLightTransportMaxDepth = cmds.getAttr("%s.%s" % (renderSettings, "iPrimarySampleSpaceMetropolisLightTransportMaxDepth"))
    iPrimarySampleSpaceMetropolisLightTransportDirectSamples = cmds.getAttr("%s.%s" % (renderSettings, "iPrimarySampleSpaceMetropolisLightTransportDirectSamples"))
    iPrimarySampleSpaceMetropolisLightTransportRRDepth = cmds.getAttr("%s.%s" % (renderSettings, "iPrimarySampleSpaceMetropolisLightTransportRRDepth"))
    iPrimarySampleSpaceMetropolisLightTransportLuminanceSamples = cmds.getAttr("%s.%s" % (renderSettings, "iPrimarySampleSpaceMetropolisLightTransportLuminanceSamples"))
    iPrimarySampleSpaceMetropolisLightTransportTwoStage = cmds.getAttr("%s.%s" % (renderSettings, "iPrimarySampleSpaceMetropolisLightTransportTwoStage"))
    iPrimarySampleSpaceMetropolisLightTransportPLarge = cmds.getAttr("%s.%s" % (renderSettings, "iPrimarySampleSpaceMetropolisLightTransportPLarge"))

    iPrimarySampleSpaceMetropolisLightTransportMaxDepth = -1 if iPrimarySampleSpaceMetropolisLightTransportUseInfiniteDepth else iPrimarySampleSpaceMetropolisLightTransportMaxDepth

    # Create a structure to be written
    elementDict = IntegratorElement(integratorMitsuba)

    elementDict.addChild( BooleanParameter('bidirectional', iPrimarySampleSpaceMetropolisLightTransportBidirectional) )
    elementDict.addChild( IntegerParameter('maxDepth', iPrimarySampleSpaceMetropolisLightTransportMaxDepth) )
    elementDict.addChild( IntegerParameter('directSamples', iPrimarySampleSpaceMetropolisLightTransportDirectSamples) )
    elementDict.addChild( IntegerParameter('rrDepth', iPrimarySampleSpaceMetropolisLightTransportRRDepth) )
    elementDict.addChild( IntegerParameter('luminanceSamples', iPrimarySampleSpaceMetropolisLightTransportLuminanceSamples) )
    elementDict.addChild( BooleanParameter('twoStage', iPrimarySampleSpaceMetropolisLightTransportTwoStage) )
    elementDict.addChild( FloatParameter('pLarge', iPrimarySampleSpaceMetropolisLightTransportPLarge) )

    return elementDict


def writeIntegratorPathSpaceMetropolisLightTransport(renderSettings, integratorMitsuba):
    # Get values from the scene
    iPathSpaceMetropolisLightTransportUseInfiniteDepth = cmds.getAttr("%s.%s" % (renderSettings, "iPathSpaceMetropolisLightTransportUseInfiniteDepth"))
    iPathSpaceMetropolisLightTransportMaxDepth = cmds.getAttr("%s.%s" % (renderSettings, "iPathSpaceMetropolisLightTransportMaxDepth"))
    iPathSpaceMetropolisLightTransportDirectSamples = cmds.getAttr("%s.%s" % (renderSettings, "iPathSpaceMetropolisLightTransportDirectSamples"))
    iPathSpaceMetropolisLightTransportLuminanceSamples = cmds.getAttr("%s.%s" % (renderSettings, "iPathSpaceMetropolisLightTransportLuminanceSamples"))
    iPathSpaceMetropolisLightTransportTwoStage = cmds.getAttr("%s.%s" % (renderSettings, "iPathSpaceMetropolisLightTransportTwoStage"))
    iPathSpaceMetropolisLightTransportBidirectionalMutation = cmds.getAttr("%s.%s" % (renderSettings, "iPathSpaceMetropolisLightTransportBidirectionalMutation"))
    iPathSpaceMetropolisLightTransportLensPurturbation = cmds.getAttr("%s.%s" % (renderSettings, "iPathSpaceMetropolisLightTransportLensPurturbation"))
    iPathSpaceMetropolisLightTransportMultiChainPurturbation = cmds.getAttr("%s.%s" % (renderSettings, "iPathSpaceMetropolisLightTransportMultiChainPurturbation"))
    iPathSpaceMetropolisLightTransportCausticPurturbation = cmds.getAttr("%s.%s" % (renderSettings, "iPathSpaceMetropolisLightTransportCausticPurturbation"))
    iPathSpaceMetropolisLightTransportManifoldPurturbation = cmds.getAttr("%s.%s" % (renderSettings, "iPathSpaceMetropolisLightTransportManifoldPurturbation"))
    iPathSpaceMetropolisLightTransportLambda = cmds.getAttr("%s.%s" % (renderSettings, "iPathSpaceMetropolisLightTransportLambda"))

    iPathSpaceMetropolisLightTransportMaxDepth = -1 if iPathSpaceMetropolisLightTransportUseInfiniteDepth else iPathSpaceMetropolisLightTransportMaxDepth

    # Create a structure to be written
    elementDict = IntegratorElement(integratorMitsuba)

    elementDict.addChild( IntegerParameter('maxDepth', iPathSpaceMetropolisLightTransportMaxDepth) )
    elementDict.addChild( IntegerParameter('directSamples', iPathSpaceMetropolisLightTransportDirectSamples) )
    elementDict.addChild( IntegerParameter('luminanceSamples', iPathSpaceMetropolisLightTransportLuminanceSamples) )
    elementDict.addChild( BooleanParameter('twoStage', iPathSpaceMetropolisLightTransportTwoStage) )
    elementDict.addChild( BooleanParameter('bidirectionalMutation', iPathSpaceMetropolisLightTransportBidirectionalMutation) )
    elementDict.addChild( BooleanParameter('lensPerturbation', iPathSpaceMetropolisLightTransportLensPurturbation) )
    elementDict.addChild( BooleanParameter('multiChainPerturbation', iPathSpaceMetropolisLightTransportMultiChainPurturbation) )
    elementDict.addChild( BooleanParameter('causticPerturbation', iPathSpaceMetropolisLightTransportCausticPurturbation) )
    elementDict.addChild( BooleanParameter('manifoldPerturbation', iPathSpaceMetropolisLightTransportManifoldPurturbation) )
    elementDict.addChild( FloatParameter('lambda', iPathSpaceMetropolisLightTransportLambda) )

    return elementDict


def writeIntegratorEnergyRedistributionPathTracing(renderSettings, integratorMitsuba):
    # Get values from the scene
    iEnergyRedistributionPathTracingUseInfiniteDepth = cmds.getAttr("%s.%s" % (renderSettings, "iEnergyRedistributionPathTracingUseInfiniteDepth"))
    iEnergyRedistributionPathTracingMaxDepth = cmds.getAttr("%s.%s" % (renderSettings, "iEnergyRedistributionPathTracingMaxDepth"))
    iEnergyRedistributionPathTracingNumChains = cmds.getAttr("%s.%s" % (renderSettings, "iEnergyRedistributionPathTracingNumChains"))
    iEnergyRedistributionPathTracingMaxChains = cmds.getAttr("%s.%s" % (renderSettings, "iEnergyRedistributionPathTracingMaxChains"))
    iEnergyRedistributionPathTracingChainLength = cmds.getAttr("%s.%s" % (renderSettings, "iEnergyRedistributionPathTracingChainLength"))
    iEnergyRedistributionPathTracingDirectSamples = cmds.getAttr("%s.%s" % (renderSettings, "iEnergyRedistributionPathTracingDirectSamples"))
    iEnergyRedistributionPathTracingLensPerturbation = cmds.getAttr("%s.%s" % (renderSettings, "iEnergyRedistributionPathTracingLensPerturbation"))
    iEnergyRedistributionPathTracingMultiChainPerturbation = cmds.getAttr("%s.%s" % (renderSettings, "iEnergyRedistributionPathTracingMultiChainPerturbation"))
    iEnergyRedistributionPathTracingCausticPerturbation = cmds.getAttr("%s.%s" % (renderSettings, "iEnergyRedistributionPathTracingCausticPerturbation"))
    iEnergyRedistributionPathTracingManifoldPerturbation = cmds.getAttr("%s.%s" % (renderSettings, "iEnergyRedistributionPathTracingManifoldPerturbation"))
    iEnergyRedistributionPathTracingLambda = cmds.getAttr("%s.%s" % (renderSettings, "iEnergyRedistributionPathTracingLambda"))

    iEnergyRedistributionPathTracingMaxDepth = -1 if iEnergyRedistributionPathTracingUseInfiniteDepth else iEnergyRedistributionPathTracingMaxDepth

    # Create a structure to be written
    elementDict = IntegratorElement(integratorMitsuba)

    elementDict.addChild( IntegerParameter('maxDepth', iEnergyRedistributionPathTracingMaxDepth) )
    elementDict.addChild( FloatParameter('numChains', iEnergyRedistributionPathTracingNumChains) )
    elementDict.addChild( IntegerParameter('maxChains', iEnergyRedistributionPathTracingMaxChains) )
    elementDict.addChild( IntegerParameter('directSamples', iEnergyRedistributionPathTracingDirectSamples) )
    elementDict.addChild( IntegerParameter('chainLength', iEnergyRedistributionPathTracingChainLength) )
    elementDict.addChild( BooleanParameter('lensPerturbation', iEnergyRedistributionPathTracingLensPerturbation) )
    elementDict.addChild( BooleanParameter('multiChainPerturbation', iEnergyRedistributionPathTracingMultiChainPerturbation) )
    elementDict.addChild( BooleanParameter('causticPerturbation', iEnergyRedistributionPathTracingCausticPerturbation) )
    elementDict.addChild( BooleanParameter('manifoldPerturbation', iEnergyRedistributionPathTracingManifoldPerturbationText) )
    elementDict.addChild( FloatParameter('lambda', iEnergyRedistributionPathTracingLambda) )

    return elementDict

def writeIntegratorAdjointParticleTracer(renderSettings, integratorMitsuba):
    # Get values from the scene
    iAdjointParticleTracerUseInfiniteDepth = cmds.getAttr("%s.%s" % (renderSettings, "iAdjointParticleTracerUseInfiniteDepth"))
    iAdjointParticleTracerMaxDepth = cmds.getAttr("%s.%s" % (renderSettings, "iAdjointParticleTracerMaxDepth"))
    iAdjointParticleTracerRRDepth = cmds.getAttr("%s.%s" % (renderSettings, "iAdjointParticleTracerRRDepth"))
    iAdjointParticleTracerGranularity = cmds.getAttr("%s.%s" % (renderSettings, "iAdjointParticleTracerGranularity"))
    iAdjointParticleTracerBruteForce = cmds.getAttr("%s.%s" % (renderSettings, "iAdjointParticleTracerBruteForce"))

    iAdjointParticleTracerMaxDepth = -1 if iAdjointParticleTracerUseInfiniteDepth else iAdjointParticleTracerMaxDepth

    # Create a structure to be written
    elementDict = IntegratorElement(integratorMitsuba)

    elementDict.addChild( IntegerParameter('maxDepth', iAdjointParticleTracerMaxDepth) )
    elementDict.addChild( IntegerParameter('rrDepth', iAdjointParticleTracerRRDepth) )
    elementDict.addChild( IntegerParameter('granularity', iAdjointParticleTracerGranularity) )
    elementDict.addChild( BooleanParameter('bruteForce', iAdjointParticleTracerBruteForce) )

    return elementDict

def writeIntegratorVirtualPointLight(renderSettings, integratorMitsuba):
    # Get values from the scene
    iVirtualPointLightUseInfiniteDepth = cmds.getAttr("%s.%s" % (renderSettings, "iVirtualPointLightUseInfiniteDepth"))
    iVirtualPointLightMaxDepth = cmds.getAttr("%s.%s" % (renderSettings, "iVirtualPointLightMaxDepth"))
    iVirtualPointLightShadowMapResolution = cmds.getAttr("%s.%s" % (renderSettings, "iVirtualPointLightShadowMapResolution"))
    iVirtualPointLightClamping = cmds.getAttr("%s.%s" % (renderSettings, "iVirtualPointLightClamping"))

    iVirtualPointLightMaxDepth = -1 if iVirtualPointLightUseInfiniteDepth else iVirtualPointLightMaxDepth

    # Create a structure to be written
    elementDict = IntegratorElement(integratorMitsuba)

    elementDict.addChild( IntegerParameter('maxDepth', iVirtualPointLightMaxDepth) )
    elementDict.addChild( IntegerParameter('shadowMapResolution', iVirtualPointLightShadowMapResolution) )
    elementDict.addChild( FloatParameter('clamping', iVirtualPointLightClamping) )

    return elementDict


def writeIntegratorAdaptive(renderSettings, integratorMitsuba, subIntegrator):
    miAdaptiveMaxError = cmds.getAttr("%s.%s" % (renderSettings, "miAdaptiveMaxError"))
    miAdaptivePValue = cmds.getAttr("%s.%s" % (renderSettings, "miAdaptivePValue"))
    miAdaptiveMaxSampleFactor = cmds.getAttr("%s.%s" % (renderSettings, "miAdaptiveMaxSampleFactor"))

    # Create a structure to be written
    elementDict = IntegratorElement(integratorMitsuba)

    elementDict.addChild( FloatParameter('maxError', miAdaptiveMaxError/100.0) )
    elementDict.addChild( FloatParameter('pValue', miAdaptivePValue/100.0) )
    elementDict.addChild( IntegerParameter('maxSampleFactor', miAdaptiveMaxSampleFactor) )

    elementDict.addChild( subIntegrator )

    return elementDict

def writeIntegratorIrradianceCache(renderSettings, integratorMitsuba, subIntegrator):
    miIrradianceCacheResolution = cmds.getAttr("%s.%s" % (renderSettings, "miIrradianceCacheResolution"))
    miIrradianceCacheQuality = cmds.getAttr("%s.%s" % (renderSettings, "miIrradianceCacheQuality"))
    miIrradianceCacheGradients = cmds.getAttr("%s.%s" % (renderSettings, "miIrradianceCacheGradients"))
    miIrradianceCacheClampNeighbor = cmds.getAttr("%s.%s" % (renderSettings, "miIrradianceCacheClampNeighbor"))
    miIrradianceCacheClampScreen = cmds.getAttr("%s.%s" % (renderSettings, "miIrradianceCacheClampScreen"))
    miIrradianceCacheOverture = cmds.getAttr("%s.%s" % (renderSettings, "miIrradianceCacheOverture"))
    miIrradianceCacheQualityAdjustment = cmds.getAttr("%s.%s" % (renderSettings, "miIrradianceCacheQualityAdjustment"))
    miIrradianceCacheIndirectOnly = cmds.getAttr("%s.%s" % (renderSettings, "miIrradianceCacheIndirectOnly"))
    miIrradianceCacheDebug = cmds.getAttr("%s.%s" % (renderSettings, "miIrradianceCacheDebug"))

    # Create a structure to be written
    elementDict = IntegratorElement(integratorMitsuba)

    elementDict.addChild( IntegerParameter('resolution', miIrradianceCacheResolution) )
    elementDict.addChild( FloatParameter('quality', miIrradianceCacheQuality) )
    elementDict.addChild( BooleanParameter('gradients', miIrradianceCacheGradients) )
    elementDict.addChild( BooleanParameter('clampNeighbor', miIrradianceCacheClampNeighbor) )
    elementDict.addChild( BooleanParameter('clampScreen', miIrradianceCacheClampScreen) )
    elementDict.addChild( BooleanParameter('overture', miIrradianceCacheOvertureText) )
    elementDict.addChild( FloatParameter('qualityAdjustment', miIrradianceCacheQualityAdjustment) )
    elementDict.addChild( BooleanParameter('indirectOnly', miIrradianceCacheIndirectOnly) )
    elementDict.addChild( BooleanParameter('debug', miIrradianceCacheDebug) )

    elementDict.addChild( subIntegrator )

    return elementDict

def writeMetaIntegrator(renderSettings, metaIntegratorMaya, subIntegrator):
    mayaMetaIntegratorUINameToMitsubaName = {
        "Adaptive" : "adaptive",
        "Irradiance Cache" : "irrcache"
    }

    if metaIntegratorMaya in mayaMetaIntegratorUINameToMitsubaName:
        metaIntegratorMitsuba = mayaMetaIntegratorUINameToMitsubaName[metaIntegratorMaya]
    else:
        metaIntegratorMitsuba = None

    mayaMetaIntegratorUINameToIntegratorFunction = {
        "Adaptive" : writeIntegratorAdaptive,
        "Irradiance Cache" : writeIntegratorIrradianceCache
    }

    if metaIntegratorMitsuba:
        writeMetaIntegratorFunction = mayaMetaIntegratorUINameToIntegratorFunction[metaIntegratorMaya]
        integratorElement = writeMetaIntegratorFunction(renderSettings, metaIntegratorMitsuba, subIntegrator)
    else:
        integratorElement = subIntegrator

    return integratorElement

def writeIntegratorField(value):
    elementDict = IntegratorElement('field')
    elementDict.addChild( StringParameter('field', value) )
    return elementDict

def writeIntegratorMultichannel(renderSettings, subIntegrator):
    multichannelPosition = cmds.getAttr("%s.%s" % (renderSettings, "multichannelPosition"))
    multichannelRelPosition = cmds.getAttr("%s.%s" % (renderSettings, "multichannelRelPosition"))
    multichannelDistance = cmds.getAttr("%s.%s" % (renderSettings, "multichannelDistance"))
    multichannelGeoNormal = cmds.getAttr("%s.%s" % (renderSettings, "multichannelGeoNormal"))
    multichannelShadingNormal = cmds.getAttr("%s.%s" % (renderSettings, "multichannelShadingNormal"))
    multichannelUV = cmds.getAttr("%s.%s" % (renderSettings, "multichannelUV"))
    multichannelAlbedo = cmds.getAttr("%s.%s" % (renderSettings, "multichannelAlbedo"))
    multichannelShapeIndex = cmds.getAttr("%s.%s" % (renderSettings, "multichannelShapeIndex"))
    multichannelPrimIndex = cmds.getAttr("%s.%s" % (renderSettings, "multichannelPrimIndex"))

    # Create a structure to be written
    elementDict = IntegratorElement('multichannel')

    elementDict.addChild( subIntegrator )
    if multichannelPosition: elementDict.addChild( writeIntegratorField("position") )
    if multichannelRelPosition: elementDict.addChild( writeIntegratorField("relPosition") )
    if multichannelDistance: elementDict.addChild( writeIntegratorField("distance") )
    if multichannelGeoNormal: elementDict.addChild( writeIntegratorField("geoNormal") )
    if multichannelShadingNormal: elementDict.addChild( writeIntegratorField("shNormal") )
    if multichannelUV: elementDict.addChild( writeIntegratorField("uv") )
    if multichannelAlbedo: elementDict.addChild( writeIntegratorField("albedo") )
    if multichannelShapeIndex: elementDict.addChild( writeIntegratorField("shapeIndex") )
    if multichannelPrimIndex: elementDict.addChild( writeIntegratorField("primIndex") )

    return elementDict

def writeIntegrator(renderSettings):
    # Create base integrator
    integratorMaya = cmds.getAttr("%s.%s" % (renderSettings, "integrator")).replace('_', ' ')

    mayaUINameToMitsubaName = {
        "Ambient Occlusion" : "ao",
        "Direct Illumination" : "direct",
        "Path Tracer" : "path",
        "Volumetric Path Tracer" : "volpath",
        "Simple Volumetric Path Tracer" : "volpath_simple",
        "Bidirectional Path Tracer" : "bdpt",
        "Photon Map" : "photonmapper",
        "Progressive Photon Map" : "ppm",
        "Stochastic Progressive Photon Map" : "sppm",
        "Primary Sample Space Metropolis Light Transport" : "pssmlt",
        "Path Space Metropolis Light Transport" : "mlt",
        "Energy Redistribution Path Tracer" : "erpt",
        "Adjoint Particle Tracer" : "ptracer",
        "Virtual Point Lights" : "vpl"
    }

    if integratorMaya in mayaUINameToMitsubaName:
        integratorMitsuba = mayaUINameToMitsubaName[integratorMaya]
    else:
        integratorMitsuba = "path"

    mayaUINameToIntegratorFunction = {
        "Ambient Occlusion" : writeIntegratorAmbientOcclusion,
        "Direct Illumination" : writeIntegratorDirectIllumination,
        "Path Tracer" : writeIntegratorPathTracer,
        "Volumetric Path Tracer" : writeIntegratorPathTracer,
        "Simple Volumetric Path Tracer" : writeIntegratorPathTracer,
        "Bidirectional Path Tracer" : writeIntegratorBidirectionalPathTracer,
        "Photon Map" : writeIntegratorPhotonMap,
        "Progressive Photon Map" : writeIntegratorProgressivePhotonMap,
        "Stochastic Progressive Photon Map" : writeIntegratorProgressivePhotonMap,
        "Primary Sample Space Metropolis Light Transport" : writeIntegratorPrimarySampleSpaceMetropolisLightTransport,
        "Path Space Metropolis Light Transport" : writeIntegratorPathSpaceMetropolisLightTransport,
        "Energy Redistribution Path Tracer" : writeIntegratorEnergyRedistributionPathTracing,
        "Adjoint Particle Tracer" : writeIntegratorAdjointParticleTracer,
        "Virtual Point Lights" : writeIntegratorVirtualPointLight
    }

    if integratorMaya in mayaUINameToIntegratorFunction:
        writeIntegratorFunction = mayaUINameToIntegratorFunction[integratorMaya]
    else:
        print( "Unsupported Integrator : %s. Using Path Tracer" % integratorMaya)
        writeIntegratorFunction = writeIntegratorPathTracer

    integratorElement = writeIntegratorFunction(renderSettings, integratorMitsuba)

    # Create meta integrator
    metaIntegratorMaya = cmds.getAttr("%s.%s" % (renderSettings, "metaIntegrator")).replace('_', ' ')
    if metaIntegratorMaya != "None":
        integratorElement = writeMetaIntegrator(renderSettings, metaIntegratorMaya, integratorElement)

    # Create multichannel integrator
    multichannel = cmds.getAttr("%s.%s" % (renderSettings, "multichannel"))

    if multichannel:
        integratorElement = writeIntegratorMultichannel(renderSettings, integratorElement)

    return integratorElement

#
#Write image sample generator
#
def writeSampler(frameNumber, renderSettings):
    samplerMaya = cmds.getAttr("%s.%s" % (renderSettings, "sampler")).replace('_', ' ')
    sampleCount = cmds.getAttr("%s.%s" % (renderSettings, "sampleCount"))
    samplerDimension = cmds.getAttr("%s.%s" % (renderSettings, "samplerDimension"))
    samplerScramble = cmds.getAttr("%s.%s" % (renderSettings, "samplerScramble"))
    if samplerScramble == -1:
        samplerScramble = frameNumber

    mayaUINameToMitsubaName = {
        "Independent Sampler"  : "independent",
        "Stratified Sampler" : "stratified",
        "Low Discrepancy Sampler" : "ldsampler",
        "Halton QMC Sampler" : "halton",
        "Hammersley QMC Sampler" : "hammersley",
        "Sobol QMC Sampler" : "sobol"
    }

    if samplerMaya in mayaUINameToMitsubaName:
        samplerMitsuba = mayaUINameToMitsubaName[samplerMaya]
    else:
        samplerMitsuba = "independent"

    elementDict = SamplerElement(samplerMitsuba)

    elementDict.addChild( IntegerParameter('sampleCount', sampleCount) )

    if( samplerMaya == "Stratified Sampler" or
        samplerMaya == "Low Discrepancy Sampler" ):
        elementDict.addChild( IntegerParameter('dimension', samplerDimension) )

    elif( samplerMaya == "Halton QMC Sampler" or
        samplerMaya == "Hammersley QMC Sampler" or
        samplerMaya == "Sobol QMC Sampler" ):
        elementDict.addChild( IntegerParameter('scramble', samplerScramble) )

    return elementDict

def filmAddMultichannelAttributes(renderSettings, elementDict):
    multichannelPosition = cmds.getAttr("%s.%s" % (renderSettings, "multichannelPosition"))
    multichannelRelPosition = cmds.getAttr("%s.%s" % (renderSettings, "multichannelRelPosition"))
    multichannelDistance = cmds.getAttr("%s.%s" % (renderSettings, "multichannelDistance"))
    multichannelGeoNormal = cmds.getAttr("%s.%s" % (renderSettings, "multichannelGeoNormal"))
    multichannelShadingNormal = cmds.getAttr("%s.%s" % (renderSettings, "multichannelShadingNormal"))
    multichannelUV = cmds.getAttr("%s.%s" % (renderSettings, "multichannelUV"))
    multichannelAlbedo = cmds.getAttr("%s.%s" % (renderSettings, "multichannelAlbedo"))
    multichannelShapeIndex = cmds.getAttr("%s.%s" % (renderSettings, "multichannelShapeIndex"))
    multichannelPrimIndex = cmds.getAttr("%s.%s" % (renderSettings, "multichannelPrimIndex"))

    pixelFormat = "rgba"
    channelNames = "rgba"

    if multichannelPosition:
        pixelFormat  += ", rgb"
        channelNames += ", position"
    if multichannelRelPosition:
        pixelFormat  += ", rgb"
        channelNames += ", relPosition"
    if multichannelDistance:
        pixelFormat  += ", luminance"
        channelNames += ", distance"
    if multichannelGeoNormal:
        pixelFormat  += ", rgb"
        channelNames += ", geoNormal"
    if multichannelShadingNormal:
        pixelFormat  += ", rgb"
        channelNames += ", shadingNormal"
    if multichannelUV:
        pixelFormat  += ", rgb"
        channelNames += ", uv"
    if multichannelAlbedo:
        pixelFormat  += ", rgb"
        channelNames += ", albedo"
    if multichannelShapeIndex:
        pixelFormat  += ", luminance"
        channelNames += ", shapeIndex"
    if multichannelPrimIndex:
        pixelFormat  += ", luminance"
        channelNames += ", primitiveIndex"

    pixelFormatChild = None
    for child in elementDict['children']:
        attributes = child['attributes']
        if 'name' in attributes and attributes['name'] == 'pixelFormat':
            pixelFormatChild = child
            break

    if pixelFormatChild:
        elementDict['children'].remove( pixelFormatChild )

    elementDict.addChild( StringParameter('pixelFormat', pixelFormat) )
    elementDict.addChild( StringParameter('channelNames', channelNames) )

    return elementDict

def writeReconstructionFilter(renderSettings):
    #Filter
    reconstructionFilterMaya = cmds.getAttr("%s.%s" % (renderSettings, "reconstructionFilter")).replace('_' ,' ')
    mayaUINameToMitsubaName = {
        "Box filter"  : "box",
        "Tent filter" : "tent",
        "Gaussian filter" : "gaussian",
        "Catmull-Rom filter" : "catmullrom",
        "Lanczos filter" : "lanczos",
        "Mitchell-Netravali filter" : "mitchell"
    }

    if reconstructionFilterMaya in mayaUINameToMitsubaName:
        reconstructionFilterMitsuba = mayaUINameToMitsubaName[reconstructionFilterMaya]
    else:
        reconstructionFilterMitsuba = "box"

    rfilterElement = createSceneElement(typeAttribute=reconstructionFilterMitsuba, elementType='rfilter')

    return rfilterElement

def writeFilmHDR(renderSettings, filmMitsuba):
    fHDRFilmFileFormat = cmds.getAttr("%s.%s" % (renderSettings, "fHDRFilmFileFormat"))
    fHDRFilmPixelFormat = cmds.getAttr("%s.%s" % (renderSettings, "fHDRFilmPixelFormat"))
    fHDRFilmComponentFormat = cmds.getAttr("%s.%s" % (renderSettings, "fHDRFilmComponentFormat"))
    fHDRFilmAttachLog = cmds.getAttr("%s.%s" % (renderSettings, "fHDRFilmAttachLog"))
    fHDRFilmBanner = cmds.getAttr("%s.%s" % (renderSettings, "fHDRFilmBanner"))
    fHDRFilmHighQualityEdges = cmds.getAttr("%s.%s" % (renderSettings, "fHDRFilmHighQualityEdges"))

    mayaFileFormatUINameToMitsubaName = {
        "OpenEXR (.exr)"  : "openexr",
        "RGBE (.hdr)" : "rgbe",
        "Portable Float Map (.pfm)"  : "pfm"
    }

    if fHDRFilmFileFormat in mayaFileFormatUINameToMitsubaName:
        fHDRFilmFileFormatMitsuba = mayaFileFormatUINameToMitsubaName[fHDRFilmFileFormat]
    else:
        print( "Unsupported file format : %s. Using OpenEXR (.exr)" % fHDRFilmFileFormat)
        fHDRFilmFileFormatMitsuba = "openexr"

    mayaPixelFormatUINameToMitsubaName = {
        'Luminance' : 'luminance',
        'Luminance Alpha' : 'luminanceAlpha',
        'RGB' : 'rgb',
        'RGBA' : 'rgba',
        'XYZ' : 'xyz',
        'XYZA' : 'xyza',
        'Spectrum' : 'spectrum',
        'Spectrum Alpha' : 'spectrumAlpha'
    }

    if fHDRFilmPixelFormat in mayaPixelFormatUINameToMitsubaName:
        fHDRFilmPixelFormatMitsuba = mayaPixelFormatUINameToMitsubaName[fHDRFilmPixelFormat]
    else:
        print( "Unsupported pixel format : %s. Using RGB" % fHDRFilmPixelFormat)
        fHDRFilmPixelFormatMitsuba = "rgb"

    mayaComponentFormatUINameToMitsubaName = {
        'Float 16' : 'float16',
        'Float 32' : 'float32',
        'UInt 32' : 'uint32',
    }

    if fHDRFilmComponentFormat in mayaComponentFormatUINameToMitsubaName:
        fHDRFilmComponentFormatMitsuba = mayaComponentFormatUINameToMitsubaName[fHDRFilmComponentFormat]
    else:
        print( "Unsupported component format : %s. Using Float 16" % fHDRFilmComponentFormat)
        fHDRFilmComponentFormatMitsuba = "float16"

    elementDict = FilmElement(filmMitsuba)

    elementDict.addChild( StringParameter('fileFormat', fHDRFilmFileFormatMitsuba) )
    if fHDRFilmFileFormatMitsuba == "openexr":
        elementDict.addChild( StringParameter('pixelFormat', fHDRFilmPixelFormatMitsuba) )
    elementDict.addChild( StringParameter('componentFormat', fHDRFilmComponentFormatMitsuba ) )
    elementDict.addChild( BooleanParameter('attachLog', fHDRFilmAttachLog) )
    elementDict.addChild( BooleanParameter('banner', fHDRFilmBanner) )
    elementDict.addChild( BooleanParameter('highQualityEdges', fHDRFilmHighQualityEdges) )

    return elementDict

def writeFilmHDRTiled(renderSettings, filmMitsuba):
    fTiledHDRFilmPixelFormat = cmds.getAttr("%s.%s" % (renderSettings, "fTiledHDRFilmPixelFormat"))
    fTiledHDRFilmComponentFormat = cmds.getAttr("%s.%s" % (renderSettings, "fTiledHDRFilmComponentFormat"))

    mayaPixelFormatUINameToMitsubaName = {
        'Luminance' : 'luminance',
        'Luminance Alpha' : 'luminanceAlpha',
        'RGB' : 'rgb',
        'RGBA' : 'rgba',
        'XYZ' : 'xyz',
        'XYZA' : 'xyza',
        'Spectrum' : 'spectrum',
        'Spectrum Alpha' : 'spectrumAlpha'
    }

    if fTiledHDRFilmPixelFormat in mayaPixelFormatUINameToMitsubaName:
        fTiledHDRFilmPixelFormatMitsuba = mayaPixelFormatUINameToMitsubaName[fTiledHDRFilmPixelFormat]
    else:
        print( "Unsupported pixel format : %s. Using RGB" % fTiledHDRFilmPixelFormat)
        fTiledHDRFilmPixelFormatMitsuba = "rgb"

    mayaComponentFormatUINameToMitsubaName = {
        'Float 16' : 'float16',
        'Float 32' : 'float32',
        'UInt 32' : 'uint32',
    }

    if fTiledHDRFilmComponentFormat in mayaComponentFormatUINameToMitsubaName:
        fTiledHDRFilmComponentFormatMitsuba = mayaComponentFormatUINameToMitsubaName[fTiledHDRFilmComponentFormat]
    else:
        print( "Unsupported component format : %s. Using Float 16" % fTiledHDRFilmComponentFormat)
        fTiledHDRFilmComponentFormatMitsuba = "float16"

    elementDict = FilmElement(filmMitsuba)

    elementDict.addChild( StringParameter('pixelFormat', fTiledHDRFilmPixelFormatMitsuba) )
    elementDict.addChild( StringParameter('componentFormat', fTiledHDRFilmComponentFormatMitsuba) )

    return elementDict

def writeFilmLDR(renderSettings, filmMitsuba):
    fLDRFilmFileFormat = cmds.getAttr("%s.%s" % (renderSettings, "fLDRFilmFileFormat"))
    fLDRFilmPixelFormat = cmds.getAttr("%s.%s" % (renderSettings, "fLDRFilmPixelFormat"))
    fLDRFilmTonemapMethod = cmds.getAttr("%s.%s" % (renderSettings, "fLDRFilmTonemapMethod"))
    fLDRFilmGamma = cmds.getAttr("%s.%s" % (renderSettings, "fLDRFilmGamma"))
    fLDRFilmExposure = cmds.getAttr("%s.%s" % (renderSettings, "fLDRFilmExposure"))
    fLDRFilmKey = cmds.getAttr("%s.%s" % (renderSettings, "fLDRFilmKey"))
    fLDRFilmBurn = cmds.getAttr("%s.%s" % (renderSettings, "fLDRFilmBurn"))
    fLDRFilmBanner = cmds.getAttr("%s.%s" % (renderSettings, "fLDRFilmBanner"))
    fLDRFilmHighQualityEdges = cmds.getAttr("%s.%s" % (renderSettings, "fLDRFilmHighQualityEdges"))

    mayaFileFormatUINameToMitsubaName = {
        "PNG (.png)"  : "png",
        "JPEG (.jpg)" : "jpeg"
    }

    if fLDRFilmFileFormat in mayaFileFormatUINameToMitsubaName:
        fLDRFilmFileFormatMitsuba = mayaFileFormatUINameToMitsubaName[fLDRFilmFileFormat]
    else:
        print( "Unsupported file format : %s. Using PNG (.png)" % fLDRFilmFileFormat)
        fLDRFilmFileFormatMitsuba = "png"

    mayaPixelFormatUINameToMitsubaName = {
        'Luminance' : 'luminance',
        'Luminance Alpha' : 'luminanceAlpha',
        'RGB' : 'rgb',
        'RGBA' : 'rgba'
    }

    if fLDRFilmPixelFormat in mayaPixelFormatUINameToMitsubaName:
        fLDRFilmPixelFormatMitsuba = mayaPixelFormatUINameToMitsubaName[fLDRFilmPixelFormat]
    else:
        print( "Unsupported pixel format : %s. Using RGB" % fLDRFilmPixelFormat)
        fLDRFilmPixelFormatMitsuba = "rgb"

    mayaTonemapMethodUINameToMitsubaName = {
        'Gamma' : 'gamma',
        'Reinhard' : 'reinhard'
    }

    if fLDRFilmTonemapMethod in mayaTonemapMethodUINameToMitsubaName:
        fLDRFilmTonemapMethodMitsuba = mayaTonemapMethodUINameToMitsubaName[fLDRFilmTonemapMethod]
    else:
        print( "Unsupported tonemap method : %s. Using Gamma" % fLDRFilmTonemapMethod)
        fLDRFilmTonemapMethodMitsuba = "gamma"

    elementDict = FilmElement(filmMitsuba)

    elementDict.addChild( StringParameter('fileFormat', fLDRFilmFileFormatMitsuba) )
    elementDict.addChild( StringParameter('pixelFormat', fLDRFilmPixelFormatMitsuba) )
    elementDict.addChild( StringParameter('tonemapMethod', fLDRFilmTonemapMethodMitsuba) )
    elementDict.addChild( FloatParameter('gamma', fLDRFilmGamma) )
    elementDict.addChild( FloatParameter('exposure', fLDRFilmExposure) )
    elementDict.addChild( FloatParameter('key', fLDRFilmKey) )
    elementDict.addChild( FloatParameter('burn', fLDRFilmBurn) )
    elementDict.addChild( BooleanParameter('banner', fLDRFilmBanner) )
    elementDict.addChild( BooleanParameter('highQualityEdges', fLDRFilmHighQualityEdges) )

    return elementDict

def writeFilmMath(renderSettings, filmMitsuba):
    fMathFilmFileFormat = cmds.getAttr("%s.%s" % (renderSettings, "fMathFilmFileFormat"))
    fMathFilmPixelFormat = cmds.getAttr("%s.%s" % (renderSettings, "fMathFilmPixelFormat"))
    fMathFilmDigits = cmds.getAttr("%s.%s" % (renderSettings, "fMathFilmDigits"))
    fMathFilmVariable = cmds.getAttr("%s.%s" % (renderSettings, "fMathFilmVariable"))
    fMathFilmHighQualityEdges = cmds.getAttr("%s.%s" % (renderSettings, "fMathFilmHighQualityEdges"))

    mayaFileFormatUINameToMitsubaName = {
        "Matlab (.m)"  : "matlab",
        "Mathematica (.m)" : "mathematica",
        "NumPy (.npy)" : "numpy"
    }

    if fMathFilmFileFormat in mayaFileFormatUINameToMitsubaName:
        fMathFilmFileFormatMitsuba = mayaFileFormatUINameToMitsubaName[fMathFilmFileFormat]
    else:
        print( "Unsupported file format : %s. Using Matlab (.m)" % fMathFilmFileFormat)
        fMathFilmFileFormatMitsuba = "matlab"

    mayaPixelFormatUINameToMitsubaName = {
        'Luminance' : 'luminance',
        'Luminance Alpha' : 'luminanceAlpha',
        'RGB' : 'rgb',
        'RGBA' : 'rgba',
        'Spectrum' : 'spectrum',
        'Spectrum Alpha' : 'spectrumAlpha'
    }

    if fMathFilmPixelFormat in mayaPixelFormatUINameToMitsubaName:
        fMathFilmPixelFormatMitsuba = mayaPixelFormatUINameToMitsubaName[fMathFilmPixelFormat]
    else:
        print( "Unsupported pixel format : %s. Using RGB" % fMathFilmPixelFormat)
        fMathFilmPixelFormatMitsuba = "rgb"

    elementDict = FilmElement(filmMitsuba)

    elementDict.addChild( StringParameter('fileFormat', fMathFilmFileFormatMitsuba) )
    elementDict.addChild( StringParameter('pixelFormat', fMathFilmPixelFormatMitsuba) )
    elementDict.addChild( IntegerParameter('digits', fMathFilmDigits) )
    elementDict.addChild( StringParameter('variable', fMathFilmVariable) )
    elementDict.addChild( BooleanParameter('highQualityEdges', fMathFilmHighQualityEdges) )

    return elementDict

def addRenderRegionCropCoordinates(filmElement):
    editor = cmds.renderWindowEditor(q=True, editorName=True )
    #print( "addRenderRegionCropCoordinates - editor : %s" % editor )
    if editor:
        renderRegion = cmds.renderWindowEditor(editor, q=True, mq=True)
        #print( "addRenderRegionCropCoordinates - render region : %s" % renderRegion )
        if renderRegion:
            left = cmds.getAttr( "defaultRenderGlobals.left" )
            right = cmds.getAttr( "defaultRenderGlobals.rght" )
            top = cmds.getAttr( "defaultRenderGlobals.top" )
            bottom = cmds.getAttr( "defaultRenderGlobals.bot" )

            imageWidth = cmds.getAttr("defaultResolution.width")
            imageHeight = cmds.getAttr("defaultResolution.height")

            filmElement.addChild( IntegerParameter('cropOffsetX', left) )
            filmElement.addChild( IntegerParameter('cropOffsetY', imageHeight-top-1 ) )
            filmElement.addChild( IntegerParameter('cropWidth',   right-left+1 ) )
            filmElement.addChild( IntegerParameter('cropHeight',  top-bottom+1 ) )

    return filmElement

def writeFilm(frameNumber, renderSettings):
    #Resolution
    imageWidth = cmds.getAttr("defaultResolution.width")
    imageHeight = cmds.getAttr("defaultResolution.height")

    # Film
    filmMaya = cmds.getAttr("%s.%s" % (renderSettings, "film"))
    mayaFilmUINameToMitsubaName = {
        "HDR Film"  : "hdrfilm",
        "LDR Film" : "ldrfilm",
        "HDR Film - Tiled"  : "tiledhdrfilm",
        "Math Film"  : "mfilm",
    }
    if filmMaya in mayaFilmUINameToMitsubaName:
        filmMitsuba = mayaFilmUINameToMitsubaName[filmMaya]
    else:
        filmMitsuba = "hdrfilm"

    mayaUINameToFilmFunction = {
        "HDR Film" : writeFilmHDR,
        "LDR Film" : writeFilmLDR,
        "HDR Film - Tiled" : writeFilmHDRTiled,
        "Math Film" : writeFilmMath
    }

    if filmMaya in mayaUINameToFilmFunction:
        writeFilmFunction = mayaUINameToFilmFunction[filmMaya]
    else:
        print( "Unsupported Film : %s. Using HDR" % filmMaya)
        writeFilmFunction = writeFilmHDR

    filmElement = writeFilmFunction(renderSettings, filmMitsuba)

    rfilterElement = writeReconstructionFilter(renderSettings)

    # Set resolution
    imageWidth = cmds.getAttr("defaultResolution.width")
    imageHeight = cmds.getAttr("defaultResolution.height")
    filmElement.addChild( IntegerParameter('height', imageHeight) )
    filmElement.addChild( IntegerParameter('width', imageWidth) )

    # Set crop window
    filmElement = addRenderRegionCropCoordinates(filmElement)

    multichannel = cmds.getAttr("%s.%s" % (renderSettings, "multichannel"))
    if multichannel and filmMitsuba in ["hdrfilm", "tiledhdrfilm"]:
        filmElement = filmAddMultichannelAttributes(renderSettings, filmElement)

    return filmElement

#
#Write sensor, which include camera, image sampler, and film
#
def getRenderableCamera():
    cams = cmds.ls(type="camera", long=True)
    rCamShape = ""
    for cam in cams:
        isRenderable = cmds.getAttr(cam+".renderable")
        if isRenderable:
            print( "Render Settings - Camera           : %s" % cam )
            rCamShape = cam
            break

    if rCamShape == "":
        print( "No renderable camera found. Rendering with first camera : %s" % cams[0] )
        rCamShape = cams[0]

    return rCamShape

def writeSensor(frameNumber, renderSettings):
    # Find renderable camera
    rCamShape = getRenderableCamera()

    # Type
    camType = "perspective"
    if cmds.getAttr(rCamShape+".orthographic"):
        camType = "orthographic"
    elif cmds.getAttr(rCamShape+".depthOfField"):
        camType = "thinlens"

    sensorOverride = cmds.getAttr("%s.sensorOverride" % renderSettings)
    mayaUINameToMistubaSensor = { 
        "Spherical" : "spherical",
        "Telecentric" : "telecentric",
        "Radiance Meter" : "radiancemeter",
        "Fluence Meter" : "fluencemeter",
        "Perspective Pinhole Camera with Radial Distortion" : "perspective_rdist"
    }
    #"Irradiance Meter" : "irradiancemeter",

    if sensorOverride != "None":
        camType = mayaUINameToMistubaSensor[sensorOverride]
        print( "\n\n\nSensor Override : %s - %s\n\n\n" % (sensorOverride, camType) )

    # Orientation    
    camera = pymel.core.PyNode(rCamShape)
    camAim = camera.getWorldCenterOfInterest()
    camPos = camera.getEyePoint('world')
    camUp = camera.getWorldUp()

    # DoF
    apertureRadius = 1
    focusDistance = 1
    if camType == "thinlens":
        apertureRadius = cmds.getAttr(rCamShape+".focusRegionScale")
        focusDistance = cmds.getAttr(rCamShape+".focusDistance")

    # FoV
    fov = cmds.camera(rCamShape, query=True, horizontalFieldOfView=True)

    # Orthographic
    orthographicWidth = cmds.getAttr( rCamShape + ".orthographicWidth")
    orthographicWidth /= 2.0

    # Near Clip Plane
    nearClip = cmds.getAttr(rCamShape+".nearClipPlane")

    # Radial distortion
    perspectiveRdistKc2 = cmds.getAttr("%s.sPerspectiveRdistKc2" % renderSettings)
    perspectiveRdistKc4 = cmds.getAttr("%s.sPerspectiveRdistKc4" % renderSettings)

    # Write Camera
    elementDict = SensorElement( camType ) 

    if camType in ["thinlens", "perspective"]:
        elementDict.addChild( FloatParameter('fov', fov) )
        elementDict.addChild( StringParameter('fovAxis', 'x') )

    if camType in ["thinlens", "perspective", "orthographic", "telecentric"]:
        elementDict.addChild( FloatParameter('nearClip', nearClip) )

    if camType in ["thinlens", "telecentric"]:
        elementDict.addChild( FloatParameter('apertureRadius', apertureRadius) )
        elementDict.addChild( FloatParameter('focusDistance', focusDistance) )

    if camType in ["perspective_rdist"]:
        elementDict.addChild( StringParameter('kc', str(perspectiveRdistKc2) + ", " + str(perspectiveRdistKc4)) )

    # Generate transform
    transformDict = TransformElement() 
    transformDict.addAttribute('name', 'toWorld')

    if camType == "orthographic":
        transformDict.addChild( Scale2Element(orthographicWidth, orthographicWidth) )
    
    transformDict.addChild( LookAtElement(camAim, camPos, camUp) )

    elementDict.addChild( transformDict )

    # Write Sampler
    samplerDict = writeSampler(frameNumber, renderSettings)
    elementDict.addChild( samplerDict )

    # Write Film
    filmDict = writeFilm(frameNumber, renderSettings)
    elementDict.addChild( filmDict )

    return elementDict

def writeLightDirectional(light):
    intensity = cmds.getAttr(light+".intensity")
    color = cmds.getAttr(light+".color")[0]
    irradiance = [0,0,0]
    for i in range(3):
        irradiance[i] = intensity*color[i]

    matrix = cmds.getAttr(light+".worldMatrix")
    lightDir = [-matrix[8],-matrix[9],-matrix[10]]

    # Create a structure to be written
    elementDict = EmitterElement('directional')

    elementDict.addChild( ColorParameter('irradiance', irradiance, colorspace='rgb') )
    elementDict.addChild( VectorParameter('direction', lightDir[0], lightDir[1], lightDir[2]) )

    return elementDict

def writeLightPoint(light):
    intensity = cmds.getAttr(light+".intensity")
    color = cmds.getAttr(light+".color")[0]
    irradiance = [0,0,0]
    for i in range(3):
        irradiance[i] = intensity*color[i]

    matrix = cmds.getAttr(light+".worldMatrix")
    position = [matrix[12],matrix[13],matrix[14]]

    # Create a structure to be written
    elementDict = EmitterElement('point')

    elementDict.addChild( ColorParameter('intensity', irradiance, colorspace='rgb') )
    elementDict.addChild( PointParameter('position', position[0], position[1], position[2]) )

    return elementDict

def writeLightSpot(light):
    intensity = cmds.getAttr(light+".intensity")
    color = cmds.getAttr(light+".color")[0]
    irradiance = [0,0,0]
    for i in range(3):
        irradiance[i] = intensity*color[i]

    coneAngle = float(cmds.getAttr(light+".coneAngle"))/2.0
    penumbraAngle = float(cmds.getAttr(light+".penumbraAngle"))

    matrix = cmds.getAttr(light+".worldMatrix")
    position = [matrix[12],matrix[13],matrix[14]]

    transform = cmds.listRelatives( light, parent=True, fullPath=True )[0]
    rotation = cmds.getAttr(transform+".rotate")[0]

    # Create a structure to be written
    elementDict = EmitterElement('spot')

    elementDict.addChild( ColorParameter('intensity', irradiance, colorspace='rgb') )
    elementDict.addChild( FloatParameter('cutoffAngle', (coneAngle + penumbraAngle) ) )
    elementDict.addChild( FloatParameter('beamWidth', coneAngle) )

    transformDict = TransformElement()
    transformDict.addAttribute('name', 'toWorld')

    transformDict.addChild( RotateElement('y', 180.0) )
    if rotation[0] != 0.0:
        transformDict.addChild( RotateElement('x', rotation[0]) )
    if rotation[1] != 0.0:
        transformDict.addChild( RotateElement('y', rotation[1]) )
    if rotation[2] != 0.0:
        transformDict.addChild( RotateElement('z', rotation[2]) )
    transformDict.addChild( TranslateElement(position[0], position[1], position[2]) )

    elementDict.addChild( transformDict )

    return elementDict


def writeLightSunSky(sunsky):
    sun = cmds.getAttr(sunsky+".useSun")
    sky = cmds.getAttr(sunsky+".useSky")
    if sun and sky:
        emitterType = 'sunsky'
    elif sun:
        emitterType = 'sun'
    elif sky:
        emitterType = 'sky'
    else:
        print "Must use either sun or sky, defaulting to sunsky"
        emitterType = 'sunsky'

    turbidity = cmds.getAttr(sunsky+".turbidity")
    albedo = cmds.getAttr(sunsky+".albedo")
    date = cmds.getAttr(sunsky+".date")
    time = cmds.getAttr(sunsky+".time")
    latitude = cmds.getAttr(sunsky+".latitude")
    longitude = cmds.getAttr(sunsky+".longitude")
    timezone = cmds.getAttr(sunsky+".timezone")
    stretch = cmds.getAttr(sunsky+".stretch")
    resolution = cmds.getAttr(sunsky+".resolution")
    sunScale = cmds.getAttr(sunsky+".sunScale")
    skyScale = cmds.getAttr(sunsky+".skyScale")
    sunRadiusScale = cmds.getAttr(sunsky+".sunRadiusScale")

    # Create a structure to be written
    elementDict = EmitterElement( emitterType )

    elementDict.addChild( FloatParameter('turbidity', turbidity) )
    elementDict.addChild( ColorParameter('albedo', albedo[0]) )

    elementDict.addChild( IntegerParameter('year', date[0][0]) )
    elementDict.addChild( IntegerParameter('month', date[0][1]) )
    elementDict.addChild( IntegerParameter('day', date[0][2]) )

    elementDict.addChild( FloatParameter('hour', time[0][0]) )
    elementDict.addChild( FloatParameter('minute', time[0][1]) )
    elementDict.addChild( FloatParameter('second', time[0][2]) )

    elementDict.addChild( FloatParameter('latitude', latitude) )
    elementDict.addChild( FloatParameter('longitude', longitude) )
    elementDict.addChild( FloatParameter('timezone', timezone) )
    elementDict.addChild( FloatParameter('stretch', stretch) )

    elementDict.addChild( IntegerParameter('resolution', resolution) )

    elementDict.addChild( FloatParameter('sunScale', sunScale) )
    elementDict.addChild( FloatParameter('skyScale', skyScale) )
    elementDict.addChild( FloatParameter('sunRadiusScale', sunRadiusScale) )

    return elementDict

def writeLightEnvMap(envmap):
    connections = cmds.listConnections(envmap, plugs=False, c=True)
    fileName = ""
    hasFile = False
    correctFormat = True

    if connections:
        connectionAttr = "source"
        fileName = getTextureFile(envmap, connectionAttr)

        if fileName:
            extension = fileName[len(fileName)-3:len(fileName)]
            if extension == "hdr" or extension == "exr":
                hasFile = True
            else:
                print "file must be hdr or exr"
                correctFormat = False
        else:
            print "Please supply a fileName if you plan to use an environment map"
            correctFormat = False
    
    if correctFormat:
        if hasFile:
            scale = cmds.getAttr(envmap+".scale")
            gamma = cmds.getAttr(envmap+".gamma")
            cache = cmds.getAttr(envmap+".cache")

            samplingWeight = cmds.getAttr(envmap+".samplingWeight")
            rotate = cmds.getAttr(envmap+".rotate")[0]

            cacheText = 'true' if cache else 'false'

            # Create a structure to be written
            elementDict = EmitterElement('envmap')

            elementDict.addChild( StringParameter('filename', fileName) )
            elementDict.addChild( FloatParameter('scale', scale) )
            elementDict.addChild( FloatParameter('gamma', gamma) )
            elementDict.addChild( BooleanParameter('cache', cacheText) )
            elementDict.addChild( FloatParameter('samplingWeight', samplingWeight) )

            transformDict = TransformElement()

            transformDict.addAttribute('name', 'toWorld')
            transformDict.addChild( RotateElement('x', rotate[0]) )
            transformDict.addChild( RotateElement('y', rotate[1]) )
            transformDict.addChild( RotateElement('z', rotate[2]) )

            elementDict.addChild( transformDict )

            return elementDict

        else:
            radiance = cmds.getAttr(envmap+".source")
            samplingWeight = cmds.getAttr(envmap+".samplingWeight")

            # Create a structure to be written
            elementDict = EmitterElement('constant')

            elementDict.addChild( ColorParameter('radiance', radiance[0], colorspace='rgb') )
            elementDict.addChild( FloatParameter('samplingWeight', samplingWeight) )

            return elementDict


#
#Write lights
#
def isVisible(object):
    #print( "Checking visibility : %s" % object )
    visible = True

    if cmds.attributeQuery("visibility", node=object, exists=True):
        visible = visible and cmds.getAttr(object+".visibility")

    if cmds.attributeQuery("intermediateObject", node=object, exists=True):
        visible = visible and not cmds.getAttr(object+".intermediateObject")

    if cmds.attributeQuery("overrideEnabled", node=object, exists=True):
        visible = visible and cmds.getAttr(object+".overrideVisibility")

    if visible:
        parents = cmds.listRelatives(object, fullPath=True, parent=True)
        if parents:
            for parent in parents:
                parentVisible = isVisible(parent)
                if not parentVisible:
                    #print( "\tParent not visible. Breaking : %s" % parent )
                    visible = False
                    break
                
    #print( "\tVisibility : %s" % visible )
    
    return visible

def writeLights():
    # Gather visible lights
    lights = cmds.ls(type="light", long=True)
    lights = [x for x in lights if isVisible(x)]

    sunskyLights = cmds.ls(type="MitsubaSunsky", long=True)
    sunskyLights = [x for x in sunskyLights if isVisible(x)]

    envLights = cmds.ls(type="MitsubaEnvironmentLight", long=True)
    envLights = [x for x in envLights if isVisible(x)]

    # Warn if multiple environment lights are active
    if sunskyLights and envLights or sunskyLights and len(sunskyLights)>1 or envLights and len(envLights)>1:
        print( "\n" )
        print( "Cannot specify more than one environment light (MitsubaSunsky and MitsubaEnvironmentLight)" )
        print( "Using first environment or sunsky light")
        print( "\n" )

    # Create light elements
    lightElements = []

    # Gather element definitions for standard lights
    for light in lights:
        lightType = cmds.nodeType(light)
        if lightType == "directionalLight":
            lightElements.append( writeLightDirectional(light) )
        elif lightType == "pointLight":
            lightElements.append( writeLightPoint(light) )
        elif lightType == "spotLight":
            lightElements.append( writeLightSpot(light) )

    # Gather element definitions for Environment lights
    if envLights:
        envmap = envLights[0]
        lightElements.append( writeLightEnvMap(envmap) )

    # Gather element definitions for Sun and Sky lights
    if envLights == [] and sunskyLights:
        sunsky = sunskyLights[0]
        lightElements.append( writeLightSunSky(sunsky) )

    return lightElements

def getRenderableGeometry():
    # Build list of visible geometry
    transforms = cmds.ls(type="transform", long=True)
    geoms = []

    for transform in transforms:
        rels = cmds.listRelatives(transform, fullPath=True)
        if rels:
            for rel in rels:
                if cmds.nodeType(rel)=="mesh":
                    visible = isVisible(transform)
                    if visible:
                        if transform not in geoms:
                            geoms.append(transform)
                            #print( "getRenderableGeometry - transform : %s" % transform )

    return geoms

def writeMaterials(geoms):
    writtenMaterials = []
    materialElements = []

    #Write the material for each piece of geometry in the scene
    for geom in geoms:
        #print( "writeMaterials - geom : %s" % geom )
        # Surface shader
        material = getSurfaceShader(geom)
        if material and material not in writtenMaterials:

            materialType = cmds.nodeType(material)
            if materialType in materialNodeTypes:
                if materialType not in ["MitsubaObjectAreaLightShader"]:
                    materialElement = writeShader(material, material)

                    materialElements.append(materialElement)
                    writtenMaterials.append(material)

        # Medium / Volume shaders
        mediumMaterial = getVolumeShader(geom)
        if mediumMaterial and mediumMaterial not in writtenMaterials:

            materialType = cmds.nodeType(mediumMaterial)
            if materialType in materialNodeTypes:
                mediumMaterialElement = writeShader(mediumMaterial, mediumMaterial)

                materialElements.append(mediumMaterialElement)
                writtenMaterials.append(mediumMaterial)
        
    return writtenMaterials, materialElements

def exportGeometry(geom, renderDir):
    geomFilename = geom.replace(':', '__').replace('|', '__')

    cmds.select(geom)

    objFilenameFullPath = os.path.join(renderDir, geomFilename + ".obj")
    objFile = cmds.file(objFilenameFullPath, op=True, typ="OBJexport", options="groups=1;ptgroups=1;materials=0;smoothing=1;normals=1", exportSelected=True, force=True)

    return objFilenameFullPath

def writeShape(geomFilename, surfaceShader, mediumShader, renderDir):
    shapeDict = ShapeElement('obj')

    # Add reference to exported geometry
    shapeDict.addChild( StringParameter('filename', geomFilename) )

    # Write medium shader reference
    if mediumShader and cmds.nodeType(mediumShader) in materialNodeTypes:
        if cmds.nodeType(mediumShader) == "MitsubaSSSDipoleShader":
            refDict = RefElement()
            refDict.addAttribute('id', mediumShader)
        else:
            refDict = RefElement()
            refDict.addAttribute('name', 'interior')
            refDict.addAttribute('id', mediumShader)

        shapeDict.addChild( refDict)

    # Write surface shader reference
    if surfaceShader and cmds.nodeType(surfaceShader) in materialNodeTypes:
        # Check for area lights
        if cmds.nodeType(surfaceShader) == "MitsubaObjectAreaLightShader":
            shaderElement = writeShaderObjectAreaLight(surfaceShader, surfaceShader)
            shapeDict.addChild( shaderElement )

        # Otherwise refer to the already written material
        else:
            refDict = RefElement()
            refDict.addAttribute('id', surfaceShader)

            shapeDict.addChild( refDict)
    
    return shapeDict


def writeGeometryAndMaterials(renderDir):
    geoms = getRenderableGeometry()

    writtenMaterials, materialElements = writeMaterials(geoms)

    geoFiles = []
    shapeElements = []

    #Write each piece of geometry with references to materials
    for geom in geoms:
        #print( "writeGeometryAndMaterials - geometry : %s" % geom )
        surfaceShader = getSurfaceShader(geom)
        volumeShader  = getVolumeShader(geom)

        #print( "\tsurface : %s" % surfaceShader )
        #print( "\tvolume  : %s" % volumeShader )

        geomFilename = exportGeometry(geom, renderDir)
        geoFiles.append(geomFilename)

        shapeElement = writeShape(geomFilename, surfaceShader, volumeShader, renderDir)
        shapeElements.append(shapeElement)

    return (geoFiles, shapeElements, materialElements)

def writeScene(outFileName, renderDir, renderSettings):
    #
    # Generate scene element hierarchy
    #
    sceneElement = createSceneElement()

    # Should make this query the binary...
    sceneElement.addAttribute('version', '0.5.0')

    # Get integrator
    integratorElement = writeIntegrator(renderSettings)
    sceneElement.addChild( integratorElement)

    # Get sensor : camera, sampler, and film
    frameNumber = int(cmds.currentTime(query=True))
    sensorElement = writeSensor(frameNumber, renderSettings)
    sceneElement.addChild( sensorElement)

    # Get lights
    lightElements = writeLights()
    if lightElements:
        sceneElement.addChildren( lightElements )

    # Get geom and material assignments
    (exportedGeometryFiles, shapeElements, materialElements) = writeGeometryAndMaterials(renderDir)
    if materialElements:
        sceneElement.addChildren( materialElements )

    if shapeElements:
        sceneElement.addChildren( shapeElements )

    #
    # Write the structure to disk
    #
    with open(outFileName, 'w+') as outFile:
        outFile.write("<?xml version=\'1.0\' encoding=\'utf-8\'?>\n")
        writeElement(outFile, sceneElement)

    return exportedGeometryFiles

