# iTRAP - The Banana API
 Interface for Touch Remote Application Programming

## Introduction
Banana is a RESTful API intended to provide a standardized remote access protocol to Derivative's TouchDesigner. While the Python API provides users extensive capabilities from within TouchDesigner, and ample forms of communication have native operators, there is no defacto way to remote into a TouchDesigner instance. Banana is an attempt to remedy this. Much of the Python API is now accessible through RESTful HTTP calls, and there is a large interface for interacting with operators and parameters in a way that makes it easy when outside of the TouchDesigner environment, such as ID maps, NAPs, and more. Additionally, the iTRAP interface is can be extended through the Monkey API, which allows users to leverage the tools already in place for routing API call, extracting parameters, and validating data.
