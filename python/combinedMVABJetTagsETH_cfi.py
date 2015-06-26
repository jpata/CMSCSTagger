import FWCore.ParameterSet.Config as cms

combinedMVABJetTagsETH = cms.EDProducer("JetTagProducer",
	jetTagComputer = cms.string('combinedMVAComputerETH'),
	tagInfos = cms.VInputTag(
		cms.InputTag("impactParameterTagInfos"),
		cms.InputTag("inclusiveSecondaryVertexFinderTagInfos"),
		cms.InputTag("softPFMuonsTagInfos"),
		cms.InputTag("softPFElectronsTagInfos")
	)
)
