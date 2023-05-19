// ******************************************************************
// *
// *
// * File included as an extension for TOPAS
// * Authors: Alejandro Bertolet <abertoletreina@mgh.harvard.edu>,
// *
// *
// ******************************************************************

#ifndef TsParameterizationDistributed_hh
#define TsParameterizationDistributed_hh

#include "G4VPVParameterisation.hh"
#include "G4ThreeVector.hh"
#include "G4Orb.hh"
#include "G4VPhysicalVolume.hh"

class TsParameterizationDistributed : public G4VPVParameterisation
{
public:
	TsParameterizationDistributed(G4double radius, std::vector<G4ThreeVector> positionList);
	virtual ~TsParameterizationDistributed();

	G4VSolid* ComputeSolid(const G4int copyNo, G4VPhysicalVolume* );
	void ComputeTransformation(const G4int, G4VPhysicalVolume*) const;

private:
	G4double fRadius;
	std::vector<G4ThreeVector> fPositionList;
};

#endif
