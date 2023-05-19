// Scorer for TrackingProcess
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

#include "TsScorerTrackingProcess.hh"

#include "G4SystemOfUnits.hh"

TsScorerTrackingProcess::TsScorerTrackingProcess(TsParameterManager* pM, TsMaterialManager* mM, TsGeometryManager* gM, TsScoringManager* scM, TsExtensionManager* eM,
                                 G4String scorerName, G4String quantity, G4String outFileName, G4bool isSubScorer)
: TsVNtupleScorer(pM, mM, gM, scM, eM, scorerName, quantity, outFileName, isSubScorer)
{
    TsScorerTrackingProcess::SetParameters();
    
    fNtuple->RegisterColumnS(&fParticleTypeName, "Particle Name");
    fNtuple->RegisterColumnF(&fDepositedEnergy, "Deposited Energy", "keV");
    fNtuple->RegisterColumnS(&fProcessName, "Process Name");

}

void TsScorerTrackingProcess::SetParameters(){

    if (fPm->ParameterExists(GetFullParmName("Component")))
            fSolid  = fPm->GetStringParameter(GetFullParmName("Component")); 

}


TsScorerTrackingProcess::~TsScorerTrackingProcess() {;}


G4bool TsScorerTrackingProcess::ProcessHits(G4Step* aStep, G4TouchableHistory*)
{
   ResolveSolid(aStep);

   G4Track* aTrack = aStep->GetTrack();

   G4TouchableHistory* touchable = (G4TouchableHistory*)(aStep->GetPreStepPoint()->GetTouchable());
   G4String PreSolidName = touchable->GetVolume(0)->GetName();


   if ((PreSolidName == fSolid))
   {    

    if (aStep->GetPostStepPoint()->GetProcessDefinedStep())
        fProcessName = aStep->GetPostStepPoint()->GetProcessDefinedStep()->GetProcessName();
    fParticleTypeName = aTrack->GetParticleDefinition()->GetParticleName();
    fDepositedEnergy = aStep->GetTotalEnergyDeposit();
    fNtuple->Fill();


   } 


   return false;
}

