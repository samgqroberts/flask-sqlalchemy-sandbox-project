from myapp.thing import Thing, db


def test_get_things(app, client):
    with app.app_context():
        t1 = Thing(name='t1')
        t2 = Thing(name='t2')
        db.session.add(t1)
        db.session.add(t2)
        db.session.commit()
    res = client.get(client.url_for('thing.things'))
    assert res.status_code == 200
    assert res.get_json() == [{'id': 1, 'name': 't1'}, {'id': 2, 'name': 't2'}]


def test_create_thing(app, client):
    res = client.post(client.url_for('thing.things'), json={'name': 'new-thing'})
    assert res.status_code == 200
    assert res.data == b'Ok'
    with app.app_context():
        created = Thing.query.one()
        assert created.id == 1
        assert created.name == 'new-thing'


def test_get_thing(app, client):
    res = client.get(client.url_for('thing.thing', id=1))
    assert res.status_code == 404

    with app.app_context():
        t1 = Thing(name='t1')
        db.session.add(t1)
        db.session.commit()
    res = client.get(client.url_for('thing.thing', id=1))
    assert res.status_code == 200
    assert res.get_json() == {'id': 1, 'name': 't1'}


def test_update_thing(app, client):
    res = client.put(client.url_for('thing.thing', id=1))
    assert res.status_code == 404

    with app.app_context():
        t1 = Thing(name='t1')
        db.session.add(t1)
        db.session.commit()
    res = client.put(client.url_for('thing.thing', id=1))
    assert res.status_code == 400
    assert res.data == b'Provided json body needs a "name" field.'

    data = {'name': 'new name'}
    res = client.put(client.url_for('thing.thing', id=1), json=data)
    assert res.status_code == 200
    assert res.data == b'Ok'
    with app.app_context():
        assert Thing.query.get(1).name == 'new name'


def test_delete_thing(app, client):
    res = client.delete(client.url_for('thing.thing', id=1))
    assert res.status_code == 404

    with app.app_context():
        t1 = Thing(name='t1')
        db.session.add(t1)
        db.session.commit()
    res = client.delete(client.url_for('thing.thing', id=1))
    assert res.status_code == 200
    assert res.data == b'Ok'
    with app.app_context():
        assert Thing.query.filter_by(id=1).count() == 0