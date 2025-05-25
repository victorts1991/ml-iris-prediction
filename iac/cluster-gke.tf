terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

variable "project_id" {
  description = "The GCP project ID."
  type        = string
  # default = "ml-iris-prediction"
}

provider "google" {
  project = var.project_id
  region  = "us-central1"
}

resource "google_container_cluster" "primary" {
  name             = "cluster-ml-iris-prediction"
  location         = "us-central1"
  enable_autopilot = true
  network          = "default"
  subnetwork       = "projects/${var.project_id}/regions/us-central1/subnetworks/default" 
}