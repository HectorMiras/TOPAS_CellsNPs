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

#ifndef TsSpheresParameterizations_hh
#define TsSpheresParameterizations_hh

#include "G4VPVParameterisation.hh"
#include "G4ThreeVector.hh"
#include "G4UnitsTable.hh"
#include "G4SystemOfUnits.hh"
#include "G4VPhysicalVolume.hh"
#include "G4LogicalVolume.hh"
#include "G4VSolid.hh"
#include "G4VisAttributes.hh"
#include "TsVGeometryComponent.hh"
#include "TsParameterManager.hh"

#include "TsSpheresParameterizations.hh"

class TsSpheresParameterizations : public G4VPVParameterisation
{
public:
    TsSpheresParameterizations(TsParameterManager*);
    virtual ~TsSpheresParameterizations();
    virtual void ComputeTransformation(const G4int copyNo, G4VPhysicalVolume* physVol) const;
    // virtual G4Material* ComputeMaterial (const G4int repNo, G4VPhysicalVolume *currentVol, const G4VTouchable *parentTouch=0) const; 
    
    void SetSphereParameters( G4double Rmin, G4double Rmax, G4double Phi, G4double Theta);
    
    void SetPositions(std::vector<G4double> fPosX_taken, std::vector<G4double> fPosY_taken, std::vector<G4double> fPosZ_taken);
    void SetMaterial(G4Material* mat);


    G4double fParentRmax;
    G4double fParentRmin;
    G4double fRmin;
    G4double fRmax;
    G4double fPhi;
    G4double fTheta;
    G4int  fNoCopies;
    G4String fMaterialSubSphere;


    std::vector<G4double> fPosX_trans;
    std::vector<G4double> fPosY_trans;
    std::vector<G4double> fPosZ_trans;
    std::vector<G4double> fPosX_taken;
    std::vector<G4double> fPosY_taken;
    std::vector<G4double> fPosZ_taken;

protected:

    std::vector<G4double> fPositions;

private:
    TsParameterManager* fPm;

};

#endif // TsSphereParametrizations