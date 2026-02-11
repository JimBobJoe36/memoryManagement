# Option 2: ML Model for Real-World Problem (technical track)
- Document process, evaluate accuracy, discuss limitations
- Present use case, model performance, and ethical considerations
- Deliverable: working code + demonstration

# Planning and Reflection
Problem: Abnormally high CPU/RAM usage

Proposed Solution: Python program that gets the current CPU usage, and flags programs that takes up high amounts of data, either terminating or alerting the user of the process

Failures: 
- <s>Detects Windows services, and flags them</s>

Reflection (Based on Flow Chart):
- Does IsolationForest work with floats?
    - Yes, but it had to be turned into a 2-D array with numpy.
- What is an "ArrayLike" data type?
    - An "ArrayLike" data type is a custom data type utilized by numpy, signalling that the data has to be an array. The array could be a string, float, integer, etc.
- How simple would it be to implement finding the usual culprits?
    - It would require a few tweaks to the code. The bigger issue is that the same processes that are flagged are consistently flagged at different states of running. In order to do this, the Windows processes would have to be exempted from that, as they cannot be "turned off".