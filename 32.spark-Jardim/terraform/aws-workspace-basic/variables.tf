variable "prefix" {
  type        = string
  description = "Prefix"
}

variable "databricks_account_id" {
  type        = string
  description = "Databricks Account ID"
}

variable "databricks_client_id" {
  type        = string
  description = "Databricks Client ID"
}

variable "databricks_client_secret" {
  type        = string
  description = "Databricks Client Secret"
}


variable "tags" {
  default     = {}
  type        = map(string)
  description = "Optional tags to add to created resources"
}

variable "cidr_block" {
  description = "IP range for AWS VPC"
  type        = string
  default     = "10.4.0.0/16"
}

variable "region" {
  default     = "us-west-1"
  type        = string
  description = "AWS region to deploy to"
}
