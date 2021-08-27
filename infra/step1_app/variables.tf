locals {
  namespace-   = var.runiac_namespace == "" ? "" : "${var.runiac_namespace}-"
  is_ephemeral = var.runiac_namespace != ""
  is_prod      = var.runiac_environment == "prod"
}

variable "runiac_account_id" {
  type = string
}

variable "runiac_region" {
  type = string
}

variable "runiac_environment" {
  type = string
}

variable "runiac_namespace" {
  type = string
}

variable "runiac_step" {
  type = string
}

variable "website_deploy_folder" {
  type    = string
  default = "../webapp_deploy"

}

variable "docker_image" {
  type    = string
  default = "askoptum"
}

variable "docker_tag" {
  type = string
}