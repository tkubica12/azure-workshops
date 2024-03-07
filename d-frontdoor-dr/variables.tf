variable "app_location" {
  description = "The location of the application"
  type        = string
}

variable "appgw_location" {
  description = "The location of the application gateway"
  type        = string
}

variable "client_locations" {
  description = "The locations of the clients"
  type        = list(string)
  default     = []
}

variable "web_fqdn" {
  description = "FQDN of web application as used by clients"
  type        = string
  default     = "web.demo.tkubica.biz"
}

variable "dns_zone_id" {
  description = "Resource ID of the DNS zone in Azure"
  type        = string
  default     = "/subscriptions/d3b7888f-c26e-4961-a976-ff9d5b31dfd3/resourceGroups/base/providers/Microsoft.Network/dnsZones/demo.tkubica.biz"
}

variable "deploy_appgw" {
  description = "Whether to deploy the application gateway"
  type        = bool
}

variable "traffic_via_fd" {
  description = "Whether to route traffic via Front Door"
  type        = bool
  default     = true
}
