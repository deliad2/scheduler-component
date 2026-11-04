"""Regression tests for loading stored schedule data."""

import unittest

from custom_components.scheduler.store import parse_schedule_data


class ParseScheduleDataTests(unittest.TestCase):
    """Stored entries with unknown keys must not break loading."""

    def test_unknown_keys_are_ignored(self):
        """A stored action with an extra 'target' key still loads."""
        data = {
            "timeslots": [
                {
                    "start": "08:00:00",
                    "stop": None,
                    "unknown_slot_key": 1,
                    "conditions": [
                        {"entity_id": "sensor.a", "value": "on", "unknown": None}
                    ],
                    "actions": [
                        {
                            "service": "switch.turn_on",
                            "entity_id": "switch.a",
                            "service_data": {},
                            "target": None,
                        }
                    ],
                }
            ]
        }
        timeslot = parse_schedule_data(data)["timeslots"][0]
        self.assertEqual(timeslot.actions[0].service, "switch.turn_on")
        self.assertEqual(timeslot.actions[0].entity_id, "switch.a")
        self.assertEqual(timeslot.conditions[0].entity_id, "sensor.a")


if __name__ == "__main__":
    unittest.main()
