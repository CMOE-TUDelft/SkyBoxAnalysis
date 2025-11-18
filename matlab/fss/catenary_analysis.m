function y = catenary_analysis(x, H, w)
%CATENARY_ANALYSIS Simple placeholder catenary-like curve.
%   y = catenary_analysis(x, H, w)
%
%   x : horizontal coordinate (vector)
%   H : horizontal tension
%   w : weight per unit length

if nargin < 2, H = 1.0; end
if nargin < 3, w = 1.0; end

a = H / w;
y = a * (cosh(x / a) - 1.0);
end
