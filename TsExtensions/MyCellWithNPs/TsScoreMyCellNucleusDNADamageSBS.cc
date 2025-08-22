// Scorer for MyCellNucleusDNADamageSBS
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

#include "TsScoreMyCellNucleusDNADamageSBS.hh"
#include "G4TouchableHistory.hh"
#include "G4VPhysicalVolume.hh"
#include "G4Step.hh"

TsScoreMyCellNucleusDNADamageSBS::TsScoreMyCellNucleusDNADamageSBS(TsParameterManager* pM, TsMaterialManager* mM, TsGeometryManager* gM, TsScoringManager* scM, TsExtensionManager* eM,
		G4String scorerName, G4String quantity, G4String outFileName, G4bool isSubScorer)
		: TsScoreDNADamageSBSNucleus(pM, mM, gM, scM, eM, scorerName, quantity, outFileName, isSubScorer)
{
	// Constructor inherits all functionality from parent class
	// Parent class handles all the DNA damage scoring logic
	G4cout << "TsScoreMyCellNucleusDNADamageSBS: Initialized DNA damage scorer for Cell nucleus subcomponent" << G4endl;
}

TsScoreMyCellNucleusDNADamageSBS::~TsScoreMyCellNucleusDNADamageSBS() 
{
	// Destructor handled by parent class
}

G4bool TsScoreMyCellNucleusDNADamageSBS::ProcessHits(G4Step* aStep, G4TouchableHistory* ROhist)
{
	// First check if the step is in the nucleus subcomponent
	if (!IsInNucleusSubcomponent(aStep)) {
		return false; // Skip scoring if not in nucleus
	}

	// If in nucleus, call the parent class ProcessHits method
	// This handles all the DNA damage scoring logic
	return TsScoreDNADamageSBSNucleus::ProcessHits(aStep, ROhist);
}

G4bool TsScoreMyCellNucleusDNADamageSBS::IsInNucleusSubcomponent(G4Step* aStep)
{
	// Get the touchable to access the volume hierarchy
	G4TouchableHistory* touchable = (G4TouchableHistory*)(aStep->GetPreStepPoint()->GetTouchable());
	
	if (!touchable) {
		return false;
	}

	// Get the current volume name
	G4String currentVolumeName = touchable->GetVolume()->GetName();
	
	// Check if we're in a nucleus-related volume
	// The nucleus subcomponent volumes should contain "Nucleus" in their name
	if (currentVolumeName.contains("Nucleus")) {
		return true;
	}

	// Also check parent volumes in the hierarchy
	G4int depth = touchable->GetHistoryDepth();
	for (G4int i = 0; i <= depth; i++) {
		G4VPhysicalVolume* volume = touchable->GetVolume(i);
		if (volume && volume->GetName().contains("Nucleus")) {
			return true;
		}
	}

	return false;
}
