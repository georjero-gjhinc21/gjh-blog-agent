def test_list_affiliates_has_sort_by_in_source():
    with open('main.py', 'r') as f:
        src = f.read()

    # Ensure function definition includes sort_by with default 'name'
    assert 'def list_affiliates(' in src
    assert 'sort_by: str = "name"' in src
