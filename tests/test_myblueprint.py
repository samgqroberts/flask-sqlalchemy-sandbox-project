from myapp.myblueprint import Thing, db


def test_get_things(app, client):
    with app.app_context():
        t1 = Thing(name='t1')
        t2 = Thing(name='t2')
        db.session.add(t1)
        db.session.add(t2)
        db.session.commit()
    res = client.get(client.url_for('myblueprint.things'))
    assert res.status_code == 200
    assert res.get_json() == [{'id': 1, 'name': 't1'}, {'id': 2, 'name': 't2'}]


def test_create_things(app, client):
    res = client.post(client.url_for('myblueprint.things'), json={'name': 'new-thing'})
    assert res.status_code == 200
    assert res.data == b'Ok'
    with app.app_context():
        created = Thing.query.one()
        assert created.id == 1
        assert created.name == 'new-thing'
