QR Code Reader
==============

This project is a QR Code Reader using OpenCV, Pyzbar, and Tkinter. It captures QR codes from a webcam, processes the data, and saves it either locally or on a USB drive.

Features
--------

*   Captures and decodes QR codes in real time.
    
*   Supports both **Objective** and **Subjective** QR code formats.
    
*   Saves scanned QR codes to a local folder (QRCodeOutputs/).
    
*   Automatically saves data to a USB drive if available.
    
*   Provides a GUI using Tkinter.
    
*   Includes settings to configure an **Event Key**.
    
*   Allows transferring local data to a USB drive.
    

Dependencies
------------

Ensure you have the following Python libraries installed:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bashCopyEditpip install opencv-python numpy pyzbar pillow   `

How It Works
------------

The script opens a webcam feed and continuously scans for QR codes.

If a QR code is detected:

*   It extracts relevant data such as match ID, team number, and collection mode.
    
*   It constructs a filename based on the extracted details.
    
*   If the **Space** key is pressed, the data is saved.
    

The program provides buttons to:

*   Open the saved QR codes folder.
    
*   Open the USB drive (if available).
    
*   Move local data to the USB drive.
    

File Storage Behavior
---------------------

If a USB drive (E:/) is available, the QR data is stored at:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bashCopyEditE:/data/{match_id}_{team_number}_{event_key}_{collection_mode}.txt   `

Otherwise, data is saved locally at:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bashCopyEditQRCodeOutputs/{match_id}_{team_number}_{event_key}_{collection_mode}.txt   `

If USB is available, the data is stored both locally and on USB.

GUI Controls
------------

*   F11 → Toggle Fullscreen Mode
    
*   Esc → Exit Fullscreen Mode
    
*   Space → Save QR Code Data
    
*   Enter → Process QR Code Manually
    

Running the Program
-------------------

Run the script using:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bashCopyEditpython script.py   `

Ensure your webcam is connected and accessible.

Customizing the Event Key
-------------------------

1.  Click the **Settings** button in the GUI.
    
2.  Enter a custom event key.
    
3.  Click **Save** to apply changes.
    

Moving Local Data to USB
------------------------

Click the **Move Local Data To USB** button in the GUI to transfer stored QR codes to the USB drive (E:/data).

Notes
-----

*   The script checks for a valid USB drive before attempting to save.
    
*   If the event key is not set, it must be configured before saving QR data.
    
*   The script handles errors gracefully and prevents duplicate file transfers.
    

License
-------

This project is licensed under the MIT License.
