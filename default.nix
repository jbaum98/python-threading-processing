{ lib, python }:

python.pkgs.buildPythonApplication rec {
  pname = "python-threading-processing";
  version = "0.0.1";

  src = lib.sourceFilesBySuffices ./. [ ".py" ];

  propagatedBuildInputs = with python.pkgs; [
   matplotlib
   numpy
  ];
}
