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
#include "G4VPhysicalVolume.hh"

class TsParameterizationDistributed : public G4VPVParameterisation
{
public:
	// Updated constructor (removed radius parameter)
	TsParameterizationDistributed(std::vector<G4ThreeVector> positionList);
	virtual ~TsParameterizationDistributed();

	// Removed ComputeSolid declaration
	void ComputeTransformation(const G4int, G4VPhysicalVolume*) const;

private:
	// Removed fRadius member
	std::vector<G4ThreeVector> fPositionList;
};

#endif