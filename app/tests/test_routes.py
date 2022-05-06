from app.models.cats import Cat


def test_get_all_cats_with_empty_db_returns_empty_list(client):
    response = client.get('/cats')
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

def test_get_one_cat_with_populated_db_returns_cat_jason(client, seven_cats):
    response = client.get("/cats/1")
    response_body = response.get_json()

    # id = 1, name = "Jazz", color = "black", age = 8
    assert response.status_code == 200
    assert response_body == {
        "id" : 1,
        "name" : "Jazz",
        "color" : "black",
        "age" : 8
    }

def test_get_all_cats_with_populated_db_returns_populated_list(client, seven_cats):
    response = client.get('/cats')
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 7


def test_post_one_cat_creates_cat_in_db(client):
    response = client.post('/cats', json = {"name" : "Bernie", "color" : "grey", "age" : 14})
    response_body = response.get_json()

    assert response.status_code == 201
    assert "id" in response_body
    assert "msg" in response_body
    
    cats = Cat.query.all()
    assert len(cats) == 1
    assert cats[0].name == "Bernie"
    assert cats[0].age == 14
    assert cats[0].color == "grey"

def test_get_one_cat_with_empty_db_returns_404(client):
    response = client.get('/cats/1')
    assert response.status_code == 404

def test_get_missing_cat_with_populated_db_returns_404(client, seven_cats):
    response = client.get('/cats/90')
    assert response.status_code == 404
