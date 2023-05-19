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

#ifndef TsScorerTrackingProcess_hh
#define TsScorerTrackingProcess_hh

#include "TsScorerTrackingProcess.hh"
#include "TsVNtupleScorer.hh"
#include "G4LogicalVolumeStore.hh"
#include "G4PhysicalVolumeStore.hh"

#include "G4VProcess.hh"


class TsScorerTrackingProcess : public TsVNtupleScorer
{
public:
    TsScorerTrackingProcess(TsParameterManager* pM, TsMaterialManager* mM, TsGeometryManager* gM, TsScoringManager* scM, TsExtensionManager* eM,
                G4String scorerName, G4String quantity, G4String outFileName, G4bool isSubScorer);
    
    virtual ~TsScorerTrackingProcess();

    G4bool ProcessHits(G4Step*,G4TouchableHistory*);
    void SetParameters();
    

    
protected:
    // Output variables
    G4float fDepositedEnergy;
    G4String fParticleTypeName;
    G4String fProcessName;

    G4String fSolid;

};
#endif
