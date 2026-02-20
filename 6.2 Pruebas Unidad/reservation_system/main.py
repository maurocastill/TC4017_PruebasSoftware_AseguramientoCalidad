"""Script to test the Hotel Management System with real JSON files."""
from src.hotel import Hotel
from src.customer import Customer
from src.reservation import Reservation


def run_system_test():
    """Executes a series of real operations to generate JSON files."""
    print("Iniciando prueba del Sistema de Gestión Hotelera...")

    # 1. Crear un Hotel
    print("\n[1] Creando Hotel...")
    Hotel.create_hotel(1, "Ocean View Resort", "Miami", 10)
    print("Hotel creado con 10 habitaciones.")

    # 2. Crear un Cliente
    print("\n[2] Creando Cliente...")
    Customer.create_customer(1, "Alice Smith", "alice@example.com")
    print("Cliente Alice registrado.")

    # 3. Hacer una Reserva
    print("\n[3] Generando Reserva...")
    # Intentamos reservar el hotel 1 para el cliente 1 con la reserva 100
    Reservation.create_reservation(100, 1, 1)
    print("Reserva completada. Habitaciones disponibles reducidas.")


if __name__ == "__main__":
    run_system_test()
