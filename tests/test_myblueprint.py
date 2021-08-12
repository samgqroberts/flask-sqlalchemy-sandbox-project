def test_get_things(client):
    res = client.get(client.url_for('myblueprint.things'))
    assert res.status_code == 200
    assert res.get_json() == ['response', 'to', 'GET', 'request']

def test_create_things(client):
    res = client.post(client.url_for('myblueprint.things'))
    assert res.status_code == 200
    assert res.get_json() == ['response', 'to', 'POST', 'request']
