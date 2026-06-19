# main.tf - Ρύθμιση OpenTofu
provider "aws" {
  region = "eu-central-1" # Επιλέγουμε να νοικιάσουμε server στην Ευρώπη
}

resource "aws_instance" "microk8s_server" {
  ami           = "ami-0ec7f9846da69de33" # Ο κωδικός για το λειτουργικό σύστημα Ubuntu
  instance_type = "t3.medium"             # Το μέγεθος του υπολογιστή (επεξεργαστής/RAM)

  tags = {
    Name = "Fuel-Logistics-MicroK8s-Node" # Το όνομα που θα φαίνεται στο Cloud
  }
}