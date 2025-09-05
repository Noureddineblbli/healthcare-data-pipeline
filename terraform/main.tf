# -----------------------------------------------------------------------------
# TERRAFORM CONFIGURATION
# -----------------------------------------------------------------------------
# Specifies the settings for Terraform itself, including the providers
# required to manage your infrastructure.

terraform {
  required_providers {
    snowflake = {
      source  = "snowflakedb/snowflake"
      version = "~> 0.93.0"
    }
  }
}

# -----------------------------------------------------------------------------
# PROVIDER CONFIGURATION
# -----------------------------------------------------------------------------
# Configures the Snowflake provider with the credentials needed to connect
# to your account. It references the variables defined in variables.tf.

provider "snowflake" {
  account  = var.snowflake_account
  user     = var.snowflake_user
  password = var.snowflake_password
  role     = var.snowflake_role
}


# -----------------------------------------------------------------------------
# RESOURCE DEFINITIONS
# -----------------------------------------------------------------------------
# These blocks define the actual Snowflake resources that Terraform will create
# and manage.
# -----------------------------------------------------------------------------

# --- VIRTUAL WAREHOUSE ---
# Creates the compute resource for running queries and data processing.
resource "snowflake_warehouse" "main" {
  name           = var.warehouse_name
  warehouse_size = var.warehouse_size
  auto_suspend   = 60 # Suspends the warehouse after 60 seconds of inactivity to save credits.
  auto_resume    = true
  initially_suspended = true
}

# --- DATABASE ---
# Creates the main database to hold all our healthcare data.
resource "snowflake_database" "main" {
  name = var.database_name
}

# --- SCHEMAS ---
# Creates the RAW, BRONZE, SILVER, and GOLD schemas within the main database.
# This uses a for_each loop to create a resource for each name in the var.schema_names list.
resource "snowflake_schema" "main" {
  for_each = toset(var.schema_names)

  database = snowflake_database.main.name
  name     = each.key
  comment  = "Schema for ${lower(each.key)} data in the pipeline."
}

# --- ROLES ---
# Creates the functional roles for access control. Permissions will be granted later.
resource "snowflake_role" "loader" {
  name = "LOADER_ROLE"
  comment = "Role for services that load raw data into Snowflake (e.g., NiFi)."
}

resource "snowflake_role" "transformer" {
  name = "TRANSFORM_ROLE"
  comment = "Role for services that transform data (e.g., Spark, dbt)."
}

resource "snowflake_role" "analyst" {
  name = "ANALYST_ROLE"
  comment = "Role for end-users and BI tools that perform analysis."
}