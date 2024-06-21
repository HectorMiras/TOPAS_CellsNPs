// Extra Class for TsDistributedComponents
//
// ******************************************************************
// *
// *
// * File included as an extension for TOPAS
// * Authors: Alejandro Bertolet <abertoletreina@mgh.harvard.edu>,
// *
// *
// ******************************************************************

#include "TsParameterizationDistributed.hh"

TsParameterizationDistributed::TsParameterizationDistributed(G4double radius, std::vector<G4ThreeVector> positionList)
	: G4VPVParameterisation()
{
	fPositionList = positionList;
	fRadius = radius;
}

TsParameterizationDistributed::~TsParameterizationDistributed() { }

G4VSolid* TsParameterizationDistributed::ComputeSolid(const G4int, G4VPhysicalVolume*)
{
	G4Orb* sphere = new G4Orb("Sphere", fRadius);
	return sphere;
}


void TsParameterizationDistributed::ComputeTransformation(const G4int copyNo, G4VPhysicalVolume* physVol) const
{
	G4ThreeVector trans = fPositionList[copyNo];
	physVol->SetTranslation(trans);
}
