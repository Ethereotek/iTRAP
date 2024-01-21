# iTRAP - The Banana API
 Interface for Touch Remote Application Programming

## Introduction
Banana is a RESTful API intended to provide a standardized remote access protocol to Derivative's TouchDesigner. While the Python API provides users extensive capabilities from within TouchDesigner, and there are native operators for almost any major communication protocol you can think of, there is no defacto way to remote into a TouchDesigner instance. Banana is an attempt to remedy this. Much of the Python API is now accessible through RESTful HTTP calls, and there is a large interface for interacting with operators and parameters in a way that makes it easy when outside of the TouchDesigner environment, such as ID maps, NAPs, and more. Additionally, the iTRAP interface can be extended through the Monkey API, which allows users to leverage the tools already in place for routing API calls, extracting parameters, and validating data.

## Getting Started 
The Banana API is served through iTRAP - Interface for Touch Remote Access Protocol - a dependency-free component that you can simply drag and drop from the `/Build` directory into your project.

- Select the IP Address of the interface you wish to use.
- By default, iTRAP is accessible via port 29980. It is best to keep this default setting, but you can change it if you wish. The Swagger documentation is served on port 8000.
- Map OP ID allows you a rough and dirty way of exposing a set of operators to the outside world. This is essentially a list that can a developer can query with an API call to get relevant information for interacting with the OPs that you want.
- Every call in the Banana API is authenticated with a bearer token. Each token is associated with a user and a set of scopes. Select the user to reveal their API key.
- At any time, you can regenerate that user's key.

## Documentation
The Banana API is documented with Swagger, which can be accessed on port 8000. this should tell you everything you need to know about what calls you can make, what they do, and the data they return.

## User and Scope Configuration
Every API Key is associated with a user and a set of scopes and exclusions defined by a permissions.json document. Users' keys are easily generated and regenerated with associated parameters on the Component.

Scopes can easily be derived from the URI's, and generally consist of a class, object and method. Example classes would be `app`, `project`, and `namedPars`. The object simply narrows that scope, such as `app.power`, and the method refers to the HTTP method, so the scope `app.power.put` would allow the API key access to change the application power state.

Scopes can be defined using a wild card, for example, `project.*` allows full access to the project class, whereas `project.*.get` allows GET access to the full project class.

Exclusions can also be defined, which override scopes. If a scope of `app.*` is defined, you can create the exclusion `app.power.put` which prevent PUT's to the `app.power` object.

The configuration must be defined in the `permissions_config` DAT. It's recommended to keep the config as an external file and sync it in the DAT.

An example permissions configuration:
```
{
	"admin": {
		"scopes": [
			"app.*",
			"project.*",
			"ops.*",
			"namedOps.*",
			"monitors.*",
			"project.*",
			"ui.*",
			"namedPars.*",
			"permissions"

		],
		"key": "b9a1ad0e-f386-11ed-815a-9cfce837ddb7"
	},
	"user1": {
		"scopes": [
			"app.*",
			"project.*",
			"permissions"
		],
		"exclusions": [
			"app.*.put",
			"project.*.put"
		],
		"key": "427ebe80-f386-11ed-aecc-9cfce837ddb7"
	}
}
```

Note that the `permissions` scope is automagically added. The `key` is also added by the key generation, and is not required to be entered. If a key is added, it will simply be overwritten when a Permission object is created.

## Map Operator ID's
To expose operators through their ID's, pulse the `Map OP ID` parameter. Drag and drop an operator into the `Expression` parameter in the window that opens. It simply creates a table of absolute paths that will calculate their ID's when `GET /api/banana/op/opIdMap` is called. This should be called any time the project is restarted, since operator ID's will change between project loads. For a more sophisticated solution, use Named Operators.

## Named Operators and Parameters
The Banana API is designed to be used in conjunction with [NAPs](https://github.com/Ethereotek/NAPs), which allows you to create project-wide shortcuts, or aliases, to operators and parameters. A guide to using NAPs can be found in the README on the NAPs github page. It is not required to use NAPs, however, and any NAPs relevant endpoints will simply return 404 if it is not employed.

## Postman Spec
In *`Documentation/Postman`* you can find a postman environment and collection. This contains every endpoint and supported method. They are configured to work with the `example.toe` project.

To get started, simply import the environment and collection, update the `token` variable in the environment with one you generated. Operator ID's are not consistent between project loads, so any endpoints that use it may need editing. There are also a couple that require directory paths on the host's machine, so you will have to edit those to match your configuration.

### Updates 21 Jan 2024
- Added call for pulsing a parameter (`[POST] /op/par/pulse`)
- Bug fixes and updated response objects to some existing calls
- Security is now optional via a parameter on the iTRAP tox. Switch this off to bypass requiring a token for requests
- CORS error when accessing Swagger doc from different machine resolved
- Updates to Swagger API documentation
