from server import run_server
from client import run_client


def main():
    while True:
        print("Choose mode:")
        print("1. Run as Server")
        print("2. Run as Client")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            print("Starting server...")
            run_server()
            break

        elif choice == "2":
            print("Starting client...")
            run_client()
            break

        elif choice == "0":
            print("Exiting program.")
            break

        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()
