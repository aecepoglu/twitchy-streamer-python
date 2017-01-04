Feature: Client version must be compatible with server

Scenario: Client is compatible with server
Given a server exists
And it will verify my version-check
When it checks for version
Then it should successfully proceed

Scenario: Client is compatible with server but a newer version exists
Given a server exists
And it verifies my version-check but a newer version exists
When it checks for version
Then it should notify me about the newer version
And it should successfully proceed

Scenario: Client is incompatible with server
Given a server exists
And it doesn't support my version
When it checks for version
Then it should fail and show a warning
