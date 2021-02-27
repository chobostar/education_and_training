# Operational patterns

## Bulkhead pattern
Preventing systemic failure. Elements of an application are isolated into pools so that if one fails, the others will continue to function.

Use this pattern to:
- Isolate resources used to consume a set of backend services, especially if the application can provide some level of functionality even when one of the services is not responding.
- Isolate critical consumers from standard consumers.
- Protect the application from cascading failures.

This pattern may not be suitable when:
- Less efficient use of resources may not be acceptable in the project.
- The added complexity is not necessary

## Links:
- https://docs.microsoft.com/en-us/azure/architecture/patterns/bulkhead



