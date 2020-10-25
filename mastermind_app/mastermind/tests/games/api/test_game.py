from flask import url_for

from mastermind.games.composition_root import get_game_write_repo


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
    # the given config and a game id
    response_game_id = response.get_json().get('game_id')
    with get_game_write_repo() as game_repo:
        game = game_repo.get_by_id(response_game_id)
        assert game.max_guesses == 6
        assert game.game_id.value == response_game_id
