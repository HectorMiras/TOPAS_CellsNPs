//
// ********************************************************************
// *																  *
// * This file is part of the TOPAS-nBio extensions to the			  *
// *   TOPAS Simulation Toolkit.									  *
// * The TOPAS-nBio extensions are freely available under the license *
// *   agreement set forth at: https://topas-nbio.readthedocs.io/	  *
// *																  *
// ********************************************************************
//
// Custom DNA damage scorer for TsMyCellWithNPs nucleus subcomponent
// Inherits from TsScoreDNADamageSBSNucleus but targets Cell/Nucleus instead of standalone Nucleus

#ifndef TsScoreMyCellNucleusDNADamageSBS_hh
#define TsScoreMyCellNucleusDNADamageSBS_hh

#include "TsScoreDNADamageSBSNucleus.hh"

class TsScoreMyCellNucleusDNADamageSBS : public TsScoreDNADamageSBSNucleus {
public:
    TsScoreMyCellNucleusDNADamageSBS(TsParameterManager*, TsMaterialManager*, TsGeometryManager*,
                                TsScoringManager*, TsExtensionManager*,
                                G4String scorerName, G4String quantity,
                                G4String outFileName, G4bool isSubScorer);
    ~TsScoreMyCellNucleusDNADamageSBS() override;
    G4bool ProcessHits(G4Step*, G4TouchableHistory*) override;

private:
    G4bool IsInNucleusSubcomponent(G4Step*);
};
#endif
