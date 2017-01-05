Feature: Client version must be compatible with server

Scenario: Client is compatible with server
Given a server at "http://theserver:3333" responds to "GET" "/api/version" with "1.0.0"
And my config has "http://theserver:3333/path/to/resource?key=123&a=b&c=d" as "publishLink"
And my config has "1.0.0" as "version"
When it checks for version
Then it should succeed

Scenario: Client is compatible with server but a newer version exists
Given a server at "http://theserver:3333" responds to "GET" "/api/version" with "1.14.0 2.5.0"
And my config has "http://theserver:3333/path/to/resource" as "publishLink"
And my config has "1.5.3" as "version"
When it checks for version
Then it should succeed
And it should notify me about the newer version

Scenario: Client is incompatible with server
Given a server at "http://theserver:3333" responds to "GET" "/api/version" with "2.0.0"
And my config has "http://theserver:3333/path/to/resource" as "publishLink"
And my config has "1.0.0" as "version"
When it checks for version
Then it should fail
And give me version incompatibility error
