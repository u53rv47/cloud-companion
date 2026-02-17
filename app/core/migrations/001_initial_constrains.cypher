CREATE CONSTRAINT org_id IF NOT EXISTS
FOR (o:Organization)
REQUIRE o.id IS UNIQUE;

CREATE CONSTRAINT cloud_account_unique IF NOT EXISTS
FOR (c:CloudAccount)
REQUIRE (c.provider, c.account_id) IS UNIQUE;

CREATE CONSTRAINT api_key_id IF NOT EXISTS
FOR (k:APIKey)
REQUIRE k.id IS UNIQUE;
