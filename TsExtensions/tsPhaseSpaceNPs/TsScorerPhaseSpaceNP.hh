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

#ifndef TsScorerPhaseSpaceNP_hh
#define TsScorerPhaseSpaceNP_hh

#include "TsScorerPhaseSpaceNP.hh"
#include "TsVNtupleScorer.hh"
#include "G4LogicalVolumeStore.hh"
#include "G4PhysicalVolumeStore.hh"
#include "G4EmCalculator.hh"


#include "G4VProcess.hh"


class TsScorerPhaseSpaceNP : public TsVNtupleScorer
{
public:
    TsScorerPhaseSpaceNP(TsParameterManager* pM, TsMaterialManager* mM, TsGeometryManager* gM, TsScoringManager* scM, TsExtensionManager* eM,
                G4String scorerName, G4String quantity, G4String outFileName, G4bool isSubScorer);
    
    virtual ~TsScorerPhaseSpaceNP();

    virtual G4bool ProcessHits(G4Step*, G4TouchableHistory*);

    void AccumulateEvent();

    void AbsorbResultsFromWorkerScorer(TsVScorer* workerScorer);

    void UpdateForEndOfRun();
    

    
protected:
    void Output();
    void Clear();

    G4float fPosX;
    G4float fPosY;
    G4float fPosZ;
    G4float fCosX;
    G4float fCosY;
    G4bool fCosZIsNegative;
    G4float fEnergy;
    G4float fWeight;
    G4int fPType;
    G4int fNumberOfSequentialEmptyHistories;
    G4bool fIsEmptyHistory;
    G4bool fIsNewHistory;
    G4float fTOPASTime;
    G4float fTimeOfFlight;
    G4int fRunID;
    G4int fEventID;
    G4int fTrackID;
    G4int fParentID;
    G4float fCharge;
    G4String fCreatorProcess;
    G4float fVertexKE;
    G4float fVertexPosX;
    G4float fVertexPosY;
    G4float fVertexPosZ;
    G4float fVertexCosX;
    G4float fVertexCosY;
    G4float fVertexCosZ;
    G4int fSeedPart1;
    G4int fSeedPart2;
    G4int fSeedPart3;
    G4int fSeedPart4;
    G4float fSignedEnergy;
    int8_t fSignedPType;

    G4bool fIncludeEmptyHistoriesInSequence;
    G4bool fIncludeEmptyHistoriesAtEndOfRun;
    G4bool fIncludeEmptyHistoriesAtEndOfFile;
    G4bool fKillAfterPhaseSpace;
    G4bool fOutputToLimited;
    G4bool fIncludeTOPASTime;
    G4bool fIncludeTimeOfFlight;
    G4bool fIncludeTrackID;
    G4bool fIncludeParentID;
    G4bool fIncludeCharge;
    G4bool fIncludeCreatorProcess;
    G4bool fIncludeVertexInfo;
    G4bool fIncludeSeed;

    G4int fPrevRunID;
    G4int fPrevEventID;

    G4long fNumberOfHistoriesThatMadeItToPhaseSpace;
    std::map<G4int, G4long> fNumberOfParticles; // # of particles of each type
    std::map<G4int, G4double> fMinimumKE;  // min KE of each particle type
    std::map<G4int, G4double> fMaximumKE;  // max KE of each particle type

    // Include subcomponentIndex (copynumber)
    G4int fsubcomponentIndex;

};
#endif
