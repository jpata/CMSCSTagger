#include <algorithm>
#include <iostream>
#include <sstream>
#include <string>
#include <memory>
#include <vector>
#include <map>

#include "FWCore/Utilities/interface/Exception.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "CondFormats/PhysicsToolsObjects/interface/MVAComputer.h"
#include "DataFormats/Common/interface/RefToBase.h"
#include "DataFormats/JetReco/interface/Jet.h"
#include "DataFormats/BTauReco/interface/TaggingVariable.h"
#include "RecoBTau/JetTagComputer/interface/JetTagComputer.h"
#include "RecoBTau/JetTagComputer/interface/JetTagComputerRecord.h"
#include "RecoBTau/JetTagComputer/interface/GenericMVAJetTagComputer.h"
#include "RecoBTag/CombinedMVA/interface/CombinedMVAJetTagComputerETH.h"

#include "DataFormats/BTauReco/interface/CandSoftLeptonTagInfo.h" 
#include "DataFormats/BTauReco/interface/CandSecondaryVertexTagInfo.h"
#include "DataFormats/BTauReco/interface/CandIPTagInfo.h"

using namespace reco;
using namespace PhysicsTools;

CombinedMVAJetTagComputerETH::CombinedMVAJetTagComputerETH(
					const edm::ParameterSet &params) :
	GenericMVAJetTagComputer(params)
{
	std::cout << "CombinedMVAJetTagComputerETH::constructor" << std::endl;

	inputComputerNames = params.getParameter< std::vector<std::string>>(
		"jetTagComputers"
	);

	uses(0, "ipTagInfos");
  	uses(1, "svTagInfos");
  	uses(2, "muonTagInfos");
  	uses(3, "elecTagInfos");
}

CombinedMVAJetTagComputerETH::~CombinedMVAJetTagComputerETH()
{
}

void CombinedMVAJetTagComputerETH::initialize(const JetTagComputerRecord & record) {
	std::cout << "CombinedMVAJetTagComputerETH::initialize" << std::endl;

	for (auto & name : inputComputerNames) {
		edm::ESHandle<JetTagComputer> computerHandle;
		record.get(name, computerHandle);
		const JetTagComputer* comp = computerHandle.product();
		computers.push_back(comp);
		std::vector<std::string> inputLabels(comp->getInputLabels());
		
		for (auto lab : inputLabels) {
			std::cout << name << " " << lab << std::endl;
		}
		
	}
  GenericMVAJetTagComputer::initialize(record);
}

float CombinedMVAJetTagComputerETH::discriminator(const JetTagComputer::TagInfoHelper &info) const
{
    const reco::CandIPTagInfo              & ipTagInfo = info.get<reco::CandIPTagInfo>(0);
    //const reco::CandSecondaryVertexTagInfo & svTagInfo = info.get<reco::CandSecondaryVertexTagInfo>(1);
    const reco::CandSoftLeptonTagInfo      & muonTagInfo = info.get<reco::CandSoftLeptonTagInfo>(2);
    const reco::CandSoftLeptonTagInfo      & elecTagInfo = info.get<reco::CandSoftLeptonTagInfo>(3);

	//jetProbabilityComputer
    float a1 = (*computers[0])(ipTagInfo);
        
	//jetBProbabilityComputer
    float a2 = (*computers[1])(ipTagInfo);
    
	//combinedSecondaryVertexComputer
    float a3 = (*computers[2])(info);
	
    //combinedSecondaryVertexComputer
    float a4 = (*computers[3])(info);
    
    float a5 = (*computers[4])(muonTagInfo);
    
    float a6 = (*computers[5])(elecTagInfo);
    
    std::cout << "computer " << a1 << " " << a2 << " " << a3 << " " << a4 << " " << a5 << " " << a6 << std::endl;

	return a1;
}
