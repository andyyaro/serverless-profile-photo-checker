# scratch-only: pin the provider to the version already on disk (not part of the repo)
terraform {
  required_providers {
    aws = { source = "hashicorp/aws", version = "6.15.0" }
  }
}
