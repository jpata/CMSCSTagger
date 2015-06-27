#include <algorithm>
#include <iostream>
#include <sstream>
#include <string>
#include <memory>
#include <vector>
#include <map>
#include <typeinfo>

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
#include "RecoBTag/SecondaryVertex/interface/CombinedSVComputer.h"
#include "RecoBTag/CombinedMVA/interface/CombinedMVAJetTagComputerETH.h"

#include "DataFormats/BTauReco/interface/CandIPTagInfo.h" 
#include "DataFormats/BTauReco/interface/CandSoftLeptonTagInfo.h" 
#include "DataFormats/BTauReco/interface/CandSecondaryVertexTagInfo.h"
#include "DataFormats/BTauReco/interface/CandIPTagInfo.h"

#include "DataFormats/BTauReco/interface/IPTagInfo.h" 
#include "DataFormats/BTauReco/interface/SoftLeptonTagInfo.h" 
#include "DataFormats/BTauReco/interface/SecondaryVertexTagInfo.h"
#include "DataFormats/BTauReco/interface/IPTagInfo.h"

#include "RecoBTag/ImpactParameter/interface/JetProbabilityComputer.h"
#include "RecoBTag/ImpactParameter/interface/CandidateJetProbabilityComputer.h"
#include "RecoBTag/ImpactParameter/interface/JetBProbabilityComputer.h"
#include "RecoBTag/ImpactParameter/interface/CandidateJetBProbabilityComputer.h"

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
	isCandidateBased = params.getParameter<bool>(
		"isCandidateBased"
	);

	uses(0, "ipTagInfos");
  	uses(1, "svTagInfos");
  	uses(2, "svTagInfos");
  	uses(3, "smTagInfos");
  	uses(4, "seTagInfos");
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
        std::cout << name << " " << typeid(*comp).name() << std::endl;
		std::vector<std::string> inputLabels(comp->getInputLabels());
		
		for (auto lab : inputLabels) {
			std::cout << name << " " << lab << std::endl;
		}
		
	}
  GenericMVAJetTagComputer::initialize(record);
}

float CombinedMVAJetTagComputerETH::discriminator(const JetTagComputer::TagInfoHelper &info) const
{
    

    if (isCandidateBased) {
        std::cout << "main tag info" << std::endl;
        info.printTypes();
        //float a1, a2, a3, a4, a5, a6;
        float a1, a2;
        const reco::CandIPTagInfo* ti1 = (const reco::CandIPTagInfo*)&info.getBase(0);
        const reco::CandIPTagInfo* ti2 = (const reco::CandIPTagInfo*)&info.getBase(0);
        const JetTagComputer::TagInfoHelper tv1({ti1}); 
        const JetTagComputer::TagInfoHelper tv2({ti2});
        //const JetTagComputer::TagInfoHelper tv_csv1({&info.get<const reco::BaseTagInfo>(0), &info.get<const reco::BaseTagInfo>(1)}); 
        //const JetTagComputer::TagInfoHelper tv_csv2({&info.get<const reco::BaseTagInfo>(0), &info.get<const reco::BaseTagInfo>(2)}); 
        //const JetTagComputer::TagInfoHelper tv3({&info.get<const reco::BaseTagInfo>(3)});
        //const JetTagComputer::TagInfoHelper tv4({&info.get<const reco::BaseTagInfo>(4)});
        std::cout << "got taginfos " << std::endl;
        //jetProbabilityComputer
        //const CandidateJetProbabilityComputer* comp1 = dynamic_cast<const CandidateJetProbabilityComputer*>(computers[0]);
        //const CandidateJetBProbabilityComputer* comp2 = dynamic_cast<const CandidateJetBProbabilityComputer*>(computers[1]);
        const JetTagComputer* comp1 = computers[0];
        const JetTagComputer* comp2 = computers[1];
        if (!comp1) {
            throw std::exception();
        }
        if (!comp2) {
            throw std::exception();
        }
        std::cout << "casted" << std::endl;
        
        a2 = (*comp2)(tv2);
        std::cout << "a2 " << a2 << std::endl;
        
        a1 = (*comp1)(tv1);
        std::cout << "a1 " << a1 << std::endl;
        //a3 = (*computers[2])(tv_csv1);
        //a4 = (*computers[3])(tv_csv2);
        //a5 = (*computers[4])(tv3);
        //a6 = (*computers[5])(tv4);
        //std::cout << "computer " << a1 << " " << a2 << " " << a3 << " " << a4 << " " << a5 << " " << a6 << std::endl;
    }
	return 0.0;
}
