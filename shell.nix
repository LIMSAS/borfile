with import <nixpkgs> { };

let
  pythonPackages = python311Packages;
in pkgs.mkShell rec {
  name = "bor-file";
  venvDir = "./.venv";

  nativeBuildInputs = with pkgs; [
    netcdf
    bashInteractive
    cmake
    gcc
    pkg-config
  ];

  buildInputs = [
    # A Python interpreter including the 'venv' module is required to bootstrap
    # the environment.
    pythonPackages.python

    # This executes some shell code to initialize a venv in $venvDir before
    # dropping into the shell
    pythonPackages.venvShellHook

    # Those are dependencies that we would like to use from nixpkgs, which will
    # add them to PYTHONPATH and thus make them accessible from within the venv.
    pythonPackages.numpy
    pythonPackages.requests
    pythonPackages.pandas

    # In this particular example, in order to compile any binary extensions they may
    # require, the Python modules listed in the hypothetical requirements.txt need
    # the following packages to be installed locally:
    acl
    git
    libb2
    libxml2
    libxslt
    libzip
    lz4.dev
    openssl
    openssl.dev
    pkg-config
    stdenv.cc.cc
    taglib
    zlib
    zstd.dev
  ];

  # Run this command, only after creating the virtual environment
  postVenvCreation = ''
    unset SOURCE_DATE_EPOCH
    make init-dev
  '';

  # Now we can execute any commands within the virtual environment.
  # This is optional and can be left out to run pip manually.
  postShellHook = ''
    # allow pip to install wheels
    unset SOURCE_DATE_EPOCH
    export NIX_ACTIVE_SHELL='${name}'
    export NIX_SHELL_DIR="${toString ./.}"
    export PATH="$NIX_SHELL_DIR/scripts:$PATH"
    export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath [ pkgs.stdenv.cc.cc.lib pkgs.openssl.dev ]}:${pkgs.stdenv.cc.cc.lib}/lib64:/lib64"
  '';
}
