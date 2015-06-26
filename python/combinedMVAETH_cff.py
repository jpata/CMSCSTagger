import FWCore.ParameterSet.Config as cms

from RecoBTag.CombinedMVA.combinedMVAComputerETH_cfi import *
from RecoBTag.CombinedMVA.combinedMVABJetTagsETH_cfi import *
from RecoBTag.CombinedMVA.pfCombinedMVABJetTagsETH_cfi import *

candidateCombinedMVAComputerNEW = cms.ESProducer("CombinedMVAJetTagESProducer",
	useCategories = cms.bool(False),
	calibrationRecord = cms.string('CombinedMVA'),
	jetTagComputers = cms.VPSet(
		cms.PSet(
			discriminator = cms.bool(True),
			variables = cms.bool(False),
			jetTagComputer = cms.string('candidateJetProbabilityComputer')
		),
		cms.PSet(
			discriminator = cms.bool(True),
			variables = cms.bool(False),
			jetTagComputer = cms.string('candidateCombinedSecondaryVertexComputer')
		),
		cms.PSet(
			discriminator = cms.bool(True),
			variables = cms.bool(False),
			jetTagComputer = cms.string('softPFMuonComputer')
		),
		cms.PSet(
			discriminator = cms.bool(True),
			variables = cms.bool(False),
			jetTagComputer = cms.string('softPFElectronComputer')
		)
	)
)

pfCombinedMVABJetTagsNEW= cms.EDProducer("JetTagProducer",
	jetTagComputer = cms.string('candidateCombinedMVAComputerNEW'),
	tagInfos = cms.VInputTag(
		cms.InputTag("pfImpactParameterTagInfos"),
		cms.InputTag("pfInclusiveSecondaryVertexFinderTagInfos"),
		cms.InputTag("softPFMuonsTagInfos"),
		cms.InputTag("softPFElectronsTagInfos")
	)
)

combinedMVAComputerNEW = cms.ESProducer("CombinedMVAJetTagESProducer",
	useCategories = cms.bool(False),
	calibrationRecord = cms.string('CombinedMVA'),
	jetTagComputers = cms.VPSet(
		cms.PSet(
			discriminator = cms.bool(True),
			variables = cms.bool(False),
			jetTagComputer = cms.string('jetProbabilityComputer')
		),
		cms.PSet(
			discriminator = cms.bool(True),
			variables = cms.bool(False),
			jetTagComputer = cms.string('combinedSecondaryVertexComputer')
		),
		cms.PSet(
			discriminator = cms.bool(True),
			variables = cms.bool(False),
			jetTagComputer = cms.string('softPFMuonComputer')
		),
		cms.PSet(
			discriminator = cms.bool(True),
			variables = cms.bool(False),
			jetTagComputer = cms.string('softPFElectronComputer')
		)
	)
)

combinedMVABJetTagsNEW = cms.EDProducer("JetTagProducer",
	jetTagComputer = cms.string('combinedMVAComputerNEW'),
	tagInfos = cms.VInputTag(
		cms.InputTag("impactParameterTagInfos"),
		cms.InputTag("inclusiveSecondaryVertexFinderTagInfos"),
		cms.InputTag("softPFMuonsTagInfos"),
		cms.InputTag("softPFElectronsTagInfos")
	)
)
