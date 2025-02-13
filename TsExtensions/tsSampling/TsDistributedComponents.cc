// Component for TsDistributedComponents
//
// ******************************************************************
// *
// *
// * File included as an extension for TOPAS
// * Authors: Alejandro Bertolet <abertoletreina@mgh.harvard.edu>,
// *
// *
// ******************************************************************

#include "TsDistributedComponents.hh"
#include "TsParameterManager.hh"


TsDistributedComponents::TsDistributedComponents(TsParameterManager* pM, TsExtensionManager* eM, TsMaterialManager* mM, TsGeometryManager* gM,
		TsVGeometryComponent* parentComponent, G4VPhysicalVolume* parentVolume, G4String& name) :
		TsVGeometryComponent(pM, eM, mM, gM, parentComponent, parentVolume, name)
{

	
	fElementRadius = fPm->GetDoubleParameter(GetFullParmName("ElementRadius"), "Length");
	fElementMaterialName = fPm->GetStringParameter(GetFullParmName("ElementMaterial"));
	fPositionsFileName = fPm->GetStringParameter(GetFullParmName("PositionsFile"));
	
	fComponentType = fPm->GetStringParameter(GetFullParmName("ComponentType"));

	if (fComponentType == "G4Sphere" || fComponentType == "G4Tubs") {
		fComponentRadius = fPm->GetDoubleParameter(GetFullParmName("ComponentRadius"), "Length");
	}
	if (fComponentType == "G4Tubs") {
		fComponentHL = fPm->GetDoubleParameter(GetFullParmName("ComponentHL"), "Length");
	}
	if (fComponentType == "G4Box" || fComponentType == "G4Ellipsoid") {
		fComponentHLX = fPm->GetDoubleParameter(GetFullParmName("ComponentHLX"), "Length");
		fComponentHLY = fPm->GetDoubleParameter(GetFullParmName("ComponentHLY"), "Length");
		fComponentHLZ = fPm->GetDoubleParameter(GetFullParmName("ComponentHLZ"), "Length");
	}
}
TsDistributedComponents::~TsDistributedComponents() {}

G4VPhysicalVolume* TsDistributedComponents::Construct()
{
	std::vector<G4ThreeVector> positionList = ReadPositionsFile();
	G4int nSubcomponents = positionList.size();
	BeginConstruction();	
	
	// Component Solid
    G4VSolid* componentSolid;
    if (fComponentType == "G4Sphere") {
        componentSolid = new G4Orb(fName, fComponentRadius);
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

	// Updated parameterization instantiation using only 'positionList'
	fParam = new TsParameterizationDistributed(positionList);

	// Subelements
	G4String name = "SubcompSolid";
	G4VSolid* subcomponentSolid = new G4Orb(name, fElementRadius);
	G4LogicalVolume* subLogic = CreateLogicalVolume("LogSubcomponent", fElementMaterialName, subcomponentSolid);
	if (nSubcomponents > 1)
		CreatePhysicalVolume("Subcomponents", subLogic, fEnvelopePhys, kUndefined, nSubcomponents, fParam);
	if (nSubcomponents == 1)
		CreatePhysicalVolume("Subcomponent", subLogic, new G4RotationMatrix(), &positionList[0], fEnvelopePhys);

	if (fParentVolume)
		InstantiateChildren();
	return fEnvelopePhys;
}

std::vector<G4ThreeVector> TsDistributedComponents::ReadPositionsFile()
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
;
