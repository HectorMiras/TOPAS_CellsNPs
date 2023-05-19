//
// ********************************************************************
// *                                                                  *
// * This file was obtained from Topas MC Inc                         *
// * under the license agreement set forth at                         *
// * http://www.topasmc.org/registration                              *
// * Any use of this file constitutes full acceptance                 *
// * of this TOPAS MC license agreement.                              *
// *                                                                  *
// ********************************************************************
//

#ifndef TsScoreProcesses_hh
#define TsScoreProcesses_hh

#include "TsVNtupleScorer.hh"
#include "G4PhysicsModelCatalog.hh"
#include "G4EmCalculator.hh"

class TsScoreProcesses : public TsVNtupleScorer
{
public:
	TsScoreProcesses(TsParameterManager* pM, TsMaterialManager* mM, TsGeometryManager* gM, TsScoringManager* scM, TsExtensionManager* eM,
						 G4String scorerName, G4String quantity, G4String outFileName, G4bool isSubScorer);

	virtual ~TsScoreProcesses();

	G4bool ProcessHits(G4Step*,G4TouchableHistory*);
	virtual void UserHookForEndOfRun();
	void AbsorbResultsFromWorkerScorer(TsVScorer*);
	void AccumulateEvent();

private:
	std::vector<std::pair<G4String, G4String>> fUniqueProcesses;

	G4EmCalculator fEmCalculator;

	G4bool fDoseToWater;

	G4double fDose;
	G4int fIntPhoto;
	G4int fIntMSc;
	G4int fInteIoni;
	G4int fNAuger;

	std::vector<G4int> fTrackIDsForAugere;

	G4int fPhotoGamma;
	G4int fComptGamma;
	G4int fPhotoAuger;
	G4int fComptAuger;
	G4int fPixeGamma;
	G4int fPixeAuger;
	G4int fElectronDNAGamma;
	G4int fElectronDNAAuger;
	G4int fProtonDNAGamma;
	G4int fProtonDNAAuger;
	G4int fHydrogenDNAGamma;
	G4int fHydrogenDNAAuger;
	G4int fAlphaDNAGamma;
	G4int fAlphaDNAAuger;
	G4int fAlphaPlusDNAGamma;
	G4int fAlphaPlusDNAAuger;
	G4int fHeliumDNAGamma;
	G4int fHeliumDNAAuger;
	G4int fGenericIonDNAGamma;
	G4int fGenericIonDNAAuger;
};
#endif
