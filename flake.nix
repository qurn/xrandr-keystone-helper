{
  # Good overview of flakes: https://www.tweag.io/blog/2020-05-25-flakes/
  inputs = {
    nixpkgs.url = "nixpkgs/master";
  };

  outputs = flakes @ { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs {
        inherit system;
        overlays = [
          self.overlays.default
        ];
        config = { allowUnfree = true; };
      };

      # Helper function to generate an attrset '{ x86_64-linux = f "x86_64-linux"; ... }'.
      forAllSystems = f: nixpkgs.lib.genAttrs supportedSystems (system: f system);

      # AMI Supported Systems
      supportedSystems = [ "x86_64-linux" ];
    in
    {
      overlays.default =
        (final: prev: rec {
          xrandr-keystone-helper = final.writers.writePython3Bin "xrandr-keystone-helper" { libraries = with pkgs.python311Packages; [ numpy matplotlib ]; flakeIgnore = [ "E501" "E265" "W291" "E231" "E226" "E241" "" ]; } ./xrandr-keystone-helper.py;
        });

      packages.x86_64-linux = {
        inherit pkgs;
      };
    };
}
