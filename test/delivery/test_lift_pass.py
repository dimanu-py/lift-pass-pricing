import pytest

from src.prices import app


class TestLiftPass:
    def test_can_add_new_lift_pass(self) -> None:
        client = app.test_client()

        response = client.put("/prices", query_string={"type": "1jour", "cost": 35})

        assert response.json == {}

    @pytest.mark.parametrize("pass_type", ["1jour", "night"])
    def test_pass_is_free_for_people_younger_than_six(self, pass_type: str) -> None:
        client = app.test_client()

        response = client.get("/prices", query_string={"type": pass_type, "age": 5})

        assert response.json == {"cost": 0}

    def test_night_pass_keeps_base_price_for_people_between_six_and_sixty_four(
        self,
    ) -> None:
        client = app.test_client()

        response = client.get("/prices", query_string={"type": "night", "age": 30})

        assert response.json == {"cost": 19}

    def test_night_pass_gets_sixty_percent_discount_for_people_older_than_sixty_four(
        self,
    ) -> None:
        client = app.test_client()

        response = client.get("/prices", query_string={"type": "night", "age": 65})

        assert response.json == {"cost": 8}

    def test_1jour_pass_gets_thirty_percent_discount_for_people_younger_than_fifteen(
        self,
    ) -> None:
        client = app.test_client()

        response = client.get("/prices", query_string={"type": "1jour", "age": 14})

        assert response.json == {"cost": 25}

    def test_1jour_pass_keeps_base_price_if_age_is_unknown(self) -> None:
        client = app.test_client()

        response = client.get("/prices", query_string={"type": "1jour"})

        assert response.json == {"cost": 35}

    def test_1jour_pass_gets_twenty_five_percent_discount_for_people_older_than_sixty_four(
        self,
    ) -> None:
        client = app.test_client()

        response = client.get("/prices", query_string={"type": "1jour", "age": 65})

        assert response.json == {"cost": 27}

    def test_1jour_pass_keeps_base_price_for_people_between_fifteen_and_sixty_four(
        self,
    ) -> None:
        client = app.test_client()

        response = client.get("/prices", query_string={"type": "1jour", "age": 30})

        assert response.json == {"cost": 35}

    def test_1jour_pass_gets_thirty_five_percent_discount_on_non_festive_mondays(
        self,
    ) -> None:
        client = app.test_client()

        response = client.get(
            "/prices", query_string={"type": "1jour", "date": "2022-01-03"}
        )

        assert response.json == {"cost": 23}

    def test_1jour_pass_keeps_base_price_on_holidays(self) -> None:
        client = app.test_client()

        response = client.get(
            "/prices", query_string={"type": "1jour", "date": "2019-02-18"}
        )

        assert response.json == {"cost": 35}

    def test_night_pass_is_free_if_age_is_unknown(self) -> None:
        client = app.test_client()

        response = client.get("/prices", query_string={"type": "night"})

        assert response.json == {"cost": 0}
