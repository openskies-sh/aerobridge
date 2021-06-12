from typing import List, NamedTuple

class DroneDetails(NamedTuple):
    ''' A class to hold details of a drone device to be sent to Digital Sky ''' 
    version:str
    txn: str
    deviceId: str
    deviceModelId: str
    operatorBusinessIdentifier: str
    idHash: str

class RPASRegistrationPayload(NamedTuple):
    ''' A class to hold payload to be sent to register a drone to Digital Sky '''
    drone: DroneDetails
    signature: str
    digitalCertificate: str
    droneCertificate: str

class DroneCertificateDetails(NamedTuple):
    ''' A class to hold details of a drone certificate ''' 
    deviceID : str
    deviceModelId: str

class RPASCertificate(NamedTuple):
    ''' A class to hold details of a RPAS Certificate data to be submitted to Digital Sky '''
    drone: DroneCertificateDetails
    signature: str
    digitalCertificate: str
    droneCertificate: str
    
class LogEntry(NamedTuple):
    ''' A log entry class to hold details of a flight log '''
    entryType: str
    timeStamp: int
    longitude: float
    latitude: float
    altitude: float
    crc: float
    
class FlightLogDetail(NamedTuple):
    ''' A class to hold details of a flight log '''
    permissionArtefact:str
    previousLogHash: str
    logEntries: List[LogEntry]
    
class FlightLogFile(NamedTuple):
    ''' A class to hold raw file (that has to be zipped) before sending to DigitalSky ''' 
    
    id: str
    flightLog: FlightLogDetail
    signature:str
    startTime: str
    endTime: str
    fileKey: str
    flightLogStatus: str
    
class FlightLogPayload(NamedTuple):
    
    uin: str
    permissionArtefactId: str
    flightLogFile: FlightLogFile
    
    
class ArtefactRequest(NamedTuple):
    ''' A class to request artefacts from Digital Sky ''' 
    flightPlanId: str