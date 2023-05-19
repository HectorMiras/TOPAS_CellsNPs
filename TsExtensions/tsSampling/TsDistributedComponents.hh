//
// ******************************************************************
// *
// *
// * File included as an extension for TOPAS
// * Authors: Alejandro Bertolet <abertoletreina@mgh.harvard.edu>,
// *
// *
// ******************************************************************

#ifndef TsDistributedComponents_hh
#define TsDistributedComponents_hh

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

class TsDistributedComponents : public TsVGeometryComponent
{
public:
	TsDistributedComponents(TsParameterManager* pM, TsExtensionManager* eM, TsMaterialManager* mM, TsGeometryManager* gM,
			  TsVGeometryComponent* parentComponent, G4VPhysicalVolume* parentVolume, G4String& name);
	~TsDistributedComponents();

	G4VPhysicalVolume* Construct();
	std::vector<G4ThreeVector> ReadPositionsFile();

private:
	TsParameterizationDistributed* fParam;

	G4double fComponentRadius;
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
};

#endif
