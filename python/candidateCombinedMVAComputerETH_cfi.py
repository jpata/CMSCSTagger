import FWCore.ParameterSet.Config as cms

candidateCombinedMVAComputerETH = cms.ESProducer("CombinedMVAJetTagESProducerETH",
	useCategories = cms.bool(False),
	calibrationRecord = cms.string('CombinedMVAETH'),
	jetTagComputers = cms.vstring(
        'candidateJetProbabilityComputer',
        'candidateCombinedSecondaryVertexComputer',
        'softPFMuonComputer',
        'softPFElectronComputer'
    )
)
