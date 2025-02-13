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

TsParameterizationDistributed::TsParameterizationDistributed(std::vector<G4ThreeVector> positionList)
	: G4VPVParameterisation()
{
	fPositionList = positionList;
}

TsParameterizationDistributed::~TsParameterizationDistributed() { }

void TsParameterizationDistributed::ComputeTransformation(const G4int copyNo, G4VPhysicalVolume* physVol) const
{
	physVol->SetTranslation(fPositionList[copyNo]);
}