module FSSLib

export dummy_catenary, example_mooring_stiffness

dummy_catenary(x; H::Float64 = 1.0, w::Float64 = 1.0) = begin
    a = H / w
    return a .* (cosh.(x ./ a) .- 1.0)
end

example_mooring_stiffness(L::Float64, EA::Float64) = begin
    L <= 0 && error("Length L must be positive.")
    return EA / L
end

end # module
