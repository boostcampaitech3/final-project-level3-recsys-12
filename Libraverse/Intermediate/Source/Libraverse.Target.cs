using UnrealBuildTool;

public class LibraverseTarget : TargetRules
{
	public LibraverseTarget(TargetInfo Target) : base(Target)
	{
		DefaultBuildSettings = BuildSettingsVersion.V2;
		Type = TargetType.Game;
		ExtraModuleNames.Add("Libraverse");
	}
}
