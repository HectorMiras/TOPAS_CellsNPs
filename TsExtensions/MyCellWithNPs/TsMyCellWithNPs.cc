// Component for TsMyCellWithNPs
//
// ******************************************************************
// *
// *
// * File included as an extension for TOPAS
// * Authors: Alejandro Bertolet <abertoletreina@mgh.harvard.edu>,
// *
// *
// ******************************************************************

#include "TsMyCellWithNPs.hh"
#include "TsParameterManager.hh"
#include "TsNucleus.hh"
#include "G4UIcommand.hh"
#include "G4SubtractionSolid.hh"
#include "G4SolidStore.hh"
#include "G4Orb.hh"
#include "G4UnitsTable.hh"
#include "G4GeometryTolerance.hh"

TsMyCellWithNPs::TsMyCellWithNPs(TsParameterManager* pM, TsExtensionManager* eM, TsMaterialManager* mM, TsGeometryManager* gM,
		TsVGeometryComponent* parentComponent, G4VPhysicalVolume* parentVolume, G4String& name) :
		TsVGeometryComponent(pM, eM, mM, gM, parentComponent, parentVolume, name),
		fLocalMm(mM),
		fLocalGm(gM)
{

	auto* gt = G4GeometryTolerance::GetInstance();
	G4cout << "[GeomTol] surface=" << gt->GetSurfaceTolerance()/nm << " nm"
	       << " radial=" << gt->GetRadialTolerance()/nm << " nm"
	       << " (10*kCarTolerance=" << (10*gt->GetRadialTolerance()/nm) << " nm)"
	       << G4endl;

	fElementRadius = fPm->GetDoubleParameter(GetFullParmName("ElementRadius"), "Length");
	fElementMaterialName = fPm->GetStringParameter(GetFullParmName("ElementMaterial"));
	fPositionsFileName = fPm->GetStringParameter(GetFullParmName("PositionsFile"));
	
	fComponentType = fPm->GetStringParameter(GetFullParmName("ComponentType"));

	if (fComponentType == "G4Orb" || fComponentType == "G4Tubs") {
		fComponentRadius = fPm->GetDoubleParameter(GetFullParmName("ComponentRadius"), "Length");
	}
	if (fComponentType == "G4Sphere") {
		fComponentRadius = fPm->GetDoubleParameter(GetFullParmName("ComponentRMax"), "Length");
		fComponentRadiusMin = fPm->GetDoubleParameter(GetFullParmName("ComponentRMin"), "Length");
	}
	if (fComponentType == "G4Tubs") {
		fComponentHL = fPm->GetDoubleParameter(GetFullParmName("ComponentHL"), "Length");
	}
	if (fComponentType == "G4Box" || fComponentType == "G4Ellipsoid") {
		fComponentHLX = fPm->GetDoubleParameter(GetFullParmName("ComponentHLX"), "Length");
		fComponentHLY = fPm->GetDoubleParameter(GetFullParmName("ComponentHLY"), "Length");
		fComponentHLZ = fPm->GetDoubleParameter(GetFullParmName("ComponentHLZ"), "Length");
	}

	// Check if nucleus parameters are defined
	fHasNucleus = fPm->ParameterExists(GetFullParmName("Nucleus/Material"));
	fNucleusComponent = nullptr;
	
	if (fHasNucleus) {
		// Read nucleus parameters
		fNucleusMaterial = fPm->GetStringParameter(GetFullParmName("Nucleus/Material"));
		fNucleusColor = fPm->GetStringParameter(GetFullParmName("Nucleus/Color"));
		fNucleusDNAModel = fPm->GetStringParameter(GetFullParmName("Nucleus/DNAModel"));
		fNucleusRadius = fPm->GetDoubleParameter(GetFullParmName("Nucleus/NucleusRadius"), "Length");
		fNucleusHilbertCurveLayer = fPm->GetIntegerParameter(GetFullParmName("Nucleus/HilbertCurveLayer"));
		fNucleusHilbertCurve3DRepeat = fPm->GetIntegerParameter(GetFullParmName("Nucleus/HilbertCurve3DRepeat"));
		fNucleusHilbertCurveFileName = fPm->GetStringParameter(GetFullParmName("Nucleus/HilbertCurveFileName"));
		fNucleusVoxelMaterial = fPm->GetStringParameter(GetFullParmName("Nucleus/Voxel/Material"));
		fNucleusShowDNAVoxels = fPm->GetBooleanParameter(GetFullParmName("Nucleus/ShowDNAVoxels"));
		fNucleusChromatinFiberMaterial = fPm->GetStringParameter(GetFullParmName("Nucleus/ChromatinFiber/Material"));
		fNucleusShowChromatinCylinders = fPm->GetBooleanParameter(GetFullParmName("Nucleus/ShowChromatinCylinders"));
		fNucleusHistoneMaterial = fPm->GetStringParameter(GetFullParmName("Nucleus/Histone/Material"));
		fNucleusOnlyBuildOneHistone = fPm->GetBooleanParameter(GetFullParmName("Nucleus/OnlyBuildOneHistone"));
		fNucleusHistoneAsScavenger = fPm->GetBooleanParameter(GetFullParmName("Nucleus/HistoneAsScavenger"));
		fNucleusAddBases = fPm->GetBooleanParameter(GetFullParmName("Nucleus/AddBases"));
		fNucleusBase1Material = fPm->GetStringParameter(GetFullParmName("Nucleus/Base1/Material"));
		fNucleusBase2Material = fPm->GetStringParameter(GetFullParmName("Nucleus/Base2/Material"));
		fNucleusAddBackbones = fPm->GetBooleanParameter(GetFullParmName("Nucleus/AddBackbone"));
		fNucleusBackbone1Material = fPm->GetStringParameter(GetFullParmName("Nucleus/Backbone1/Material"));
		fNucleusBackbone2Material = fPm->GetStringParameter(GetFullParmName("Nucleus/Backbone2/Material"));
		fNucleusAddHydrationShell = fPm->GetBooleanParameter(GetFullParmName("Nucleus/AddHydrationShell"));
		fNucleusHydrationShell1Material = fPm->GetStringParameter(GetFullParmName("Nucleus/HydrationShell1/Material"));
		fNucleusHydrationShell2Material = fPm->GetStringParameter(GetFullParmName("Nucleus/HydrationShell2/Material"));
	}
}
TsMyCellWithNPs::~TsMyCellWithNPs() {
	if (fNucleusComponent) {
		delete fNucleusComponent;
	}
}

G4VPhysicalVolume* TsMyCellWithNPs::Construct()
{
    std::vector<G4ThreeVector> positionList = ReadPositionsFile();
    G4int nSubcomponents = positionList.size();
    BeginConstruction();    
    
    // Component Solid
    G4VSolid* componentSolid;
    if (fComponentType == "G4Orb") {
        componentSolid = new G4Orb(fName, fComponentRadius);
    } else if (fComponentType == "G4Sphere") {
        componentSolid = new G4Sphere(fName, fComponentRadiusMin, fComponentRadius, 0.0, 360.0 * deg, 0.0, 180.0 * deg);
	} else if (fComponentType == "G4Tubs") {
        componentSolid = new G4Tubs(fName, 0.0, fComponentRadius, fComponentHL, 0.0, 360.0 * deg);
	} else if (fComponentType == "G4Ellipsoid") {
        componentSolid = new G4Ellipsoid(fName, fComponentHLX, fComponentHLY, fComponentHLZ);
    } else if (fComponentType == "G4Box") {
        componentSolid = new G4Box(fName, fComponentHLX, fComponentHLY, fComponentHLZ);
    } else {
        G4cerr << "Error: Invalid component shape '" << fComponentType <<"'." << G4endl;
		return nullptr;
	}

    fEnvelopeLog = CreateLogicalVolume(componentSolid);
    fEnvelopePhys = CreatePhysicalVolume(fEnvelopeLog);

    // Parameterization for NPs
    fParam = new TsParameterizationDistributed(positionList);

    // Create NP container if nucleus exists: Cell minus Nucleus
    G4VPhysicalVolume* npMotherPhys = fEnvelopePhys;
    if (fHasNucleus) {
        // Subtract a spherical nucleus at the cell center
        G4VSolid* nucleusCut = new G4Orb("NucleusCut", fNucleusRadius);
        G4VSolid* npContainerSolid =
            new G4SubtractionSolid("NPContainerSolid", componentSolid, nucleusCut, nullptr, G4ThreeVector());

        // Use the same material as the cell
        G4String cellMaterial = fPm->GetStringParameter(GetFullParmName("Material"));
        G4LogicalVolume* npContainerLog =
            CreateLogicalVolume("LogNPContainer", cellMaterial, npContainerSolid);
        npMotherPhys = CreatePhysicalVolume("NPContainer", npContainerLog, fEnvelopePhys);
    }

    // Subelements (NPs) – place inside NP container (if present)
    G4String name = "SubcompSolid";
    G4VSolid* subcomponentSolid = new G4Orb(name, fElementRadius);
    G4LogicalVolume* subLogic = CreateLogicalVolume("LogSubcomponent", fElementMaterialName, subcomponentSolid);
    if (nSubcomponents > 1)
        CreatePhysicalVolume("Subcomponents", subLogic, npMotherPhys, kUndefined, nSubcomponents, fParam);
    if (nSubcomponents == 1)
        CreatePhysicalVolume("Subcomponent", subLogic, new G4RotationMatrix(), &positionList[0], npMotherPhys);

    // Create nucleus subcomponent if nucleus parameters are defined
    if (fHasNucleus) {
        CreateNucleusSubcomponent();
    }

    if (fParentVolume)
        InstantiateChildren();
    return fEnvelopePhys;
}

std::vector<G4ThreeVector> TsMyCellWithNPs::ReadPositionsFile()
{
	std::vector<G4ThreeVector> positions;

	  // Open the file for reading.
	  std::ifstream file(fPositionsFileName);
	  if (!file)
	  {
	    std::cerr << "Error: Unable to open file '" << fPositionsFileName << "'." << std::endl;
	    return positions;
	  }

	  // Read each line of the file, which should contain a 3D position in the
	  // format "x y z".
	  std::string line;
	  while (std::getline(file, line))
	  {
	    std::istringstream lineStream(line);
	    double x, y, z;
	    if (lineStream >> x >> y >> z)
	    {
	      // If the line could be parsed as a 3D position, add it to the vector.
	      positions.push_back(G4ThreeVector(x*nm, y*nm, z*nm));
	    }
	    else
	    {
	      // Otherwise, print an error message.
	      std::cerr << "Error: Invalid position '" << line << "'." << std::endl;
	    }
	  }
	  return positions;
}

void TsMyCellWithNPs::CreateNucleusSubcomponent()
{
    if (!fHasNucleus) return;

    G4String nucleusName = "Nucleus";

    // Helpers to format values
    auto Quote = [](const G4String& s) -> G4String { return "\"" + s + "\""; };
    auto QBool = [](G4bool b) -> G4String { return b ? "\"true\"" : "\"false\""; };

    // IMPORTANT: publish TsNucleus under Ge/Nucleus/... (Parent = this cell)
    auto ge = [&](const G4String& p) -> G4String { return "Ge/" + nucleusName + "/" + p; };

    // Helpers to avoid re-defining parameters that already exist
    auto Bare = [](const G4String& keyWithType) -> G4String { return keyWithType.substr(2); }; // strip "s:", "d:", ...
    auto Exists = [&](const G4String& keyWithType) -> G4bool { return fPm->ParameterExists(Bare(keyWithType)); };

    // Logging wrapper
    auto AddAndLog = [&](const G4String& key, const G4String& val) {
        if (Exists(key)) {
            G4cout << "[CreateNucleusSubcomponent] (skip, exists) " << key << G4endl;
            return;
        }
        G4cout << "[CreateNucleusSubcomponent] " << key << " = " << val << G4endl;
        fPm->AddParameter(key, val);
    };

    G4cout << "=== Begin Nucleus parameters generated by CreateNucleusSubcomponent ===" << G4endl;

    // Define nucleus component parameters under Ge/Nucleus/...
    AddAndLog("s:" + ge("Type"),                        "\"TsNucleus\"");
    AddAndLog("s:" + ge("Parent"),                      Quote(fName)); // attach under this cell
    AddAndLog("s:" + ge("Material"),                    Quote(fNucleusMaterial));
    AddAndLog("s:" + ge("Color"),                       Quote(fNucleusColor));
    AddAndLog("s:" + ge("DNAModel"),                    Quote(fNucleusDNAModel));
    AddAndLog("d:" + ge("NucleusRadius"),               G4UIcommand::ConvertToString(fNucleusRadius/mm) + " mm");
    AddAndLog("i:" + ge("HilbertCurveLayer"),           G4UIcommand::ConvertToString(fNucleusHilbertCurveLayer));
    AddAndLog("i:" + ge("HilbertCurve3DRepeat"),        G4UIcommand::ConvertToString(fNucleusHilbertCurve3DRepeat));
    AddAndLog("s:" + ge("HilbertCurveFileName"),        Quote(fNucleusHilbertCurveFileName));

    AddAndLog("s:" + ge("Voxel/Material"),              Quote(fNucleusVoxelMaterial));
    AddAndLog("b:" + ge("ShowDNAVoxels"),               QBool(fNucleusShowDNAVoxels));
    AddAndLog("s:" + ge("ChromatinFiber/Material"),     Quote(fNucleusChromatinFiberMaterial));
    AddAndLog("b:" + ge("ShowChromatinCylinders"),      QBool(fNucleusShowChromatinCylinders));
    AddAndLog("s:" + ge("Histone/Material"),            Quote(fNucleusHistoneMaterial));
    AddAndLog("b:" + ge("OnlyBuildOneHistone"),         QBool(fNucleusOnlyBuildOneHistone));
    AddAndLog("b:" + ge("HistoneAsScavenger"),          QBool(fNucleusHistoneAsScavenger));
    AddAndLog("b:" + ge("AddBases"),                    QBool(fNucleusAddBases));
    AddAndLog("s:" + ge("Base1/Material"),              Quote(fNucleusBase1Material));
    AddAndLog("s:" + ge("Base2/Material"),              Quote(fNucleusBase2Material));

    // Set both for compatibility (TsNucleus reads "AddBackbone")
    AddAndLog("b:" + ge("AddBackbones"),                QBool(fNucleusAddBackbones));
    AddAndLog("b:" + ge("AddBackbone"),                 QBool(fNucleusAddBackbones));

    AddAndLog("s:" + ge("Backbone1/Material"),          Quote(fNucleusBackbone1Material));
    AddAndLog("s:" + ge("Backbone2/Material"),          Quote(fNucleusBackbone2Material));
    AddAndLog("b:" + ge("AddHydrationShell"),           QBool(fNucleusAddHydrationShell));
    AddAndLog("s:" + ge("HydrationShell1/Material"),    Quote(fNucleusHydrationShell1Material));
    AddAndLog("s:" + ge("HydrationShell2/Material"),    Quote(fNucleusHydrationShell2Material));

    // Center the nucleus in the cell
    AddAndLog("d:" + ge("translateX"),                  "0.0 um");
    AddAndLog("d:" + ge("translateY"),                  "0.0 um");
    AddAndLog("d:" + ge("translateZ"),                  "0.0 um");

    G4cout << "=== End Nucleus parameters ===" << G4endl;

    // Print the actual radius of the constructed G4Orb("Nucleus")
    G4Orb* nucleusOrb = nullptr;
    for (auto* solid : *G4SolidStore::GetInstance()) {
        if (solid->GetName() == "Nucleus") {
            nucleusOrb = dynamic_cast<G4Orb*>(solid);
            break;
        }
    }
    if (nucleusOrb) {
        G4cout << "[TsMyCellWithNPs] Nucleus G4Orb radius = "
               << nucleusOrb->GetRadius()/nm << " nm" << G4endl;
    } else {
        G4cout << "[TsMyCellWithNPs] Nucleus G4Orb not found in G4SolidStore" << G4endl;
    }
}
;
