# Crossplane Terminology

https://crossplane.io/docs/v1.9/concepts/terminology.html

a distinct type - 'Pascal Case', e.g. “RDSInstance”

classes of types - “managed resource”

A Composition (higher level “composite resource”) tells Crossplane 
“when someone creates composite resource X, you should respond by creating resources Y and Z”.

a composite resources (XRs) as database entries, while an Composite Resource Definition (XRD) is a database schema.

Managed resources are the building blocks of Crossplane.

Packages (configurations and providers) extend Crossplane, either with support for new kinds of composite resources and claims:
- A configuration extends Crossplane by installing conceptually related groups of XRDs and Compositions
- A provider extends Crossplane by installing controllers for new kinds of managed resources (AWS provider)

