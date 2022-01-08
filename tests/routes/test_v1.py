import json


def test_email_sent_success(test_client):
    """
    GIVEN app client
    WHEN the '/v1/encode' route is called via POST method
    THEN check if the response is valid
    """
    response = test_client.post(
        '/v1/user/register/confirm',
        data=json.dumps(dict(name='Jakub', email='jakub@graitor.dk')),
        mimetype="application/json"
    )

    assert response.status_code == 200


def test_email_sent_missing_parameters(test_client):
    response = test_client.post(
        '/v1/user/register/confirm',
        data=json.dumps(dict(email='jakub@graitor.dk')),
        mimetype="application/json"
    )

    assert response.status_code == 400
    assert b'not found' in response.data