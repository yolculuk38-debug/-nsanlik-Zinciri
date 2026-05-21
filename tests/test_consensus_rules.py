from consensus_rules import ConsensusStatus, evaluate_consensus


def witness(witness_id, verdict, content_hash="abc"):
    return {
        "witness_id": witness_id,
        "witness_type": "ai",
        "verdict": verdict,
        "content_hash": content_hash,
    }


def test_pass_consensus_reached():
    result = evaluate_consensus(
        [
            witness("w1", "PASS"),
            witness("w2", "PASS"),
            witness("w3", "PASS"),
        ]
    )
    assert result["status"] == ConsensusStatus.CONSENSUS_REACHED.value
    assert result["trusted"] is True


def test_partial_consensus():
    result = evaluate_consensus(
        [
            witness("w1", "PASS"),
            witness("w2", "PASS"),
            witness("w3", "FAIL"),
        ],
        threshold=0.8,
    )
    assert result["status"] == ConsensusStatus.PARTIAL_CONSENSUS.value


def test_hash_conflict():
    result = evaluate_consensus(
        [
            witness("w1", "PASS", "hash-a"),
            witness("w2", "PASS", "hash-b"),
            witness("w3", "PASS", "hash-a"),
        ]
    )
    assert result["status"] == ConsensusStatus.CONFLICT.value
    assert result["hash_conflict"] is True


def test_insufficient_witnesses():
    result = evaluate_consensus([witness("w1", "PASS")])
    assert result["status"] == ConsensusStatus.INSUFFICIENT_WITNESSES.value


def test_duplicate_witness_ignored():
    result = evaluate_consensus(
        [
            witness("same", "PASS"),
            witness("same", "FAIL"),
            witness("w2", "PASS"),
            witness("w3", "PASS"),
        ]
    )
    assert result["status"] == ConsensusStatus.CONSENSUS_REACHED.value
    assert result["witness_count"] == 3


def test_invalid_input():
    result = evaluate_consensus("bad-input")
    assert result["status"] == ConsensusStatus.INVALID_INPUT.value
