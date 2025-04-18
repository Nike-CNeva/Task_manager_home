nix
{
  description = "Task manager";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

  outputs = { self, nixpkgs }:
  let
    supportedSystems = [ "x86_64-linux" "aarch64-linux" ];
    forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
  in {
    devShells = forAllSystems (system: {
      default = import ./dev.nix {
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ ];
        };
      };
    });
  };
}