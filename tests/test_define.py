from blackmamba_cognitive.define import create_contract


def test_define_contract_is_deterministic():
    first = create_contract(
        "Map repository evidence",
        inputs=["snapshot"],
        outputs=["graph"],
        constraints=["deterministic"],
        acceptance=["same input => same hash"],
        prohibited=["mutate source"],
        evidence=["snapshot:abc"],
    )
    second = create_contract(
        "Map repository evidence",
        inputs=["snapshot"],
        outputs=["graph"],
        constraints=["deterministic"],
        acceptance=["same input => same hash"],
        prohibited=["mutate source"],
        evidence=["snapshot:abc"],
    )

    assert first == second
    assert first["authorization_required"] is True
    assert first["contract_sha256"]


def test_define_rejects_empty_objective():
    try:
        create_contract("   ")
    except ValueError:
        pass
    else:
        raise AssertionError("empty objective must fail")
