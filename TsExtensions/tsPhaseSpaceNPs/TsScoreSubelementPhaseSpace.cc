#include "TsScoreSubelementPhaseSpace.hh"
#include "TsDistributedComponents.hh"

// Constructor
TsScoreSubelementPhaseSpace::TsScoreSubelementPhaseSpace(const G4String& name, TsParameterManager* pM, TsComponent* parent)
    : TsScorePhaseSpace(name, pM, parent)
{
}

// Destructor
TsScoreSubelementPhaseSpace::~TsScoreSubelementPhaseSpace()
{
}

void TsScoreSubelementPhaseSpace::UserHookForParticleIn(const G4Track* aTrack)
{
    // Get the distributed component and its subelement the particle is in
    TsDistributedComponents* distComponent = dynamic_cast<TsDistributedComponents*>(fComponent);
    if (!distComponent) {
        G4Exception("TsScoreSubelementPhaseSpace::UserHookForParticleIn", "InvalidComponent",
                    FatalException, "The scored component is not of type TsDistributedComponents.");
    }

    G4int subelementID = distComponent->GetSubelementID(aTrack->GetPosition());
    if (subelementID >= 0) {
        // Set subelement ID as the fRunID, which will be saved in the phase space data
        SetRunID(subelementID);
        // Call the base class method to fill the phase space data
        TsScorePhaseSpace::UserHookForParticleIn(aTrack);
    }
}

void TsScoreSubelementPhaseSpace::UserHookForParticleOut(const G4Track* aTrack)
{
    // Get the distributed component and its subelement the particle is in
    TsDistributedComponents* distComponent = dynamic_cast<TsDistributedComponents*>(fComponent);
    if (!distComponent) {
        G4Exception("TsScoreSubelementPhaseSpace::UserHookForParticleOut", "InvalidComponent",
                    FatalException, "The scored component is not of type TsDistributedComponents.");
    }

    G4int subelementID = distComponent->GetSubelementID(aTrack->GetPosition());
    if (subelementID >= 0) {
        // Set subelement ID as the fRunID, which will be saved in the phase space data
        SetRunID(subelementID);
        // Call the base class method to fill the phase space data
        TsScorePhaseSpace::UserHookForParticleOut(aTrack);
    }
}
