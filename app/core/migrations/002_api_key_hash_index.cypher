CREATE INDEX api_key_hash IF NOT EXISTS
FOR (k:APIKey)
ON (k.hashed_key);
