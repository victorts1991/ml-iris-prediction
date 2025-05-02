terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = "ml-iris-prediction"
  region  = "us-central1"
}

resource "google_container_cluster" "primary" {
  name             = "cluster-ml-iris-prediction"
  location         = "us-central1"
  enable_autopilot = true
  network          = "default"
  subnetwork       = "projects/ml-iris-prediction/regions/us-central1/subnetworks/default"
}