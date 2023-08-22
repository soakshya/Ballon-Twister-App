import csv

 

class BalloonTwister:
    def __init__(self, name):
        self.name = name
        self.schedule = []

 

class Holiday:
    def __init__(self, name):
        self.name = name
        self.bookings = []

 

class BalloonTwiisterApp:
    def __init__(self):
        self.balloon_twisters = []
        self.holidays = []
        self.waiting_list = []

 

    def load_data(self):
        with open("BalloonTwisters.dat", "r") as twister_file:
            for line in twister_file:
                twister_name = line.strip()
                self.balloon_twisters.append(BalloonTwister(twister_name))

 

        with open("Holidays.dat", "r") as holiday_file:
            for line in holiday_file:
                holiday_name = line.strip()
                self.holidays.append(Holiday(holiday_name))

 

        with open("Schedule.csv", "r") as schedule_file:
            schedule_reader = csv.reader(schedule_file)
            for row in schedule_reader:
                customer_name, holiday_name, twister_name = row
                self._add_booking(customer_name, holiday_name, twister_name)

 

        # Load waiting list from file

 

    def save_data(self):
        with open("BalloonTwisters.dat", "w") as twister_file:
            for twister in self.balloon_twisters:
                twister_file.write(twister.name + "\n")

 

        with open("Holidays.dat", "w") as holiday_file:
            for holiday in self.holidays:
                holiday_file.write(holiday.name + "\n")

 

        with open("Schedule.csv", "w", newline="") as schedule_file:
            schedule_writer = csv.writer(schedule_file)
            for holiday in self.holidays:
                for booking in holiday.bookings:
                    schedule_writer.writerow([booking[0], holiday.name, booking[1]])

 

        # Save waiting list to file

 

    def _add_booking(self, customer_name, holiday_name, twister_name):
        # Helper method to add a booking to the appropriate twister and holiday
        for twister in self.balloon_twisters:
            if twister.name == twister_name:
                twister.schedule.append((customer_name, holiday_name))
                break
        for holiday in self.holidays:
            if holiday.name == holiday_name:
                holiday.bookings.append((customer_name, twister_name))
                break

 

    def schedule_balloon_twister(self, customer_name, holiday_name):
        available_twister = None
        for twister in self.balloon_twisters:
            if all((twister.name != booking[1] or holiday_name != booking[0]) for booking in twister.schedule):
                available_twister = twister
                break

 

        if available_twister:
            self._add_booking(customer_name, holiday_name, available_twister.name)
            print(f"Scheduled {available_twister.name} for {customer_name} on {holiday_name}.")
        else:
            self.waiting_list.append((customer_name, holiday_name))
            print(f"Added {customer_name} to waiting list for {holiday_name}.")

 

    def cancel_booking(self, customer_name, holiday_name):
        for holiday in self.holidays:
            if holiday.name == holiday_name:
                for booking in holiday.bookings:
                    if booking[0] == customer_name:
                        twister_name = booking[1]
                        holiday.bookings.remove(booking)
                        for twister in self.balloon_twisters:
                            if twister.name == twister_name:
                                twister.schedule.remove((customer_name, holiday_name))
                                if self.waiting_list:
                                    new_booking = self.waiting_list.pop(0)
                                    self.schedule_balloon_twister(new_booking[0], new_booking[1])
                                print(f"Booking for {customer_name} on {holiday_name} canceled.")
                                return
                print("Booking not found.")
                return

 

    def print_schedule(self, target):
        if target.lower() == "balloon twister":
            twister_name = input("Enter the name of the balloon twister: ")
            for twister in self.balloon_twisters:
                if twister.name == twister_name:
                    print(f"Schedule for {twister_name}:")
                    for booking in twister.schedule:
                        print(f"  - {booking[1]} for {booking[0]}")
                    return
            print("Balloon twister not found.")
        elif target.lower() == "holiday":
            holiday_name = input("Enter the name of the holiday: ")
            for holiday in self.holidays:
                if holiday.name == holiday_name:
                    print(f"Schedule for {holiday_name}:")
                    for booking in holiday.bookings:
                        print(f"  - {booking[0]} with {booking[1]}")
                    return
            print("Holiday not found.")
        else:
            print("Invalid target.")

 

    def signup_balloon_twister(self, twister_name):
        self.balloon_twisters.append(BalloonTwister(twister_name))
        print(f"Balloon twister {twister_name} signed up.")

 

    def dropout_balloon_twister(self, twister_name):
        for twister in self.balloon_twisters:
            if twister.name == twister_name:
                self.balloon_twisters.remove(twister)
                for booking in twister.schedule:
                    self.waiting_list.append(booking)
                    if self.waiting_list:
                        new_booking = self.waiting_list.pop(0)
                        self.schedule_balloon_twister(new_booking[0], new_booking[1])
                    print(f"Rescheduled booking for {booking[0]} on {booking[1]}.")
                print(f"Balloon twister {twister_name} has dropped out.")
                return
        print("Balloon twister not found.")

 

    def run(self):
        self.load_data()
        while True:
            print("\nMenu:")
            print("1. Schedule a balloon twister")
            print("2. Cancel a booking")
            print("3. Print schedule")
            print("4. Sign up a balloon twister")
            print("5. Drop out a balloon twister")
            print("6. Quit")

 

            choice = input("Enter your choice: ")

 

            if choice == "1":
                customer_name = input("Enter customer's name: ")
                holiday_name = input("Enter holiday's name: ")
                self.schedule_balloon_twister(customer_name, holiday_name)
            elif choice == "2":
                customer_name = input("Enter customer's name: ")
                holiday_name = input("Enter holiday's name: ")
                self.cancel_booking(customer_name, holiday_name)
            elif choice == "3":
                target = input("Enter 'balloon twister' or 'holiday': ")
                self.print_schedule(target)
            elif choice == "4":
                twister_name = input("Enter balloon twister's name: ")
                self.signup_balloon_twister(twister_name)
            elif choice == "5":
                twister_name = input("Enter balloon twister's name: ")
                self.dropout_balloon_twister(twister_name)
            elif choice == "6":
                self.save_data()
                print("Data saved. Exiting the program.")
                break
            else:
                print("Invalid choice. Please select a valid option.")

 

if __name__ == "__main__":
    app = BalloonTwiisterApp()
    app.run()