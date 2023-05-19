#ifndef TsScoreSubelementPhaseSpace_hh
#define TsScoreSubelementPhaseSpace_hh

#include "TsScorePhaseSpace.hh"

class TsDistributedComponents;

class TsScoreSubelementPhaseSpace : public TsScorePhaseSpace
{
public:
    TsScoreSubelementPhaseSpace(const G4String& name, TsParameterManager* pM, TsComponent* parent);
    virtual ~TsScoreSubelementPhaseSpace();

    virtual void UserHookForParticleIn(const G4Track* aTrack) override;
    virtual void UserHookForParticleOut(const G4Track* aTrack) override;

private:
    // Not implemented
    TsScoreSubelementPhaseSpace();
    TsScoreSubelementPhaseSpace(const TsScoreSubelementPhaseSpace&);
    TsScoreSubelementPhaseSpace& operator=(const TsScoreSubelementPhaseSpace&);
};

#endif // TsScoreSubelementPhaseSpace_hh
