[Setup]
AppName=PyCalc-SE
AppVerName=PyCalc-SE v1.3
AppPublisher=Chill-Astro
DefaultDirName={autopf}\Chill-Astro\PyCalc-SE 
DefaultGroupName=Chill-Astro                 
UninstallDisplayIcon={app}\Pycalc-SE.exe
DisableWelcomePage=no
Compression=lzma2               
SolidCompression=yes            
ArchitecturesAllowed=x64compatible 
ArchitecturesInstallIn64BitMode=x64compatible 
OutputDir=Output                
OutputBaseFilename=PyCalc-SE-Setup 
WizardStyle=modern            

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\Master\Chill-Astro\PyCalc-SE\dist\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\PyCalc-SE"; Filename: "{app}\PyCalc-SE.exe"; IconFilename: "{app}\PyCalc-SE.ico"
Name: "{commondesktop}\PyCalc-SE"; Filename: "{app}\PyCalc-SE.exe"; IconFilename: "{app}\PyCalc-SE.ico"; Tasks: desktopicon

[Registry]
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; ValueName: "Path"; ValueType: expandsz; ValueData: "{olddata};{app}";