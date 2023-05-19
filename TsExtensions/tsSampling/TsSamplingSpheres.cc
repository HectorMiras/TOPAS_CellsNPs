// Component for TsSamplingSpheres
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

#include <iostream>
#include <fstream>
#include "TsSamplingSpheres.hh"

#include "TsParameterManager.hh"
#include "G4VPhysicalVolume.hh"

#include "G4Orb.hh"
#include "G4Ellipsoid.hh"
#include "G4LogicalVolume.hh"
#include "G4SystemOfUnits.hh"
#include "G4PhysicalConstants.hh"
#include "Randomize.hh"

TsSamplingSpheres::TsSamplingSpheres(TsParameterManager* pM, TsExtensionManager* eM, TsMaterialManager* mM, 
                                     TsGeometryManager* gM, TsVGeometryComponent* parentComponent,
                                     G4VPhysicalVolume* parentVolume, G4String& name)
                                    :TsVGeometryComponent(pM, eM, mM, gM, parentComponent, parentVolume, name)
{
    ResolveParameters();
}


TsSamplingSpheres::~TsSamplingSpheres()
{;}

void TsSamplingSpheres::ResolveParameters() {

    if (fPm->ParameterExists(GetFullParmName("ParentRmax")))
        fParentRmax = fPm->GetDoubleParameter(GetFullParmName("ParentRmax"), "Length");
    if (fPm->ParameterExists(GetFullParmName("ParentRmin")))
        fParentRmin = fPm->GetDoubleParameter(GetFullParmName("ParentRmin"), "Length");
    else {fParentRmin=0*um;}; 
        // fMaterialSubSphere = materialName;
    if (fPm->ParameterExists(GetFullParmName("MaterialSubSpheres")))
        fMaterialSubSphere = fPm->GetStringParameter(GetFullParmName("MaterialSubSpheres")); 
    if (fPm->ParameterExists(GetFullParmName("Rmax")))
        fRmax = fPm->GetDoubleParameter(GetFullParmName("Rmax"), "Length");
    if (fPm->ParameterExists(GetFullParmName("Rmin")))
        fRmin = fPm->GetDoubleParameter(GetFullParmName("Rmin"), "Length");
    else {fRmin=0*um;}
    if (fPm->ParameterExists(GetFullParmName("Phi")))
        fPhi = fPm->GetDoubleParameter(GetFullParmName("Phi"), "Angle");
    else{fPhi=360*deg;};
    if (fPm->ParameterExists(GetFullParmName("Theta")))
        fTheta = fPm->GetDoubleParameter(GetFullParmName("Theta"), "Angle");
    else{fTheta=180*deg;};
    if (fPm->ParameterExists(GetFullParmName("NoCopies")))
        fNoCopies = fPm->GetIntegerParameter(GetFullParmName("NoCopies"));
    fPositionsFileName = "";
    if (fPm->ParameterExists(GetFullParmName("PositionsFile")))
        fPositionsFileName = fPm->GetStringParameter(GetFullParmName("PositionsFile")); 
    
    
}


G4VPhysicalVolume* TsSamplingSpheres::Construct()
{
	BeginConstruction();


    G4VSolid* ParentSphere = new G4Sphere("Sphere",
                                          fParentRmin,
                                          fParentRmax,
                                          0*deg,
                                          360*deg,
                                          0*deg,
                                          180*deg
                                          );



    fEnvelopeLog = CreateLogicalVolume(ParentSphere);
    fEnvelopePhys = CreatePhysicalVolume(fEnvelopeLog);


    G4Sphere* SubSphere = new G4Sphere("Sphere",
                                        fRmin,
                                        fRmax,
                                        0*deg,
                                        fPhi,
                                        0*deg,
                                        fTheta
                                        );

    G4LogicalVolume* lSubSphere = CreateLogicalVolume("SubSphere", fMaterialSubSphere, SubSphere);
    // SamplePositions();
    TsSamplingSpheres::PositionsFromFile(fPositionsFileName);

    param = new TsSpheresParameterizations(fPm);
    param->SetPositions(fPosX_taken, fPosY_taken, fPosZ_taken); 


    CreatePhysicalVolume("SubSphere", lSubSphere, fEnvelopePhys, kUndefined, fNoCopies, param);

    InstantiateChildren(fEnvelopePhys);
    
    return fEnvelopePhys;

}

void TsSamplingSpheres::SamplePositions(){
    G4double RSamplmax = fParentRmax-fRmax;
        G4double RSamplmin = fParentRmin+fRmax;

        G4double r = RSamplmin + cbrt(G4UniformRand())*(RSamplmax-RSamplmin);
        G4double theta = 2 * pi * G4UniformRand() - pi; // Uniform on [-pi, pi]
        G4double phi = 4*pi * G4UniformRand() - 2*pi;
        fPosX = r*std::sin(phi)*std::sin(theta);
        fPosY = r*std::sin(phi)*std::cos(theta);
        fPosZ = r*std::cos(phi);
        fPosX_taken.push_back(fPosX);
        fPosY_taken.push_back(fPosY);
        fPosZ_taken.push_back(fPosZ);

        G4bool overlap;
        G4int n=0;
        while (n<fNoCopies){

            r =  RSamplmin + cbrt(G4UniformRand())*(RSamplmax-RSamplmin); 
            theta = std::acos(2*G4UniformRand()-1); // Uniform on [-pi, pi]
            phi = 2*pi * G4UniformRand()-pi;
            fPosX = r*std::sin(theta)*std::cos(phi);
            fPosY = r*std::sin(theta)*std::sin(phi);
            fPosZ = r*std::cos(theta);
            overlap = false;
            for (int k=0 ; k<fPosX_taken.size(); k++){
                disX = fPosX-fPosX_taken[k];
                disY = fPosY-fPosY_taken[k];
                disZ = fPosZ-fPosZ_taken[k];
                dis = std::pow(disX,2) + std::pow(disY,2) + std::pow(disZ,2);
                dis = std::sqrt(dis);
                if (dis < 2*fRmax){overlap=true;};
            }
            if (overlap==false){
                fPosX_taken.push_back(fPosX);
                fPosY_taken.push_back(fPosY);
                fPosZ_taken.push_back(fPosZ);
                n++;
            } else {continue;}
        }

}


void TsSamplingSpheres::PositionsFromFile(G4String FileName){

    std::ifstream MyReadFile(FileName);
    G4String myText;
    // Use a while loop together with the getline() function to read the file line by line
    while(std::getline (MyReadFile, myText)){
    G4double col1, col2, col3;
    std::istringstream ss(myText);
    // ss >> col1 >> col2 >> col3;
    // G4cout << col1 << "   " << col2 << "   " << col3 << G4endl;
    if (ss >> col1) {
        fPosX_taken.push_back(col1);}
    if (ss >> col2) {
        fPosY_taken.push_back(col2);}
    if (ss >> col3) {
        fPosZ_taken.push_back(col3);
    }
}
};