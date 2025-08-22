# DNA Damage Scorer Integration Guide for TsMyCellWithNPs

## Overview
This guide explains how to integrate DNA damage scoring capability from Phase3 simulations into the Phase2 simulation using the enhanced `TsMyCellWithNPs` class with nucleus subcomponent functionality.

## Problem and Solution

### The Challenge
The original Phase3 DNA damage scorer (`TsScoreDNADamageSBSNucleus`) was designed to work with a standalone `TsNucleus` component declared directly in the parameter file. However, in the enhanced `TsMyCellWithNPs` class, the nucleus is created as an internal subcomponent and is not directly accessible as a standalone component in the parameter file.

### The Solution
A new custom scorer class `TsMyCellNucleusDNADamageSBS` was created that:
1. **Inherits from `TsScoreDNADamageSBSNucleus`** - Preserves all DNA damage scoring functionality
2. **Targets the Cell component** - Points to the parent Cell component instead of a non-existent standalone Nucleus component
3. **Filters for nucleus subcomponent** - Uses volume hierarchy checking to ensure scoring only occurs within the nucleus subcomponent
4. **Maintains parameter compatibility** - Uses the same parameter structure as the original Phase3 scorer

## Implementation Details

### New Scorer Class: TsMyCellNucleusDNADamageSBS

**Header file (`TsMyCellNucleusDNADamageSBS.hh`):**
- Inherits from `TsScoreDNADamageSBSNucleus`
- Overrides `ProcessHits()` method to filter for nucleus subcomponent
- Adds helper method `IsInNucleusSubcomponent()` for volume filtering

**Implementation file (`TsMyCellNucleusDNADamageSBS.cc`):**
- **Constructor**: Calls parent constructor, inherits all DNA damage scoring setup
- **ProcessHits()**: First checks if step is in nucleus subcomponent, then calls parent ProcessHits if valid
- **IsInNucleusSubcomponent()**: Examines volume hierarchy to determine if current step is within nucleus-related volumes

### Parameter File Changes

**Scorer Configuration:**
```
s:Sc/DNADamageScorer/Quantity = "MyCellNucleusDNADamageSBS"    # Use new scorer class
s:Sc/DNADamageScorer/Component = "Cell"                        # Target Cell component instead of Nucleus
```

**Parameter Mapping:**
All nucleus-related parameters use the `Ge/Cell/Nucleus...` prefix structure:
- `d:Sc/DNADamageScorer/ScoringRadius = Ge/Cell/NucleusNucleusRadius um`
- `d:Sc/DNADamageScorer/ImageXMinPosition = 0 um - Ge/Cell/NucleusNucleusRadius`
- etc.

## How It Works

### Volume Hierarchy
```
World
├── Cell (TsMyCellWithNPs)
│   ├── Nucleus (TsNucleus subcomponent)
│   │   ├── DNA volumes...
│   └── Nanoparticles...
```

### Scoring Process
1. **Step occurs in simulation** → Any volume within Cell component
2. **ProcessHits() called** → New scorer's ProcessHits method
3. **Volume check performed** → IsInNucleusSubcomponent() examines hierarchy
4. **If in nucleus** → Calls parent TsScoreDNADamageSBSNucleus::ProcessHits()
5. **If not in nucleus** → Returns false, no scoring occurs

### Volume Detection Logic
The scorer identifies nucleus volumes by:
- Checking current volume name for "Nucleus" substring
- Traversing parent volumes in touchable hierarchy
- Matching any volume containing "Nucleus" in the name

## Benefits of This Approach

1. **Full DNA Damage Functionality**: Inherits complete DNA damage scoring from proven Phase3 implementation
2. **Component Integration**: Works seamlessly with TsMyCellWithNPs class structure
3. **Parameter Compatibility**: Uses existing parameter file structure from Phase3
4. **Selective Scoring**: Only scores hits within nucleus subcomponent, ignoring other cell parts
5. **Maintainability**: Minimal custom code, relies on well-tested parent class

## Usage Instructions

### 1. Include the New Scorer
Ensure `TsMyCellNucleusDNADamageSBS.hh` and `.cc` files are in your TOPAS extensions directory.

### 2. Configure Parameters
In your parameter file:
```
# Use new scorer targeting Cell component
s:Sc/DNADamageScorer/Quantity = "MyCellNucleusDNADamageSBS"
s:Sc/DNADamageScorer/Component = "Cell"

# Include standard DNA scorer parameters
includeFile = supportFiles/DNAScorerStepByStep.txt

# Map all nucleus parameters to Cell/Nucleus prefix
d:Sc/DNADamageScorer/ScoringRadius = Ge/Cell/NucleusNucleusRadius um
# ... other parameters ...
```

### 3. Verify Nucleus Creation
Ensure your TsMyCellWithNPs component has nucleus parameters defined:
```
# Nucleus parameters
d:Ge/Cell/NucleusNucleusRadius = 4.65 um
s:Ge/Cell/NucleusDNAModel = "Sphere"
# ... other nucleus parameters ...
```

## Testing and Validation

### Verify Correct Operation
1. **Check nucleus creation**: Ensure TsMyCellWithNPs creates nucleus subcomponent
2. **Monitor scoring output**: Verify DNA damage events are recorded
3. **Volume filtering**: Confirm scoring only occurs in nucleus regions
4. **Parameter validation**: Check all nucleus parameters are properly read

### Expected Output
- DNA damage SDD files with chromosome and base pair information
- Scoring limited to nucleus subcomponent volumes only
- Full DNA damage analysis capabilities (DSB, SSB, foci, etc.)

## Troubleshooting

### Common Issues
1. **No DNA damage scored**: Check nucleus subcomponent creation in TsMyCellWithNPs
2. **Scorer not found**: Verify TsMyCellNucleusDNADamageSBS files are compiled
3. **Parameter errors**: Ensure all Ge/Cell/Nucleus... parameters are defined
4. **Volume detection fails**: Check nucleus volume naming convention

### Debug Steps
1. Enable TOPAS geometry visualization to verify nucleus creation
2. Add debug output to IsInNucleusSubcomponent() method
3. Check parameter file for correct nucleus parameter mapping
4. Verify all required support files exist (Geoinfo.txt, etc.)

## Required Support Files

Ensure these files are available in the `supportFiles/` directory:
- `DNAScorerStepByStep.txt`: Defines the DNA damage scorer base configuration
- `Geoinfo.txt`: Geometry information for the nucleus
- `CopyNoTable.txt`: Copy number table for voxels inside nucleus
- `signedCHVoxel.txt`: Chromosome voxel mapping file
- `HilbertPoints_iteration1.dat`: Hilbert curve points for DNA arrangement

## Output Files

The scorer will generate:
- `DNADamage_Phase2.phsp`: DNA damage events and locations
- `DNADamage_Phase2_summary.txt`: Summary of DNA damage statistics

## Conclusion

The `TsMyCellNucleusDNADamageSBS` scorer provides a robust solution for integrating DNA damage scoring into the TsMyCellWithNPs simulation framework. By leveraging inheritance and volume hierarchy checking, it maintains full compatibility with existing DNA damage analysis tools while working seamlessly with the integrated cell-nucleus-nanoparticle geometry.

This approach enables:
- **Unified simulations**: Combines cell geometry, nanoparticles, and DNA damage in a single Phase2 simulation
- **Enhanced realism**: DNA damage is scored in the presence of nanoparticles
- **Full functionality**: All Phase3 DNA damage analysis capabilities are preserved
- **Easy maintenance**: Minimal custom code, relies on proven base implementation
- `Geoinfo.txt`: Geometry information for the nucleus
- `CopyNoTable.txt`: Copy number table for voxels inside nucleus
- `signedCHVoxel.txt`: Chromosome voxel mapping file
- `HilbertPoints_iteration1.dat`: Hilbert curve points for DNA arrangement

## Output Files

The scorer will generate:
- `DNADamage_Phase2.phsp`: DNA damage events and locations
- `DNADamage_Phase2_summary.txt`: Summary of DNA damage statistics

## Benefits of This Approach

1. **Unified Simulation**: Combines cell geometry, nanoparticles, and detailed DNA damage scoring in a single Phase2 simulation
2. **Efficiency**: Eliminates the need for separate Phase3 simulations for DNA damage analysis
3. **Context**: DNA damage is scored in the presence of nanoparticles, providing more realistic results
4. **Consistency**: Uses the same nucleus geometry and parameters throughout the simulation chain

## Usage Notes

- Ensure the TsScoreDNADamageSBSNucleus extension is compiled and available
- The nucleus must have DNA structure (histones, bases, backbones) defined for the scorer to work properly
- Monitor memory usage as detailed DNA structure can be memory-intensive
- Consider adjusting `NumberOfHistoriesInRun` based on statistical requirements
