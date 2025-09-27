# home/yrrrrrf/lab/code/python/qt-ingot/flake.nix
{
  description = "A development environment for the qt-ingot Python project";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };

      # List all the system libraries Qt needs to run.
      # This is the key to solving the problem declaratively.
      qt-runtime-deps = with pkgs; [
        # Core Wayland and graphics libraries
        wayland
        libglvnd
        
        # Essential for keyboard input and X11 compatibility
        libxkbcommon
        xorg.libxcb 

        # Other common dependencies
        xorg.libX11
        xorg.libXcursor
        xorg.libXi
        xorg.libXinerama
        xorg.libXrandr
        fontconfig
        freetype
        glib
        alsa-lib
      ];

    in
    {
      # This defines the development shell you will enter with `nix develop`
      devShells.${system}.default = pkgs.mkShell {
        # These are the packages available in the shell
        buildInputs = [
          # The tool to manage our python environment
          pkgs.uv

          # The Qt libraries themselves
          pkgs.qt6.qtbase
          pkgs.qt6.qtwayland

          # And crucially, all the runtime dependencies
        ] ++ qt-runtime-deps;

        # These environment variables will be set automatically inside the shell
        shellHook = ''
          export QT_QPA_PLATFORM="wayland"
          echo "✅ Entered qt-ingot development shell."
        '';
      };
    };
}
