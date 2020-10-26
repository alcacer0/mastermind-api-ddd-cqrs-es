import pytest

from flask import url_for

from mastermind.shared.model import UniqueID
from mastermind.games.composition_root import get_game_write_repo
from mastermind.games.use_cases import create_new_game_with_code_to_break, GameConfigDTO


@pytest.fixture
def test_game(test_db):
    with get_game_write_repo() as game_repo:
        game_config = GameConfigDTO(max_guesses=6)
        game = create_new_game_with_code_to_break(
            operation_id=UniqueID(), game_config=game_config, repo=game_repo)

    yield game


def test_post_new_game(client, test_db):
    # Test max guesses is validated
    url = url_for('gameresource')
    response = client.post(url, json={})
    assert response.status_code == 422
    response = client.post(url, json={'max_guesses': 99})
    assert response.status_code == 422

    # Test max_guesses and new game uuid is returned
    response = client.post(url, json={'max_guesses': 6})
    assert 'max_guesses' in response.get_json()
    assert 'game_id' in response.get_json()

    # Test events are created and we can source a game aggregate/entity with
    # the given config, a game id and a code to break.
    response_game_id = response.get_json().get('game_id')
    with get_game_write_repo() as game_repo:
        game = game_repo.get_by_id(response_game_id)
        assert game.max_guesses == 6
        assert game.game_id.value == response_game_id
        assert game.code_to_break is not None
        assert game.points == 0
        assert not game.finished


def test_post_a_code_guess_and_return_feedback(client, test_db, test_game):
    # Test guess data is validated
    url = url_for('codeguessresource', game_id=test_game.game_id.value)
    response = client.post(url, json={'code': ['Red']})
    assert response.status_code == 400 # min kwarg no effect in schema. Validated by Code.
    response = client.post(url, json={'code': ['Red', 'Red', 'Red', 'R']})
    assert response.status_code == 422

    # Test feedback is returned
    response = client.post(url, json={'code': ['Red', 'Red', 'Red', 'Red']})
    assert response.status_code == 201
    assert 'blacks' in response.get_json()
    assert 'whites' in response.get_json()


def test_a_code_guess_increases_one_point(client, test_db, test_game):
    # Can make a guess and the code maker earns a point
    url = url_for('codeguessresource', game_id=test_game.game_id.value)
    response = client.post(url, json={'code': ['Red', 'Red', 'Red', 'Red']})
    assert response.status_code == 201

    with get_game_write_repo() as game_repo:
        game = game_repo.get_by_id(test_game.game_id.value)
        assert game.points == 1


def test_game_is_finished_and_decoded_when_guess_is_correct(client, test_db, test_game):
    url = url_for('codeguessresource', game_id=test_game.game_id.value)
    response = client.post(url, json={'code': test_game.code_to_break.value})
    assert response.status_code == 201

    with get_game_write_repo() as game_repo:
        game = game_repo.get_by_id(test_game.game_id.value)
        assert game.decoded
        assert game.finished


def test_game_is_finished_but_not_decoded_when_reaching_max_attempts(client, test_db, test_game):
    url = url_for('codeguessresource', game_id=test_game.game_id.value)

    for i in range(test_game.max_guesses):
        response = client.post(url, json={'code': ['Red', 'Red', 'Red', 'Red']})
        assert response.status_code == 201

    # Test game finished validation
    response = client.post(url, json={'code': ['Red', 'Red', 'Red', 'Red']})
    assert response.status_code == 400

    with get_game_write_repo() as game_repo:
        game = game_repo.get_by_id(test_game.game_id.value)
        assert not game.decoded
        assert game.finished

        # Test one extra point is given if the game finishes without being decoded
        assert game.points == game.max_guesses + 1
