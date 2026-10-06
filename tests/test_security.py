import copy
import json
import os
import re
import tempfile
import unittest
from itertools import count
from pathlib import Path

os.environ["SECRET_KEY"] = "unit-test-only-secret-key-" + "a" * 40

import app as application


TEST_ADDRESS_COUNTER = count(1)


def valid_record():
    return {
        "Name": "Test Router",
        "IP": "192.168.20.1",
        "Protocolos": ["OSPF", "BGP"],
        "status": "online",
        "VLANs": {
            "VL1": {
                "Ports": ["GigabitEthernet0/1"],
                "Policies": ["ALLOW_ALL"],
                "ET": True,
                "IP": "192.168.20.2",
                "SSH": True,
            },
            "VL2": {
                "Ports": ["WLAN0"],
                "Policies": ["BLOCK_ALL"],
                "ET": False,
                "IP": "192.168.20.3",
                "SSH": False,
            },
        },
    }


class SecurityRouteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        application.app.config.update(TESTING=True)

    def setUp(self):
        self.original_data = copy.deepcopy(application.datos_json)
        self.original_path = application.API_JSON_PATH
        self.temp_directory = tempfile.TemporaryDirectory()
        application.API_JSON_PATH = Path(self.temp_directory.name) / "API.json"
        application.API_JSON_PATH.write_text(json.dumps(self.original_data), encoding="utf-8")
        application.datos_json = copy.deepcopy(self.original_data)
        self.client = application.app.test_client()
        self.client.environ_base["REMOTE_ADDR"] = f"198.51.100.{next(TEST_ADDRESS_COUNTER)}"

    def tearDown(self):
        application.API_JSON_PATH = self.original_path
        application.datos_json = self.original_data
        self.temp_directory.cleanup()

    def csrf_token(self, path):
        response = self.client.get(path)
        match = re.search(rb'name="csrf_token" value="([^"]+)"', response.data)
        self.assertIsNotNone(match)
        return match.group(1).decode()

    def test_device_routes_are_public_and_auth_routes_are_removed(self):
        self.assertEqual(self.client.get("/elements").status_code, 200)
        self.assertEqual(self.client.get("/add").status_code, 200)
        self.assertEqual(self.client.get("/json/3D:AF:09:7F:00:02").status_code, 200)
        self.assertEqual(self.client.get("/login").status_code, 404)
        self.assertEqual(self.client.get("/logout").status_code, 404)

    def test_add_requires_csrf_and_persists_multiple_vlans(self):
        payload = {"identifier": "AA:BB:CC:DD:EE:FF", "record": valid_record()}
        token = self.csrf_token("/add")
        missing_token = self.client.post("/add", json=payload)
        self.assertEqual(missing_token.status_code, 400)
        self.assertIn("error", missing_token.get_json())

        response = self.client.post(
            "/add", json=payload, headers={"X-CSRFToken": token}
        )
        self.assertEqual(response.status_code, 201)
        stored = json.loads(application.API_JSON_PATH.read_text(encoding="utf-8"))
        self.assertEqual(stored[payload["identifier"]], payload["record"])
        self.assertIn(b"Test Router", self.client.get("/elements").data)

        duplicate = self.client.post(
            "/add", json=payload, headers={"X-CSRFToken": token}
        )
        self.assertEqual(duplicate.status_code, 409)

    def test_invalid_device_fields_are_rejected(self):
        token = self.csrf_token("/add")
        record = valid_record()
        invalid_payloads = [
            ("broken-mac", record, "identifier"),
            ("AA:BB:CC:DD:EE:01", {**record, "Name": "2Router"}, "name"),
            ("AA:BB:CC:DD:EE:02", {**record, "IP": "256.1.1.1"}, "device_ip"),
            ("AA:BB:CC:DD:EE:03", {**record, "Protocolos": ["made-up"]}, "protocols"),
            ("AA:BB:CC:DD:EE:04", {**record, "status": []}, "status"),
        ]
        for identifier, invalid_record, expected_field in invalid_payloads:
            with self.subTest(field=expected_field):
                response = self.client.post(
                    "/add",
                    json={"identifier": identifier, "record": invalid_record},
                    headers={"X-CSRFToken": token},
                )
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.get_json()["field"], expected_field)

    def test_duplicate_ports_are_rejected_across_vlans(self):
        record = valid_record()
        record["VLANs"]["VL2"]["Ports"] = ["gigabitethernet0/1"]
        cleaned, error = application.validate_device_record(record)
        self.assertIsNone(cleaned)
        self.assertEqual(error["field"], "vlan:VL2:Ports")

    def test_duplicate_protocols_are_rejected(self):
        record = valid_record()
        record["Protocolos"] = ["OSPF", "ospf"]
        cleaned, error = application.validate_device_record(record)
        self.assertIsNone(cleaned)
        self.assertEqual(error["field"], "protocols")

    def test_duplicate_json_vlan_keys_are_rejected(self):
        token = self.csrf_token("/add")
        raw_payload = (
            '{"identifier":"AA:BB:CC:DD:EE:FF","record":'
            '{"Name":"Router","IP":"192.0.2.1","Protocolos":["OSPF"],'
            '"status":"online","VLANs":{"VL1":{},"VL1":{}}}}'
        )
        response = self.client.post(
            "/add",
            data=raw_payload,
            content_type="application/json",
            headers={"X-CSRFToken": token},
        )
        self.assertEqual(response.status_code, 400)

    def test_deeply_nested_json_is_rejected_without_server_error(self):
        token = self.csrf_token("/add")
        deeply_nested = "[" * 2000 + "0" + "]" * 2000
        response = self.client.post(
            "/add",
            data=deeply_nested,
            content_type="application/json",
            headers={"X-CSRFToken": token},
        )
        self.assertEqual(response.status_code, 400)

    def test_disk_only_identifier_collision_is_rejected(self):
        token = self.csrf_token("/add")
        identifier = "3D:AF:09:7F:00:02"
        application.datos_json.pop(identifier)
        response = self.client.post(
            "/add",
            json={"identifier": identifier, "record": valid_record()},
            headers={"X-CSRFToken": token},
        )
        self.assertEqual(response.status_code, 409)

    def test_control_characters_are_removed_from_text(self):
        record = valid_record()
        record["Name"] = "Test\x00 Router"
        cleaned, error = application.validate_device_record(record)
        self.assertIsNone(error)
        self.assertEqual(cleaned["Name"], "Test Router")

    def test_edit_prefills_legacy_record_and_persists_update(self):
        device_id = "3D:RF:09:7F::"
        form = self.client.get(f"/edit/{device_id}")
        self.assertEqual(form.status_code, 200)
        self.assertIn(b"Edit network device", form.data)
        self.assertIn(b"value=\"R1\"", form.data)
        self.assertIn(b"value=\"192.168.10.1\"", form.data)
        self.assertIn(b"value=\"3D:RF:09:7F::\"", form.data)
        self.assertIn(b"action=\"/edit/3D:RF:09:7F::\"", form.data)
        self.assertIn(b"value=\"GigabitEthernet0/1\"", form.data)
        self.assertIn(b"value=\"ALLOW_ALL\"", form.data)
        self.assertIn(b'data-field="ET" type="checkbox" checked', form.data)

        token = self.csrf_token(f"/edit/{device_id}")
        updated_record = valid_record()
        updated_record["Name"] = "Renamed Router"
        response = self.client.post(
            f"/edit/{device_id}",
            json={"identifier": device_id, "record": updated_record},
            headers={"X-CSRFToken": token},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(application.datos_json[device_id], updated_record)
        saved = json.loads(application.API_JSON_PATH.read_text(encoding="utf-8"))
        self.assertEqual(saved[device_id], updated_record)
        table = self.client.get("/elements")
        self.assertIn(b"Renamed Router", table.data)
        self.assertIn(b"updated successfully", table.data)

    def test_elements_link_to_csrf_protected_edit_and_delete_actions(self):
        response = self.client.get("/elements")
        self.assertIn(b'href="/edit/3D:AF:09:7F:00:02"', response.data)
        self.assertIn(b'action="/delete/3D:AF:09:7F:00:02"', response.data)
        self.assertIn(b'onsubmit="return confirm(\'Are you sure you want to delete this device?\');"', response.data)
        self.assertIn("'unsafe-hashes'", response.headers["Content-Security-Policy"])
        self.assertIn("sha256-SI4XQnc/9AWQkyG4KUZRPynC67aXcU2DL8cqNOunJcc=", response.headers["Content-Security-Policy"])
        self.assertIn(b'name="csrf_token" value="', response.data)

    def test_edit_rejects_invalid_update_and_is_rate_limited(self):
        device_id = "3D:AF:09:7F:00:02"
        token = self.csrf_token(f"/edit/{device_id}")
        headers = {"X-CSRFToken": token}
        invalid_record = {**valid_record(), "IP": "256.1.1.1"}
        response = self.client.post(
            f"/edit/{device_id}",
            json={"identifier": device_id, "record": invalid_record},
            headers=headers,
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["field"], "device_ip")

        statuses = []
        for index in range(4):
            record = valid_record()
            record["Name"] = f"Updated Router {index}"
            statuses.append(
                self.client.post(
                    f"/edit/{device_id}",
                    json={"identifier": device_id, "record": record},
                    headers=headers,
                ).status_code
            )
        statuses.append(
            self.client.post(
                f"/edit/{device_id}",
                json={"identifier": device_id, "record": valid_record()},
                headers=headers,
            ).status_code
        )
        self.assertEqual(statuses, [200, 200, 200, 200, 429])

    def test_delete_requires_csrf_and_removes_record_atomically(self):
        device_id = "3D:AF:09:7F:00:02"
        url = f"/delete/{device_id}"
        self.assertEqual(self.client.post(url).status_code, 400)
        token = self.csrf_token("/elements")
        response = self.client.post(url, data={"csrf_token": token})
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(device_id, application.datos_json)
        saved = json.loads(application.API_JSON_PATH.read_text(encoding="utf-8"))
        self.assertNotIn(device_id, saved)
        table = self.client.get("/elements")
        self.assertIn(b"Device deleted successfully", table.data)

    def test_delete_is_rate_limited(self):
        token = self.csrf_token("/elements")
        device_ids = list(application.datos_json)[:6]
        statuses = [
            self.client.post(
                f"/delete/{device_id}", data={"csrf_token": token}
            ).status_code
            for device_id in device_ids
        ]
        self.assertEqual(statuses, [302, 302, 302, 302, 302, 429])

    def test_add_rate_limit(self):
        token = self.csrf_token("/add")
        record = valid_record()
        headers = {"X-CSRFToken": token}
        statuses = []
        for index in range(1, 7):
            payload = {
                "identifier": f"AA:BB:CC:DD:EF:{index:02X}",
                "record": record,
            }
            statuses.append(self.client.post("/add", json=payload, headers=headers).status_code)
        self.assertEqual(statuses, [201, 201, 201, 201, 201, 429])

    def test_security_headers_and_auth_routes_are_absent(self):
        page = self.client.get("/elements")
        self.assertEqual(page.headers["X-Frame-Options"], "DENY")
        self.assertIn("Content-Security-Policy", page.headers)
        self.assertIn("HttpOnly", page.headers["Set-Cookie"])
        self.assertEqual(self.client.get("/login").status_code, 404)
        self.assertEqual(self.client.get("/logout").status_code, 404)


if __name__ == "__main__":
    unittest.main()
