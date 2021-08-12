def test_get_things(client):
    res = client.get(client.url_for('myblueprint.list_things'))
    assert res.status_code == 200
    assert res.get_json() == ['thing1', 'thing2']
