% Add the matlab folder (which contains +fss) to the path
here = fileparts(mfilename('fullpath'));
repo_root = fullfile(here, '..');
addpath(repo_root);

x = linspace(-5, 5, 201);
y = fss.catenary_analysis(x, 10.0, 2.0);

fprintf('Catenary y-range: %g to %g\n', min(y), max(y));
