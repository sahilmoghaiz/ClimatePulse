from config.locations import LOCATIONS


def test_locations_exist():
    assert len(LOCATIONS) == 31

def test_location_configuration_integrity():
    required_fields = {
        "state",
        "city",
        "latitude",
        "longitude",
        "location_type",
    }

    for location in LOCATIONS:
        assert required_fields.issubset(location.keys())
        assert location["state"]
        assert location["city"]
        assert -90 <= location["latitude"] <= 90
        assert -180 <= location["longitude"] <= 180
        assert location["location_type"] in {
            "State Representative",
            "Additional City",
            "Union Territory",
        }
