
class Vehicle:
    def __init__(self, vehicle_type):
        #
        Initialize the Vehicle class.

        Args:
            vehicle_type (str): The type of vehicle (e.g., car, truck, plane, boat, broomstick)
        #
        self.vehicle_type = vehicle_type

    def display_vehicle_info(self):
        #
        Display the vehicle type.
        #
        print(f"Vehicle type: {self.vehicle_type}")


# Define the Automobile subclass
class Automobile(Vehicle):
    def __init__(self, vehicle_type, year, make, model, doors, roof):
        #
        Initialize the Automobile class.

        Args:
            vehicle_type (str): The type of vehicle (e.g., car, truck, plane, boat, broomstick)
            year (int): The year of the automobile
            make (str): The make of the automobile
            model (str): The model of the automobile
            doors (int): The number of doors (2 or 4)
            roof (str): The type of roof (solid or sun roof)
        #
        super().__init__(vehicle_type)
        self.year = year
        self.make = make
        self.model = model
        self.doors = doors
        self.roof = roof

    def display_automobile_info(self):
        #
        Display the automobile information.
        #
        self.display_vehicle_info()
        print(f"Year: {self.year}")
        print(f"Make: {self.make}")
        print(f"Model: {self.model}")
        print(f"Number of doors: {self.doors}")
        print(f"Type of roof: {self.roof}")


def main():
    # Accept user input for a car
    vehicle_type = "car"
    year = int(input("Enter the year: "))
    make = input("Enter the make: ")
    model = input("Enter the model: ")
    doors = int(input("Enter the number of doors (2 or 4): "))
    while doors not in [2, 4]:
        doors = int(input("Invalid input. Please enter 2 or 4: "))
    roof = input("Enter the type of roof (solid or sun roof): ")
    while roof.lower() not in ["solid", "sun roof"]:
        roof = input("Invalid input. Please enter solid or sun roof: ")

    # Create an Automobile object and display the information
    automobile = Automobile(vehicle_type, year, make, model, doors, roof)
    print("\nAutomobile Information:")
    automobile.display_automobile_info()


if __name__ == "__main__":
    main()