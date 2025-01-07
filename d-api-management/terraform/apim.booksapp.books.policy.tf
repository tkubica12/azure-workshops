locals {
  policy_books = <<XML
<policies>
    <!-- Throttle, authorize, validate, cache, or transform the requests -->
    <inbound>
        <set-backend-service base-url="https://${azurerm_container_app.books_api.ingress[0].fqdn}" />
        <base />
    </inbound>
    <!-- Control if and how the requests are forwarded to services  -->
    <backend>
        <base />
    </backend>
    <!-- Customize the responses -->
    <outbound>
        <base />
    </outbound>
    <!-- Handle exceptions and customize error responses  -->
    <on-error>
        <base />
    </on-error>
</policies>
XML
}


