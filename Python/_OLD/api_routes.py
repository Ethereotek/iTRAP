api_routes = {
    "GET /api/v1/app/architecture": app.architecture,
    "GET /api/v1/app/build": app.build,
    "GET /api/v1/app/launchTime": app.launchTime,
    "GET /api/v1/app/osName": app.osName,
}
'''
    "GET /api/v1/app/power": getAppPower,
    "PUT /api/v1/app/power": putAppPower,
    "GET/api/v1/app/product": app.product,
    "GET /api/v1/app/version": app.version,
    "GET /api/v1/app/play": getAppPlay,
    "PUT /api/v1/app/play": putAppPlay,
    "GET /api/v1/app/stop": getAppStop,
    "PUT /api/v1/app/stop": putAppStop,

    "GET /api/v1/project/name": project.name,
    "GET /api/v1/project/saveVersion": project.saveVersion,

    "GET /api/v1/project/saveBuild": project.saveBuild,
    "GET /api/v1/project/saveTime": project.saveTime,
    "GET /api/v1/project/saveOSName": project.saveOSName,
    "GET /api/v1/project/saveOSVersion": project.saveOSVersion,
    "GET /api/v1/project/paths": getProjectPaths,
    "GET /api/v1/project/cookRate": getProjectCookRate,
    "PUT /api/v1/project/cookRate": putProjectCookRate,
    "GET /api/v1/project/realTime": getProjectRealTime,
    "PUT /api/v1/project/realTime": putProjectRealTime,
    "GET /api/v1/project/performOnStart": getProjectPerformOnStart,
    "PUT /api/v1/project/performOnStart": putProjectPerformOnStart,
    "POST /api/v1/project/load": postProjectLoad,
    "POST /api/v1/project/save": postProjectSave,
    "POST /api/v1/project/quit": postProjectQuit,

    "GET /api/v1/sys_info/numCPUs": sys_info.numCPUs,
    "GET /api/v1/sys_info/ram": sys_info.ram,
    "GET /api/v1/sys_info/numMonitors": sys_info.numMonitors,
    "GET /api/v1/sys_info/xres": sys_info.xres,
    "GET /api/v1/sys_info/yres": sys_info.yres,
    "GET /api/v1/sys_info/res": getSysInfoRes,
    "GET /api/v1/sys_info/tfs": sys_info.tfs,
    "GET /api/v1/sys_info/MIDIInputs": sys_info.MINIInputs,
    "GET /api/v1/sys_info/MIDIOutputs": sys_info.MIDIOuputs,
   
    "GET /api/v1/ui/masterVolume": getUIMasterVolume,
    "PUT /api/v1/ui/masterVolume": putUIMasterVolume,

    "GET /api/v1/monitors/height": monitors.height,
    "GET /api/v1/monitors/numMonitors": monitors.numMonitors,
    "POST /api/v1/monitors/refresh": postMonitorsRefresh,

    "GET /api/v1/op": getOp,
    "POST /api/v1/op": postOp,
    "DELETE /api/v1/op": deleteOp,
    "GET /api/v1/op/valid": getOpValid,
    "GET /api/v1/op/id": getOpID,
    "GET /api/v1/op/name": getOpName,
    "PUT /api/v1/op/name": putOpName,
    "GET /api/v1/op/path": getOpPath,
    "GET /api/v1/op/storage": getOpStorage,
    "GET /api/v1/op/tags": getOpTags,
    "POST /api/v1/op/tags": postOpTags,
    "DELETE /api/v1/op/tags": deleteOpTags,

    "GET /api/v1/op/bypass": getOpBypass,
    "GET /api/v1/op/bypass": putOpBypass,
    "GET /api/v1/op/par": getOpPar,
    "PUT /api/v1/op/par": putOpPar,
}

'''