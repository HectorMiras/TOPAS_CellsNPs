// Scorer for DoseAndProcesses
// ********************************************************************
// *                                                                  *
// * This  code  implementation is the  intellectual property  of the *
// * TOPAS collaboration.                                             *
// * Use or redistribution of this code is not permitted without the  *
// * explicit approval of the TOPAS collaboration.                    *
// * Contact: Joseph Perl, perl@slac.stanford.edu                     *
// *                                                                  *
// ********************************************************************
//

#include "TsScoreProcesses.hh"
//#include "TsSequenceManager.hh"
#include "G4VProcess.hh"
#include "G4Track.hh"
#include "G4ParticleDefinition.hh"
#include "G4Material.hh"

TsScoreProcesses::TsScoreProcesses(TsParameterManager* pM, TsMaterialManager* mM, TsGeometryManager* gM, TsScoringManager* scM, TsExtensionManager* eM,
										   G4String scorerName, G4String quantity, G4String outFileName, G4bool isSubScorer)
: TsVNtupleScorer(pM, mM, gM, scM, eM, scorerName, quantity, outFileName, isSubScorer),
  fEmCalculator()
{
	SetUnit("Gy");

	fDoseToWater = false;
	if (fPm->ParameterExists(GetFullParmName("DoseToWater")))
		fDoseToWater = fPm->GetBooleanParameter(GetFullParmName("DoseToWater"));

	fPhotoGamma = G4PhysicsModelCatalog::GetIndex("phot_fluo");
	fComptGamma = G4PhysicsModelCatalog::GetIndex("compt_fluo");
	fPhotoAuger = G4PhysicsModelCatalog::GetIndex("phot_auger");
	fComptAuger = G4PhysicsModelCatalog::GetIndex("compt_auger");
	fPixeGamma = G4PhysicsModelCatalog::GetIndex("gammaPIXE");
	fPixeAuger = G4PhysicsModelCatalog::GetIndex("e-PIXE");
	fElectronDNAGamma = G4PhysicsModelCatalog::GetIndex("e-_G4DNAIonisation_fluo");
	fElectronDNAAuger = G4PhysicsModelCatalog::GetIndex("e-_G4DNAIonisation_auger");
	fProtonDNAGamma = G4PhysicsModelCatalog::GetIndex("proton_G4DNAIonisation_fluo");
	fProtonDNAAuger = G4PhysicsModelCatalog::GetIndex("proton_G4DNAIonisation_auger");
	fHydrogenDNAGamma = G4PhysicsModelCatalog::GetIndex("hydrogen_G4DNAIonisation_fluo");
	fHydrogenDNAAuger = G4PhysicsModelCatalog::GetIndex("hydrogen_G4DNAIonisation_auger");
	fAlphaDNAGamma = G4PhysicsModelCatalog::GetIndex("alpha_G4DNAIonisation_fluo");
	fAlphaDNAAuger =G4PhysicsModelCatalog::GetIndex("alpha_G4DNAIonisation_auger");
	fAlphaPlusDNAGamma = G4PhysicsModelCatalog::GetIndex("alpha+_G4DNAIonisation_fluo");
	fAlphaPlusDNAAuger = G4PhysicsModelCatalog::GetIndex("alpha+_G4DNAIonisation_auger");
	fHeliumDNAGamma = G4PhysicsModelCatalog::GetIndex("helium_G4DNAIonisation_fluo");
	fHeliumDNAAuger = G4PhysicsModelCatalog::GetIndex("helium_G4DNAIonisation_auger");
	fGenericIonDNAGamma = G4PhysicsModelCatalog::GetIndex("GenericIon_G4DNAIonisation_fluo");
	fGenericIonDNAAuger = G4PhysicsModelCatalog::GetIndex("GenericIon_G4DNAIonisation_auger");
	G4cout << "LIST OF ID CREATIONS" << G4endl;
	G4cout << fPhotoGamma << G4endl;
	G4cout << fComptGamma << G4endl;
	G4cout << fPhotoAuger << G4endl;
	G4cout << fComptAuger << G4endl;
	G4cout << fPixeGamma << G4endl;
	G4cout << fPixeAuger << G4endl;
	G4cout << fElectronDNAGamma << G4endl;
	G4cout << fElectronDNAAuger << G4endl;
	G4cout <<  fProtonDNAGamma << G4endl;
	G4cout <<  fProtonDNAAuger << G4endl;
	G4cout <<  fHydrogenDNAGamma << G4endl;
	G4cout <<  fHydrogenDNAAuger << G4endl;
	G4cout <<  fAlphaDNAGamma << G4endl;
	G4cout <<  fAlphaDNAAuger << G4endl;
	G4cout <<  fAlphaPlusDNAGamma  << G4endl;
	G4cout <<  fAlphaPlusDNAAuger << G4endl;
	G4cout <<  fHeliumDNAGamma << G4endl;
	G4cout <<  fHeliumDNAAuger << G4endl;
	G4cout <<  fGenericIonDNAGamma << G4endl;
	G4cout <<  fGenericIonDNAAuger << G4endl;

	// Register
	fNtuple->RegisterColumnD(&fDose, "Dose", "Gy");
	fNtuple->RegisterColumnI(&fIntPhoto, "Int. Photoelectric");
	fNtuple->RegisterColumnI(&fIntMSc, "Int. MSC");
	fNtuple->RegisterColumnI(&fInteIoni, "Int. e-Ioni");
	fNtuple->RegisterColumnI(&fNAuger, "Auger e- produced");
}


TsScoreProcesses::~TsScoreProcesses() {;}


G4bool TsScoreProcesses::ProcessHits(G4Step* aStep,G4TouchableHistory*)
{
	if (!fIsActive) {
		fSkippedWhileInactive++;
		return false;
	}



	G4String processName = "Not defined";
	if (aStep->GetPostStepPoint()->GetProcessDefinedStep())
		processName = aStep->GetPostStepPoint()->GetProcessDefinedStep()->GetProcessName();
	G4String particleName = aStep->GetTrack()->GetParticleDefinition()->GetParticleName();

	G4int idx = aStep->GetTrack()->GetCreatorModelID();

	std::pair<G4String, G4String> newPair = std::make_pair(particleName, processName);

	if (fUniqueProcesses.size() == 0)
	{
		fUniqueProcesses.push_back(newPair);
	}
	if (std::find(fUniqueProcesses.begin(), fUniqueProcesses.end(), newPair) == fUniqueProcesses.end())
	{
		fUniqueProcesses.push_back(newPair);
	}

	// Get number of interactions
	if (strstr(particleName, "gamma") && strstr(processName, "phot"))
		fIntPhoto++;
	if (strstr(particleName, "e-") && strstr(processName, "eIoni"))
		fInteIoni++;
	if (strstr(particleName, "e-") && strstr(processName, "msc"))
		fIntMSc++;
	if (idx == 2 && strstr(particleName, "e-"))
	{
		G4int trackID = aStep->GetTrack()->GetTrackID();
		if (std::find(fTrackIDsForAugere.begin(), fTrackIDsForAugere.end(), trackID) == fTrackIDsForAugere.end())
		{
			fTrackIDsForAugere.push_back(trackID);
			fNAuger++;
		}
	}

	// Get dose
	G4double edep = aStep->GetTotalEnergyDeposit();
	if ( edep > 0. )
	{
		ResolveSolid(aStep);

		G4double density = aStep->GetPreStepPoint()->GetMaterial()->GetDensity();
		G4double dose = edep / (density * GetCubicVolume(aStep));
		dose *= aStep->GetPreStepPoint()->GetWeight();

		if (fDoseToWater)
		{
			G4Material* referenceMaterial = GetMaterial("G4_WATER");
			G4ParticleDefinition* particle = aStep->GetTrack()->GetDefinition();
			G4double energy = aStep->GetPreStepPoint()->GetKineticEnergy();
			if (particle->GetPDGCharge() != 0)
			{
				G4double materialStoppingPower = fEmCalculator.ComputeTotalDEDX(energy, particle, aStep->GetPreStepPoint()->GetMaterial());
				if (materialStoppingPower == 0)
				{
					//fPm->GetSequenceManager()->NoteUnscoredHit(energy, GetName());
					return false;
				}
				G4double referenceMaterialStoppingPower = fEmCalculator.ComputeTotalDEDX(energy, particle, referenceMaterial);
				dose *= (density / referenceMaterial->GetDensity()) * (referenceMaterialStoppingPower / materialStoppingPower);
			}
		}
		fDose += dose;
		return true;
	}

	return true;
}

void TsScoreProcesses::AccumulateEvent()
{
	fTrackIDsForAugere.clear();
}

void TsScoreProcesses::UserHookForEndOfRun()
{
	fNtuple->Fill();
	G4cout << "number of processes scored: " << fUniqueProcesses.size() << G4endl;
	for (const auto& pair : fUniqueProcesses)
		G4cout << "(" << pair.first << ", " << pair.second << ")" << G4endl;
}

void TsScoreProcesses::AbsorbResultsFromWorkerScorer(TsVScorer* workerScorer)
{
	TsVNtupleScorer::AbsorbResultsFromWorkerScorer(workerScorer);
	TsScoreProcesses* workerMTScorer = dynamic_cast<TsScoreProcesses*>(workerScorer);

	for(unsigned int i=0; i < workerMTScorer->fUniqueProcesses.size(); i++)
		fUniqueProcesses.push_back(workerMTScorer->fUniqueProcesses[i]);
	workerMTScorer->fUniqueProcesses.clear();

	fDose = workerMTScorer->fDose;
	fIntPhoto = workerMTScorer->fIntPhoto;
	fIntMSc = workerMTScorer->fIntMSc;
	fInteIoni = workerMTScorer->fInteIoni;
	fNAuger = workerMTScorer->fNAuger;
}
