# ProtocolParser
Bit operations using Python to provide byte streams
## PROPERTY
## curBitsIndex
Indicating the current bit index and updated itself while you call the bit process function
## curBytesIndex
Indicating the current byte index and updated iteself as bit index
## endian
Assigned the endian form when you create a instance, default is big endian; The bit set action only provide big endian
## METHOD
### getStreamInBytes
Get the hex string in bytes type
### getSegmentByIndex
Get assigned bit segment from stream, which sliced by input bit start index and bit width
### setSegmentByIndex
Set a value to the assigned bit offset with input width in bytes stream, which set by input  the value, bit start index and the assigned width
        