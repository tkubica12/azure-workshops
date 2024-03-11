# Azure FrontDoor DR strategy

Note that **CDNs can fail too**.

Key ideas:
- Pretty much all CDNs are incredibly redundant and distributed and in general **work extremely well**. Episodic approach should not be confused with statistics (I know a person who practiced healthy life style and died at 40 and also know person who smoked, drunk and died happily at 90 - sure both do exist, sure both are not common sample).
- **SLAs** in terms of money back of all such services **suck** - you are lucky to get few % back from your monthly bill of this specific service if they fail. Given your app is down if this service fail, SLAs pretty much do not matter.
- Multi-CDN increase complexity, but lowers your risk. If done in DR way it is not all that difficult. Note that **CDN failures are pretty much never complete**, almost never down for all users - most of the time things get slow for some (up to beyond usability)., dead for few, ok for most. Therefore automated response is difficult and risky - use good monitoring, but do not automate failover between CDNs.

In this demo:
- I use static configuration on Public DNS with 1 minute TTL to send traffic to:
  - FrontDoor - primary
  - Application Gateway - secondary (does not have to be predeployed, therefore there are now cloud consumption costs on top)
- So - is DNS "single point of failure" now?
  - Could be in theory, unless you point your DNS registrar NS records to two different DNS services like Azure Public DNS and something else
  - Do not use 60 seconds TTL on DNS, that is too aggressive for real world, target 5 minutes as an example