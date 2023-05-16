# iTRAP - The Banana API
 Interface for Touch Remote Application Programming

## Introduction
Banana is a RESTful API intended to provide a standardized remote access protocol to Derivative's TouchDesigner. While the Python API provides users extensive capabilities from within TouchDesigner, and there native operators almost any major communication protocol you can think of, there is no defacto way to remote into a TouchDesigner instance. Banana is an attempt to remedy this. Much of the Python API is now accessible through RESTful HTTP calls, and there is a large interface for interacting with operators and parameters in a way that makes it easy when outside of the TouchDesigner environment, such as ID maps, NAPs, and more. Additionally, the iTRAP interface can be extended through the Monkey API, which allows users to leverage the tools already in place for routing API calls, extracting parameters, and validating data.

## Getting Started 
The Banana API is served through iTRAP - Interface for Touch Remote Access Protocol - a dependency-free component that you can simply drag and drop into your project.

- Select the IP Address of the interface you wish to use.
- By default, iTRAP is accessible via port 29980. It is best to keep this default setting, but you can change it if you wish. The Swagger documentation is served on port 8000.
- Map OP ID allows you a rough and dirty way of exposing a set of operators to the outside world. This is essentially a list that can a developer can query with an API call to get relevant information for interacting with the OPs that you want.
- Every call in the Banana API is authenticated with a bearer token. Each token is associated with a user and a set of scopes. Select the user to reveal their API key.
- At any time, you can regenerate that user's key.

## Documentation
The Banana API is documented with Swagger, which can be accessed on port 8000. this should tell you everything you need to know about what calls you can make, what they do, and the data they return.

## User and Scope Configuration
Scopes can easily be derived from the URI's, and generally consist of a class, object and method. Example classes would be `app`, `project`, and `namedPars`. The object simply narrows that scope, such as `app.power`, and the method refers to the HTTP method, so the scope `app.power.put` would allow the API key access to change the application power state.

Scopes can be defined using a wild card, for example, `project.*` allows full access to the project class, whereas `project.*.get` allows GET access to the full project class.

Exclusions can also be defined, which override scopes. If a scope of `app.*` is defined, you can create the exclusion `app.power.put` which prevent PUT's to the `app.power` object.

The configuration must be defined in the `permissions_config` DAT. It's recommended to keep the config as an external file and sync it in the DAT.

## Named Operators and Parameters
The Banana API is designed to be used in conjunction with [NAPs](https://github.com/Ethereotek/NAPs), which allows you to create project-wide shortcuts, or aliases, to operators and parameters. A guide to using NAPs can be found in the README on the NAPs github page. It is not required to use NAPs, however, and any NAPs relevant endpoints will simply return 404 if it is not employed.