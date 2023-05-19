// Extra Class for TsNucleus
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
// Author: Hongyu Zhu
// Created date: 12/07/2018
// Last edit   : 07/08/2019 by Alexander Klapproth

#include "TsSpheresParameterizations.hh"
#include "G4SystemOfUnits.hh"

#include "G4NistManager.hh"
#include "G4Material.hh"
#include "G4Box.hh"
#include "G4Orb.hh"
#include "TsParameterManager.hh"
#include "G4PVPlacement.hh"
#include "G4LogicalVolume.hh"


TsSpheresParameterizations::TsSpheresParameterizations(TsParameterManager* pM)
    : G4VPVParameterisation(), fPm(pM)
{}

TsSpheresParameterizations::~TsSpheresParameterizations()
{}

void TsSpheresParameterizations::ComputeTransformation(const G4int copyNo, G4VPhysicalVolume* physVol) const
{
  G4ThreeVector trans(fPosX_trans[copyNo]*nm, fPosY_trans[copyNo]*nm, fPosZ_trans[copyNo]*nm);
  physVol->SetTranslation(trans);
}


void TsSpheresParameterizations::SetPositions(std::vector<G4double> fPosX_taken, 
                                              std::vector<G4double> fPosY_taken,
                                              std::vector<G4double> fPosZ_taken)
{
  fPosX_trans = fPosX_taken;
  fPosY_trans = fPosY_taken;
  fPosZ_trans = fPosZ_taken;
}

void TsSpheresParameterizations::SetSphereParameters( G4double Rmin, G4double Rmax, G4double Phi, G4double Theta )
{
    fRmin = Rmin;
    fRmax = Rmax;
    fPhi = Phi;
    fTheta = Theta;
}

void TsSpheresParameterizations::SetMaterial(G4Material* mat)
{
  fMaterialSubSphere = mat->GetName();

}
