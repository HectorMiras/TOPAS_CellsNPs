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

TsParameterizationDistributed::TsParameterizationDistributed(std::vector<Nanoparticle> particles)
    : G4VPVParameterisation()
{
    fParticles = particles;
}

G4VSolid* TsParameterizationDistributed::ComputeSolid(const G4int copyNo, G4VPhysicalVolume*)
{
    G4Orb* sphere = new G4Orb("Sphere", fParticles[copyNo].radius);
    return sphere;
}



void TsParameterizationDistributed::ComputeTransformation(const G4int copyNo, G4VPhysicalVolume* physVol) const
{
    G4ThreeVector trans = fParticles[copyNo].position;
    physVol->SetTranslation(trans);
}

