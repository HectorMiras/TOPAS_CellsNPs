//
// ******************************************************************
// *
// *
// * File included as an extension for TOPAS
// * Authors: Alejandro Bertolet <abertoletreina@mgh.harvard.edu>,
// *
// *
// ******************************************************************

#ifndef TsMyCellWithNPs_hh
#define TsMyCellWithNPs_hh

#include "TsVGeometryComponent.hh"
#include "G4PVParameterised.hh"
#include "TsParameterizationDistributed.hh"
#include "G4ThreeVector.hh"
#include "G4Orb.hh"
#include "G4Ellipsoid.hh"
#include "G4Tubs.hh"
#include "G4Box.hh"
#include "G4Material.hh"
#include "G4UnitsTable.hh"
#include "G4SystemOfUnits.hh"

class TsNucleus;
class TsMaterialManager;   // forward declarations to store pointers
class TsGeometryManager;

class TsMyCellWithNPs : public TsVGeometryComponent
{
public:
	TsMyCellWithNPs(TsParameterManager* pM, TsExtensionManager* eM, TsMaterialManager* mM, TsGeometryManager* gM,
			  TsVGeometryComponent* parentComponent, G4VPhysicalVolume* parentVolume, G4String& name);
	~TsMyCellWithNPs();

	G4VPhysicalVolume* Construct();
	std::vector<G4ThreeVector> ReadPositionsFile();
	void CreateNucleusSubcomponent();

private:
	TsParameterizationDistributed* fParam;

	// Store managers locally instead of accessing base-class private members
	TsMaterialManager* fLocalMm;
	TsGeometryManager* fLocalGm;

	G4double fComponentRadius;
	G4double fComponentRadiusMin;
	G4double fElementRadius;

	G4String fElementMaterialName;

	G4String fPositionsFileName;
	
	// Add new parameters for cylinder and box dimensions
	G4double fComponentHL;
	G4double fComponentHLX;
	G4double fComponentHLY;
	G4double fComponentHLZ;

	// Add a parameter to store the shape type
	G4String fComponentType;

	// Nucleus-related parameters
	G4bool fHasNucleus;
	TsNucleus* fNucleusComponent;
	G4String fNucleusMaterial;
	G4String fNucleusColor;
	G4String fNucleusDNAModel;
	G4double fNucleusRadius;
	G4int fNucleusHilbertCurveLayer;
	G4int fNucleusHilbertCurve3DRepeat;
	G4String fNucleusHilbertCurveFileName;
	G4String fNucleusVoxelMaterial;
	G4bool fNucleusShowDNAVoxels;
	G4String fNucleusChromatinFiberMaterial;
	G4bool fNucleusShowChromatinCylinders;
	G4String fNucleusHistoneMaterial;
	G4bool fNucleusOnlyBuildOneHistone;
	G4bool fNucleusHistoneAsScavenger;
	G4bool fNucleusAddBases;
	G4String fNucleusBase1Material;
	G4String fNucleusBase2Material;
	G4bool fNucleusAddBackbones;
	G4String fNucleusBackbone1Material;
	G4String fNucleusBackbone2Material;
	G4bool fNucleusAddHydrationShell;
	G4String fNucleusHydrationShell1Material;
	G4String fNucleusHydrationShell2Material;
};

#endif
