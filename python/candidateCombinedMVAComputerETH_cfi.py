import FWCore.ParameterSet.Config as cms

candidateCombinedMVAComputerETH = cms.ESProducer("CombinedMVAJetTagESProducerETH",
	useCategories = cms.bool(False),
	calibrationRecord = cms.string('CombinedMVA'),
	jetTagComputers = cms.vstring(
        'candidateJetProbabilityComputer',
        'candidateJetBProbabilityComputer',
        'candidateCombinedSecondaryVertexComputer',
        'candidateCombinedSecondaryVertexComputer',
        'softPFMuonComputer',
        'softPFElectronComputer'
    ),
    isCandidateBased = cms.bool(True)
)
