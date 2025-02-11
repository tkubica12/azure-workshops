locals {
  genai_policy = <<POLICY
<policies>
    <inbound>
        <base />
        <!-- Getting the main variable where we keep the list of backends. The cache is specific to the current API to avoid cross-contamination. -->
        <cache-lookup-value key="@("listBackends-" + context.Api.Id)" variable-name="listBackends" />
        <!-- If we can't find the variable, initialize it -->
        <choose>
            <when condition="@(context.Variables.ContainsKey("listBackends") == false)">
                <set-variable name="listBackends" value="@{
                    // -------------------------------------------------
                    // ------- Explanation of backend properties -------
                    // -------------------------------------------------
                    // "url":          Your backend url
                    // "priority":     Lower value means higher priority over other backends. 
                    //                 If you have more one or more Priority 1 backends, they will always be used instead
                    //                 of Priority 2 or higher. Higher values backends will only be used if your lower values (top priority) are all throttling.
                    // "isThrottling": Indicates if this endpoint is returning 429 (Too many requests) currently
                    // "retryAfter":   We use it to know when to mark this endpoint as healthy again after we received a 429 response

                    JArray backends = new JArray();
                    backends.Add(new JObject()
                    {
                        { "url", "${azapi_resource.ai_service_p1.output.properties.endpoints["OpenAI Language Model Instance API"]}" },
                        { "priority", 1},
                        { "isThrottling", false }, 
                        { "retryAfter", DateTime.MinValue } 
                    });

                    backends.Add(new JObject()
                    {
                        { "url", "${azapi_resource.ai_service_p2.output.properties.endpoints["OpenAI Language Model Instance API"]}" },
                        { "priority", 2},
                        { "isThrottling", false }, 
                        { "retryAfter", DateTime.MinValue } 
                    });

                    return backends;   
                }" />
                <!-- And store the variable into cache again -->
                <cache-store-value key="@("listBackends-" + context.Api.Id)" value="@((JArray)context.Variables["listBackends"])" duration="60" />
            </when>
        </choose>
        <authentication-managed-identity resource="https://cognitiveservices.azure.com" output-token-variable-name="msi-access-token" ignore-error="false" client-id="${azurerm_user_assigned_identity.main.client_id}" />
        <set-header name="Authorization" exists-action="override">
            <value>@("Bearer " + (string)context.Variables["msi-access-token"])</value>
        </set-header>
        <set-variable name="backendIndex" value="-1" />
        <set-variable name="remainingBackends" value="1" />
    </inbound>
    <backend>
        <retry condition="@(context.Response != null && (context.Response.StatusCode == 401 || context.Response.StatusCode == 429 || context.Response.StatusCode >= 500) && (int.Parse((string)context.Variables["remainingBackends"])) > 0)" count="50" interval="0">
            <!-- Before picking the backend, let's verify if there is any that should be set to not throttling anymore -->
            <set-variable name="listBackends" value="@{
                JArray backends = (JArray)context.Variables["listBackends"];

                for (int i = 0; i < backends.Count; i++)
                {
                    JObject backend = (JObject)backends[i];

                    if (backend.Value<bool>("isThrottling") && DateTime.Now >= backend.Value<DateTime>("retryAfter"))
                    {
                        backend["isThrottling"] = false;
                        backend["retryAfter"] = DateTime.MinValue;
                    }
                }

                return backends; 
            }" />
            <cache-store-value key="@("listBackends-" + context.Api.Id)" value="@((JArray)context.Variables["listBackends"])" duration="60" />
            <!-- This is the main logic to pick the backend to be used -->
            <set-variable name="backendIndex" value="@{
                JArray backends = (JArray)context.Variables["listBackends"];

                int selectedPriority = Int32.MaxValue;
                List<int> availableBackends = new List<int>();

                for (int i = 0; i < backends.Count; i++)
                {
                    JObject backend = (JObject)backends[i];

                    if (!backend.Value<bool>("isThrottling"))
                    {
                        int backendPriority = backend.Value<int>("priority");

                        if (backendPriority < selectedPriority)
                        {
                            selectedPriority = backendPriority;
                            availableBackends.Clear();
                            availableBackends.Add(i);
                        } 
                        else if (backendPriority == selectedPriority)
                        {
                            availableBackends.Add(i);
                        }
                    }
                }

                if (availableBackends.Count == 1)
                {
                    return availableBackends[0];
                }
            
                if (availableBackends.Count > 0)
                {
                    //Returns a random backend from the list if we have more than one available with the same priority
                    return availableBackends[new Random().Next(0, availableBackends.Count)];
                }
                else
                {
                    //If there are no available backends, the request will be sent to the first one
                    return 0;    
                }
                }" />
            <set-variable name="backendUrl" value="@(((JObject)((JArray)context.Variables["listBackends"])[(Int32)context.Variables["backendIndex"]]).Value<string>("url") + "openai")" />
            <set-backend-service base-url="@((string)context.Variables["backendUrl"])" />
            <forward-request buffer-request-body="true" />
            <choose>
                <!-- In case we got a 401, 429, or 5xx from a backend, update the list with its status -->
                <when condition="@(context.Response != null && (context.Response.StatusCode == 401 || context.Response.StatusCode == 429 || context.Response.StatusCode >= 500) )">
                    <cache-lookup-value key="@("listBackends-" + context.Api.Id)" variable-name="listBackends" />
                    <set-variable name="listBackends" value="@{
                        JArray backends = (JArray)context.Variables["listBackends"];
                        int currentBackendIndex = context.Variables.GetValueOrDefault<int>("backendIndex");
                        int retryAfter = Convert.ToInt32(context.Response.Headers.GetValueOrDefault("Retry-After", "-1"));

                        if (retryAfter == -1)
                        {
                            retryAfter = Convert.ToInt32(context.Response.Headers.GetValueOrDefault("x-ratelimit-reset-requests", "-1"));
                        }

                        if (retryAfter == -1)
                        {
                            retryAfter = Convert.ToInt32(context.Response.Headers.GetValueOrDefault("x-ratelimit-reset-tokens", "10"));
                        }

                        JObject backend = (JObject)backends[currentBackendIndex];
                        backend["isThrottling"] = true;
                        backend["retryAfter"] = DateTime.Now.AddSeconds(retryAfter);

                        return backends;      
                    }" />
                    <cache-store-value key="@("listBackends-" + context.Api.Id)" value="@((JArray)context.Variables["listBackends"])" duration="60" />
                    <set-variable name="remainingBackends" value="@{
                        JArray backends = (JArray)context.Variables["listBackends"];

                        int remainingBackends = 0;

                        for (int i = 0; i < backends.Count; i++)
                        {
                            JObject backend = (JObject)backends[i];

                            if (!backend.Value<bool>("isThrottling"))
                            {
                                remainingBackends++;
                            }
                        }

                        return remainingBackends;
                    }" />
                </when>
            </choose>
        </retry>
    </backend>
    <outbound>
        <base />
        <!-- This will return the used backend URL in the HTTP header response. Remove it if you don't want to expose this data -->
        <set-header name="x-openai-backendurl" exists-action="override">
            <value>@(context.Variables.GetValueOrDefault<string>("backendUrl", "none"))</value>
        </set-header>
    </outbound>
    <on-error>
        <base />
    </on-error>
</policies>
POLICY

  silver_policy = <<POLICY
<policies>
    <inbound>
        <base />
        <azure-openai-token-limit
            counter-key="@(context.Subscription.Id)"
            tokens-per-minute="1000" 
            estimate-prompt-tokens="true" 
            remaining-tokens-variable-name="remainingTokens" />
    </inbound>
    <outbound>
        <base />
    </outbound>
</policies>
POLICY

  caching_policy = <<POLICY
<policies>
    <inbound>
        <base />
        <set-backend-service backend-id="${azapi_resource.embeddings_backend.name}" />
        <authentication-managed-identity resource="https://cognitiveservices.azure.com/" />
        <azure-openai-semantic-cache-lookup
            score-threshold="0.8"
            embeddings-backend-id="${azapi_resource.embeddings_backend.name}"
            embeddings-backend-auth="system-assigned"
            ignore-system-messages="false"
            max-message-count="2">
            <vary-by>@(context.Subscription.Id)</vary-by>
        </azure-openai-semantic-cache-lookup>
    </inbound>
    <outbound>
        <azure-openai-semantic-cache-store duration="120" />
        <base />
    </outbound>
</policies>
POLICY
}

resource "azurerm_api_management_api_policy" "genai_policy" {
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  api_name            = azurerm_api_management_api.openai.name
  xml_content         = local.genai_policy
}

resource "azurerm_api_management_product_policy" "silver_policy" {
  product_id          = azurerm_api_management_product.silver.product_id
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  xml_content         = local.silver_policy
}

resource "azurerm_api_management_product_policy" "caching_policy" {
  product_id          = azurerm_api_management_product.caching.product_id
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  xml_content         = local.caching_policy
}

