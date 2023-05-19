//
// ********************************************************************
// *                                                                  *
// * This file is part of the TOPAS-nBio extensions to the            *
// *   TOPAS Simulation Toolkit.                                      *
// * The TOPAS-nBio extensions are freely available under the license *
// *   agreement set forth at: https://topas-nbio.readthedocs.io/     *
// *                                                                  *
// ********************************************************************
//

#ifndef TsSamplingSpheres_hh
#define TsSamplingSpheres_hh

#include "TsVGeometryComponent.hh"
#include "G4VPVParameterisation.hh"
#include "G4PVParameterised.hh"
#include "G4NistManager.hh"
#include "TsSpheresParameterizations.hh"


class TsSamplingSpheres : public TsVGeometryComponent
{    
public:
	TsSamplingSpheres(TsParameterManager* pM, TsExtensionManager* eM, TsMaterialManager* mM, TsGeometryManager* gM,
				  TsVGeometryComponent* parentComponent, G4VPhysicalVolume* parentVolume, G4String& name);
	~TsSamplingSpheres();
	
	G4VPhysicalVolume* Construct();
	void SamplePositions();
    void ResolveParameters();
    void PositionsFromFile(G4String FileName);

 //    G4Material* ComputeMaterial(const G4int repNo, G4VPhysicalVolume* pvol, const G4VTouchable* parent);
	// void ComputeTransformation(const G4int copyNo, G4VPhysicalVolume* pvol) const;
	// void ComputeDimensions(G4Sphere& sphere, const G4int copyNo, const G4VPhysicalVolume*);
    
private:

	// Defined by user:
	G4double fParentRmax;
	G4double fParentRmin;
	G4double fRmin;
	G4double fRmax;
	G4double fPhi;
	G4double fTheta;
	G4int fNoCopies;
	G4String fMaterialSubSphere;
	G4String fPositionsFileName;


	// Used to placing
	G4double fPosX;
	G4double fPosY;
	G4double fPosZ;
	std::vector<G4double> fPosX_taken;
	std::vector<G4double> fPosY_taken;
	std::vector<G4double> fPosZ_taken;
	G4double disX;
	G4double disY;
	G4double disZ;
	G4double dis;
	TsSpheresParameterizations* param;


	// G4LogicalVolume fEnvelopeLog;
	// G4VPhysicalVolume fEnvelopePhys;

};



#endif
