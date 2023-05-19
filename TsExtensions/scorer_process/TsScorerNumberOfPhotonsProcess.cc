// Scorer for NumberOfPhotonsProcess
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
//Tuple scorer for scoring events deposited in the cell organelles

#include "TsScorerNumberOfPhotonsProcess.hh"

#include "G4SystemOfUnits.hh"

TsScorerNumberOfPhotonsProcess::TsScorerNumberOfPhotonsProcess(TsParameterManager* pM, TsMaterialManager* mM, TsGeometryManager* gM, TsScoringManager* scM, TsExtensionManager* eM,
                                 G4String scorerName, G4String quantity, G4String outFileName, G4bool isSubScorer)
: TsVNtupleScorer(pM, mM, gM, scM, eM, scorerName, quantity, outFileName, isSubScorer)
{
    TsScorerNumberOfPhotonsProcess::SetParameters();
    
    fNtuple->RegisterColumnI(&fNumberPhotoelectric, "Number of Photoelectric");
    fNtuple->RegisterColumnF(&fDepositedEnergyPH, "Edep photoelectric", "keV");

    fNtuple->RegisterColumnI(&fNumberCompton, "Number of Compton");
    fNtuple->RegisterColumnF(&fDepositedEnergyCO, "Edep Compton", "keV");

    fNtuple->RegisterColumnI(&fNumberPairProduction, "Number of PairProduction");
    fNtuple->RegisterColumnF(&fDepositedEnergyPP, "Edep Pair Production", "keV");

}

void TsScorerNumberOfPhotonsProcess::SetParameters(){

    if (fPm->ParameterExists(GetFullParmName("Component")))
            fSolid  = fPm->GetStringParameter(GetFullParmName("Component")); 

}


TsScorerNumberOfPhotonsProcess::~TsScorerNumberOfPhotonsProcess() {;}


G4bool TsScorerNumberOfPhotonsProcess::ProcessHits(G4Step* aStep, G4TouchableHistory*)
{
   ResolveSolid(aStep);

   G4Track* aTrack = aStep->GetTrack();

   G4TouchableHistory* touchable = (G4TouchableHistory*)(aStep->GetPreStepPoint()->GetTouchable());
   G4String PreSolidName = touchable->GetVolume(0)->GetName();
   fParticleTypeName = aTrack->GetParticleDefinition()->GetParticleName();

   if (PreSolidName == fSolid && fParticleTypeName=="gamma")
   {    

    if (aStep->GetPostStepPoint()->GetProcessDefinedStep())
        fProcessName = aStep->GetPostStepPoint()->GetProcessDefinedStep()->GetProcessName();
    fEnergy = aStep->GetTotalEnergyDeposit();

    if (fProcessName=="phot"){ 
        fNumberPhotoelectric=+1;
        fDepositedEnergyPH=+fEnergy;
    } else if (fProcessName=="compt"){
        fNumberCompton=+1;
        fDepositedEnergyCO-+fEnergy;
    } else if (fProcessName=="pairproduction"){
        fNumberPairProduction=+1;
        fDepositedEnergyPP+=fEnergy;
    } else { ;};


   } 


   return false;
}

void TsScorerNumberOfPhotonsProcess::AccumulateEvent()
{   
        fNtuple->Fill();
        fDepositedEnergyPH = 0;
        fDepositedEnergyCO = 0;
        fDepositedEnergyPP = 0;
        fNumberPhotoelectric = 0;
        fNumberCompton = 0;
        fNumberPairProduction = 0;

}
