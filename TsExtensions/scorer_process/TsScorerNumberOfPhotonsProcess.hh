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

#ifndef TsScorerNumberOfPhotonsProcess_hh
#define TsScorerNumberOfPhotonsProcess_hh

#include "TsScorerNumberOfPhotonsProcess.hh"
#include "TsVNtupleScorer.hh"
#include "G4LogicalVolumeStore.hh"
#include "G4PhysicalVolumeStore.hh"

#include "G4VProcess.hh"


class TsScorerNumberOfPhotonsProcess : public TsVNtupleScorer
{
public:
    TsScorerNumberOfPhotonsProcess(TsParameterManager* pM, TsMaterialManager* mM, TsGeometryManager* gM, TsScoringManager* scM, TsExtensionManager* eM,
                G4String scorerName, G4String quantity, G4String outFileName, G4bool isSubScorer);
    
    virtual ~TsScorerNumberOfPhotonsProcess();

    G4bool ProcessHits(G4Step*,G4TouchableHistory*);
    void AccumulateEvent();
    void SetParameters();
    

    
protected:
    // Output variables
    G4float  fEnergy;
    G4float  fDepositedEnergyPH;
    G4float  fDepositedEnergyCO;
    G4float  fDepositedEnergyPP;
    G4String fParticleTypeName;
    G4String fProcessName;

    G4int    fNumberPhotoelectric;
    G4int    fNumberCompton;
    G4int    fNumberPairProduction;


    G4String fSolid;

};
#endif
