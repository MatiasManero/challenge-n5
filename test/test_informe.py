import json
from pathlib import Path
from test.config import test_client


def read_file(file_path):
    """Se lee archivo de datos json
    Args:
        file_path: ruta del archivo
    """
    with file_path.open("r") as f:
        data = json.load(f)
    return data


def test_get_generar_informe(test_client):
    """Se prueba generar un informe de una persona"""

    email = "persona1@persona.com"

    vehiculo_path = Path(__file__).parent / "seed" / "vehiculos.json"
    personas_path = Path(__file__).parent / "seed" / "personas.json"

    vehiculos = read_file(vehiculo_path)
    personas = read_file(personas_path)

    persona = [entry for entry in personas if entry["correo_electronico"] == email][0]
    vehiculo_persona = [entry["placa"] for entry in vehiculos if entry["persona_id"] == persona["id"]]

    response = test_client.get(f"/generar_informe?email={email}")

    assert response.status_code == 200
    infracciones = response.json()

    for infraccion in infracciones:
        assert "id" not in infraccion
        assert "persona_id" not in infraccion
        assert infraccion["placa_patente"] in vehiculo_persona


def test_post_infraccion(test_client):
    """Se prueba la carga de una infraccion correcta"""
    email = "persona3@persona.com"

    # Se verifica que no exista ninguna infraccion para el email solicitado
    response = test_client.get(f"/generar_informe?email={email}")
    assert response.status_code == 200
    informe_antes = len(response.json())

    infraccion = {
        "placa_patente": "MN123QZ",
        "timestamp": "2024-12-12T12:12:12.814+03:00",
        "comentarios": "TEST INFRACCION by TEST"
    }

    response = test_client.post(f"/cargar_infraccion", json=infraccion)

    assert response.status_code == 200

    # Verificamos que se haya cargado correctamente la infraccion
    response = test_client.get(f"/generar_informe?email={email}")
    assert response.status_code == 200
    assert len(response.json()) == informe_antes + 1


def test_post_infraccion_not_patent(test_client):
    """Se prueba la carga de una infraccion con una patente inexistente"""
    infraccion = {
        "placa_patente": "123444",
        "timestamp": "2024-12-12T12:12:12.814+03:00",
        "comentarios": "TEST INFRACCION by TEST"
    }

    response = test_client.post(f"/cargar_infraccion", json=infraccion)

    assert response.status_code == 404
    assert response.json()["detail"] == f"Patente {infraccion['placa_patente']} no encontrada"
