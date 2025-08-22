# TsMyCellWithNPs Enhancement Documentation

## Overview
The `TsMyCellWithNPs` class has been enhanced to include a nucleus subcomponent of type `TsNucleus`. This allows for detailed DNA structure modeling within the cell geometry while maintaining the nanoparticle distribution functionality from `TsDistributedComponents`.

## Changes Made

### Header File (TsMyCellWithNPs.hh)
1. Added forward declaration for `TsNucleus` class
2. Added `CreateNucleusSubcomponent()` method declaration
3. Added nucleus-related member variables:
   - `fHasNucleus`: Boolean flag to check if nucleus is enabled
   - `fNucleusComponent`: Pointer to the TsNucleus component
   - Multiple nucleus parameter variables (material, geometry, DNA model parameters)

### Source File (TsMyCellWithNPs.cc)
1. Added include for `TsNucleus.hh` and `G4UIcommand.hh`
2. Enhanced constructor to read nucleus parameters from the parameter file
3. Modified destructor to properly clean up nucleus component
4. Enhanced `Construct()` method to call `CreateNucleusSubcomponent()`
5. Implemented `CreateNucleusSubcomponent()` method to:
   - Create parameter entries for the nucleus component
   - Instantiate a `TsNucleus` component
   - Construct the nucleus geometry

## Parameter File Usage

The enhanced class now supports nucleus parameters with the prefix `Ge/Cell/Nucleus...`. These parameters are automatically mapped to the internal TsNucleus component.

### Example Parameters
```
# Cell with nanoparticles and nucleus
s:Ge/Cell/Type                        = "TsMyCellWithNPs"
s:Ge/Cell/Parent                      = "CellLayer"
s:Ge/Cell/ComponentType               = "G4Tubs"
s:Ge/Cell/Material                    = "G4_WATER"
d:Ge/Cell/ComponentRadius             = Ge/RCell um
d:Ge/Cell/ComponentHL                 = Ge/HLCell um
d:Ge/Cell/ElementRadius	              = Ge/RNP nm
s:Ge/Cell/ElementMaterial             = Ma/NPMaterial
s:Ge/Cell/PositionsFile 	          = Ge/CellNPPositionsFile

# Nucleus parameters
s:Ge/Cell/NucleusMaterial                   = "G4_WATER"
s:Ge/Cell/NucleusColor                      = "White"
s:Ge/Cell/NucleusDNAModel					= "Sphere"
d:Ge/Cell/NucleusNucleusRadius              = 4.65 um
i:Ge/Cell/NucleusHilbertCurveLayer          = 4
i:Ge/Cell/NucleusHilbertCurve3DRepeat       = 30
s:Ge/Cell/NucleusHilbertCurveFileName       = "supportFiles/HilbertPoints_iteration1.dat"
# ... additional nucleus parameters
```

## Key Features

1. **Backward Compatibility**: The class remains fully compatible with existing parameter files that don't include nucleus parameters
2. **Automatic Detection**: Nucleus creation is automatically enabled when nucleus parameters are detected
3. **Full TsNucleus Integration**: Complete access to all TsNucleus features including DNA structure, histones, and chromatin fibers
4. **Proper Memory Management**: Nucleus component is properly created and destroyed

## Compilation Notes

This enhancement requires:
- TOPAS environment with Geant4
- Access to TsNucleus class and its dependencies
- Proper include paths for TOPAS extensions

The implementation provides a clean integration of nucleus functionality into the cell-with-nanoparticles geometry, enabling sophisticated DNA damage modeling in the presence of nanoparticles.
